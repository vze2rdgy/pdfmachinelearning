"""
Reader that examines PDF file converted to text by Poppler's text extractor.
This reader examines features of each line in the text file and generates
a feature set that defines the structure of the document.
"""

import io, os
from enum import IntFlag

Sections = IntFlag(
    "Sections", 
    "PAGEHEADER PAGE_FOOTER \
    LIST_KEY_VALUE_START LIST_KEY_VALUE_LINE LIST_KEY_VALUE_LINE_CONTINUE LIST_KEY_VALUE_END \
    TABLEROW \
    SINGLE_COL_PARA_START SINGLE_COL_PARA_END SINGLE_COL_PARA_MIDDLE \
    MULTI_COL_PARA_START MULTI_COL_PARA_LINE MULTI_COL_PARA_END"
)


class PopplerPDFTextFeatureBuilder(object):
    __slots__ = [
        "_iostream",
        "_featureNames",
        "_docStructInfo", # a dictionary key=section, value another dictionary featureName:value
        "_pageIncr",
    ]
    def __init__(self, StreamOrFilepath):
        if isinstance(StreamOrFilepath, io.TextIOBase):
            self._iostream = StreamOrFilepath
        elif isinstance(StreamOrFilepath, str):
            if not os.path.exists(StreamOrFilepath):
                raise ValueError("File not found.")
            self._iostream = open(StreamOrFilepath, "r")
        else:
            raise ValueError("Invalid argument")
        self._pageIncr = 0
        self._featureNames = set()
        self._docStructInfo = {}
        self._docStructInfo["features"] = {}
        return

    def _getDocumentLevelFeatures(self):
        self._iostream.seek(0)
        docWidth = 0
        for l in self._iostream.readlines():
            docWidth = max(docWidth, len(l))
        self._docStructInfo["docWidth"] = docWidth
        return

    def _initFeatures(self):
        return {
                "PageNo" : None,
                "IsPageheader" : False,
                "LeftSpace" : None,
                "RightSpace" : None,
                "GapCount" : None,
                "Gaps" : None,
                "Semicolons" : None,
                "Periods" : None,
                "FirstChar" : None,
                "HasMatchingGapPositionFromPrevious" : False, 
                "HasMatchingGapPositionToNext" : False, 
                "Section" : None, # target
                "Line" : None # cached line
            }

    def _getLineFeatures(self, allLines, lineIndex):
        line = allLines[lineIndex]
        # check if unicode char 0x00FF (Y with two dots above) is the first char. If yes,
        # then it is a page start
        features = self._initFeatures()
        isPageHeader = False
        firstChar = None
        if line:
            c = line[0].encode("utf-8")
            firstChar = c
            if c == b"\xc3\xbf":
                pageno = features.get("PageNo")
                isPageHeader = True
                if not pageno:
                    features["PageNo"] = self._pageIncr
                self._pageIncr += 1
            else:
                # reuse the same page no
                features["PageNo"] = self._pageIncr

            # check other properties
            # examine gaps between
            # numlargegaps
            startGapOffset = -1
            leftoffset = -1
            gaps = []
            gapwidth = 0
            endPos = 0
            for i in range(len(line)):
                endPos = i
                c = line[i]
                if not c or c == ' ':
                    gapwidth += 1
                    if leftoffset < 0:
                        leftoffset = i
                else:
                    if startGapOffset < 0:
                        startGapOffset = leftoffset
                    if gapwidth > 1:
                            # tuple values:
                            # 0: first char position from left of the doc or from after previous gap
                            # 1: length of gap chars (spaces)
                            # 2: position+1 at the end of the gap where next char begins
                            gaps.append((leftoffset, gapwidth, i)) 
                            gapwidth = 0
                            leftoffset = -1
            if gapwidth > 1:
                # tuple values:
                # 0: first char position from left of the doc or from after previous gap
                # 1: length of gap chars (spaces)
                # 2: position+1 at the end of the gap where next char begins
                gaps.append((leftoffset, gapwidth, endPos))

            # check space between last char and right end
            if self._docStructInfo["docWidth"] - endPos > 1:
                gaps.append((endPos, self._docStructInfo["docWidth"] - endPos, self._docStructInfo["docWidth"]-1))

            features["IsPageheader"] = isPageHeader # is it a page header line ?
            features["LeftSpace"] = startGapOffset # how much space left on left side ?
            features["RightSpace"] = self._docStructInfo["docWidth"] - endPos # how much space left on the right side
            features["GapCount"] = len(gaps)
            features["Gaps"] = gaps

            #store special char counts
            features["Semicolons"] = line.count(":")
            features["Periods"] = line.count(".")

            features["FirstChar"] = firstChar
            if isPageHeader:
                features["Section"] = Sections.PAGEHEADER

        features["Line"] = line

        return features

    def Construct(self):
        self._getDocumentLevelFeatures()
        self._iostream.seek(0)
        lines = self._iostream.readlines()
        lcount = len(lines)
        for i in range(lcount):
            dFeat = self._getLineFeatures(lines, i)
            self._docStructInfo["features"][i] = dFeat
            # get features of last line
            if i > 0:
                dLFeat = self._getLineFeatures(lines, i-1)
                # compare how many gaps
                if dLFeat["GapCount"] == dFeat["GapCount"]: 
                    # if gap counts are same, check chars after gap starts same position
                    lgaps = dLFeat["Gaps"]
                    cgaps = dFeat["Gaps"]
                    # tuple values 0, and 2 are compared
                    bFlag = True
                    for lg, cg in zip(lgaps, cgaps):
                        bFlag &= lg[2] == cg[2]
                    dFeat["HasMatchingGapPositionFromPrevious"] = bFlag


            if i < (lcount - 2):
                dNFeat = self._getLineFeatures(lines, i+1)
                # compare how many gaps
                if dNFeat["GapCount"] == dFeat["GapCount"]: 
                    # if gap counts are same, check chars after gap starts same position
                    ngaps = dNFeat["Gaps"]
                    cgaps = dFeat["Gaps"]
                    bFlag = True
                    for cg, ng in zip(cgaps, ngaps):
                        bFlag &= ng[2] == cg[2]
                    dFeat["HasMatchingGapPositionToNext"] = bFlag

            if dFeat["Semicolons"] == 1:
                if dFeat["HasMatchingGapPositionToNext"] and not dFeat["HasMatchingGapPositionFromPrevious"]:
                    dFeat["Section"] = Sections.LIST_KEY_VALUE_START
                elif dFeat["HasMatchingGapPositionToNext"] and dFeat["HasMatchingGapPositionFromPrevious"]:
                    dFeat["Section"] = Sections.LIST_KEY_VALUE_LINE
                elif not dFeat["HasMatchingGapPositionToNext"] and dFeat["HasMatchingGapPositionFromPrevious"]:
                    dFeat["Section"] = Sections.LIST_KEY_VALUE_END

        return

    def __del__(self):
        self.Close()

    def Close(self):
        if self._iostream:
            self._iostream.close()
            self._iostream = None



if __name__ == "__main__" :
    filePath = "../../convertedfiles/31016_PromaCareTM_BR.txt"
    pop = PopplerPDFTextFeatureBuilder(filePath)
    pop.Construct()
    pop.Close()
