#
# Generated Makefile - do not edit!
#
# Edit the Makefile in the project folder instead (../Makefile). Each target
# has a -pre and a -post target defined where you can add customized code.
#
# This makefile implements configuration specific macros and targets.


# Environment
MKDIR=mkdir
CP=cp
GREP=grep
NM=nm
CCADMIN=CCadmin
RANLIB=ranlib
CC=gcc
CCC=g++
CXX=g++
FC=gfortran
AS=as

# Macros
CND_PLATFORM=GNU-Linux
CND_DLIB_EXT=so
CND_CONF=Debug
CND_DISTDIR=dist
CND_BUILDDIR=build

# Include project Makefile
include Makefile

# Object Directory
OBJECTDIR=${CND_BUILDDIR}/${CND_CONF}/${CND_PLATFORM}

# Object Files
OBJECTFILES= \
	${OBJECTDIR}/Annot.o \
	${OBJECTDIR}/Array.o \
	${OBJECTDIR}/BuiltinFont.o \
	${OBJECTDIR}/BuiltinFontTables.o \
	${OBJECTDIR}/CMap.o \
	${OBJECTDIR}/CachedFile.o \
	${OBJECTDIR}/Catalog.o \
	${OBJECTDIR}/CharCodeToUnicode.o \
	${OBJECTDIR}/DCTStream.o \
	${OBJECTDIR}/DateInfo.o \
	${OBJECTDIR}/Decrypt.o \
	${OBJECTDIR}/Dict.o \
	${OBJECTDIR}/Error.o \
	${OBJECTDIR}/FileSpec.o \
	${OBJECTDIR}/FlateEncoder.o \
	${OBJECTDIR}/FlateStream.o \
	${OBJECTDIR}/FontEncodingTables.o \
	${OBJECTDIR}/FontInfo.o \
	${OBJECTDIR}/Form.o \
	${OBJECTDIR}/Function.o \
	${OBJECTDIR}/Gfx.o \
	${OBJECTDIR}/GfxFont.o \
	${OBJECTDIR}/GfxState.o \
	${OBJECTDIR}/GlobalParams.o \
	${OBJECTDIR}/Hints.o \
	${OBJECTDIR}/JArithmeticDecoder.o \
	${OBJECTDIR}/JBIG2Stream.o \
	${OBJECTDIR}/JPEG2000Stream.o \
	${OBJECTDIR}/Lexer.o \
	${OBJECTDIR}/Linearization.o \
	${OBJECTDIR}/Link.o \
	${OBJECTDIR}/LocalPDFDocBuilder.o \
	${OBJECTDIR}/MarkedContentOutputDev.o \
	${OBJECTDIR}/Movie.o \
	${OBJECTDIR}/NameToCharCode.o \
	${OBJECTDIR}/Object.o \
	${OBJECTDIR}/OptionalContent.o \
	${OBJECTDIR}/Outline.o \
	${OBJECTDIR}/OutputDev.o \
	${OBJECTDIR}/PDFDoc.o \
	${OBJECTDIR}/PDFDocEncoding.o \
	${OBJECTDIR}/PDFDocFactory.o \
	${OBJECTDIR}/PSOutputDev.o \
	${OBJECTDIR}/PSTokenizer.o \
	${OBJECTDIR}/Page.o \
	${OBJECTDIR}/PageLabelInfo.o \
	${OBJECTDIR}/PageTransition.o \
	${OBJECTDIR}/Parser.o \
	${OBJECTDIR}/PopplerCache.o \
	${OBJECTDIR}/PreScanOutputDev.o \
	${OBJECTDIR}/ProfileData.o \
	${OBJECTDIR}/Rendition.o \
	${OBJECTDIR}/SecurityHandler.o \
	${OBJECTDIR}/SignatureHandler.o \
	${OBJECTDIR}/SignatureInfo.o \
	${OBJECTDIR}/Sound.o \
	${OBJECTDIR}/SplashOutputDev.o \
	${OBJECTDIR}/StdinCachedFile.o \
	${OBJECTDIR}/StdinPDFDocBuilder.o \
	${OBJECTDIR}/Stream.o \
	${OBJECTDIR}/StructElement.o \
	${OBJECTDIR}/StructTreeRoot.o \
	${OBJECTDIR}/TextOutputDev.o \
	${OBJECTDIR}/UTF.o \
	${OBJECTDIR}/UnicodeMap.o \
	${OBJECTDIR}/UnicodeTypeTable.o \
	${OBJECTDIR}/ViewerPreferences.o \
	${OBJECTDIR}/XRef.o \
	${OBJECTDIR}/XpdfPluginAPI.o


# C Compiler Flags
CFLAGS=

# CC Compiler Flags
CCFLAGS=-fPIC
CXXFLAGS=-fPIC

# Fortran Compiler Flags
FFLAGS=

# Assembler Flags
ASFLAGS=

# Link Libraries and Options
LDLIBSOPTIONS=-L/usr/lib/x86_64-linux-gnu -L../output/${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM} -L../openjpeg/openjpeg-v2.3.0-linux-x86_64/lib/openjpeg-2.3 -Wl,-rpath,'./' -lnss3 -lfreetype -lopenjp2 -lfontconfig -llcms2 -lnssutil3 -lnss_files -lnss_nis -ljpeg -lgoo -lfofi -lsplash

# Build Targets
.build-conf: ${BUILD_SUBPROJECTS}
	"${MAKE}"  -f nbproject/Makefile-${CND_CONF}.mk ../output/${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/libpoppler.${CND_DLIB_EXT}

../output/${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/libpoppler.${CND_DLIB_EXT}: ${OBJECTFILES}
	${MKDIR} -p ../output/${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}
	${LINK.cc} -o ../output/${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/libpoppler.${CND_DLIB_EXT} ${OBJECTFILES} ${LDLIBSOPTIONS} -shared -fPIC

${OBJECTDIR}/Annot.o: Annot.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/Annot.o Annot.cc

${OBJECTDIR}/Array.o: Array.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/Array.o Array.cc

${OBJECTDIR}/BuiltinFont.o: BuiltinFont.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/BuiltinFont.o BuiltinFont.cc

${OBJECTDIR}/BuiltinFontTables.o: BuiltinFontTables.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/BuiltinFontTables.o BuiltinFontTables.cc

${OBJECTDIR}/CMap.o: CMap.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/CMap.o CMap.cc

${OBJECTDIR}/CachedFile.o: CachedFile.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/CachedFile.o CachedFile.cc

${OBJECTDIR}/Catalog.o: Catalog.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/Catalog.o Catalog.cc

${OBJECTDIR}/CharCodeToUnicode.o: CharCodeToUnicode.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/CharCodeToUnicode.o CharCodeToUnicode.cc

${OBJECTDIR}/DCTStream.o: DCTStream.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/DCTStream.o DCTStream.cc

${OBJECTDIR}/DateInfo.o: DateInfo.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/DateInfo.o DateInfo.cc

${OBJECTDIR}/Decrypt.o: Decrypt.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/Decrypt.o Decrypt.cc

${OBJECTDIR}/Dict.o: Dict.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/Dict.o Dict.cc

${OBJECTDIR}/Error.o: Error.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/Error.o Error.cc

${OBJECTDIR}/FileSpec.o: FileSpec.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/FileSpec.o FileSpec.cc

${OBJECTDIR}/FlateEncoder.o: FlateEncoder.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/FlateEncoder.o FlateEncoder.cc

${OBJECTDIR}/FlateStream.o: FlateStream.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/FlateStream.o FlateStream.cc

${OBJECTDIR}/FontEncodingTables.o: FontEncodingTables.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/FontEncodingTables.o FontEncodingTables.cc

${OBJECTDIR}/FontInfo.o: FontInfo.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/FontInfo.o FontInfo.cc

${OBJECTDIR}/Form.o: Form.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/Form.o Form.cc

${OBJECTDIR}/Function.o: Function.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/Function.o Function.cc

${OBJECTDIR}/Gfx.o: Gfx.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/Gfx.o Gfx.cc

${OBJECTDIR}/GfxFont.o: GfxFont.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/GfxFont.o GfxFont.cc

${OBJECTDIR}/GfxState.o: GfxState.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/GfxState.o GfxState.cc

${OBJECTDIR}/GlobalParams.o: GlobalParams.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/GlobalParams.o GlobalParams.cc

${OBJECTDIR}/Hints.o: Hints.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/Hints.o Hints.cc

${OBJECTDIR}/JArithmeticDecoder.o: JArithmeticDecoder.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/JArithmeticDecoder.o JArithmeticDecoder.cc

${OBJECTDIR}/JBIG2Stream.o: JBIG2Stream.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/JBIG2Stream.o JBIG2Stream.cc

${OBJECTDIR}/JPEG2000Stream.o: JPEG2000Stream.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/JPEG2000Stream.o JPEG2000Stream.cc

${OBJECTDIR}/Lexer.o: Lexer.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/Lexer.o Lexer.cc

${OBJECTDIR}/Linearization.o: Linearization.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/Linearization.o Linearization.cc

${OBJECTDIR}/Link.o: Link.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/Link.o Link.cc

${OBJECTDIR}/LocalPDFDocBuilder.o: LocalPDFDocBuilder.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/LocalPDFDocBuilder.o LocalPDFDocBuilder.cc

${OBJECTDIR}/MarkedContentOutputDev.o: MarkedContentOutputDev.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/MarkedContentOutputDev.o MarkedContentOutputDev.cc

${OBJECTDIR}/Movie.o: Movie.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/Movie.o Movie.cc

${OBJECTDIR}/NameToCharCode.o: NameToCharCode.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/NameToCharCode.o NameToCharCode.cc

${OBJECTDIR}/Object.o: Object.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/Object.o Object.cc

${OBJECTDIR}/OptionalContent.o: OptionalContent.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/OptionalContent.o OptionalContent.cc

${OBJECTDIR}/Outline.o: Outline.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/Outline.o Outline.cc

${OBJECTDIR}/OutputDev.o: OutputDev.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/OutputDev.o OutputDev.cc

${OBJECTDIR}/PDFDoc.o: PDFDoc.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/PDFDoc.o PDFDoc.cc

${OBJECTDIR}/PDFDocEncoding.o: PDFDocEncoding.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/PDFDocEncoding.o PDFDocEncoding.cc

${OBJECTDIR}/PDFDocFactory.o: PDFDocFactory.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/PDFDocFactory.o PDFDocFactory.cc

${OBJECTDIR}/PSOutputDev.o: PSOutputDev.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/PSOutputDev.o PSOutputDev.cc

${OBJECTDIR}/PSTokenizer.o: PSTokenizer.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/PSTokenizer.o PSTokenizer.cc

${OBJECTDIR}/Page.o: Page.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/Page.o Page.cc

${OBJECTDIR}/PageLabelInfo.o: PageLabelInfo.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/PageLabelInfo.o PageLabelInfo.cc

${OBJECTDIR}/PageTransition.o: PageTransition.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/PageTransition.o PageTransition.cc

${OBJECTDIR}/Parser.o: Parser.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/Parser.o Parser.cc

${OBJECTDIR}/PopplerCache.o: PopplerCache.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/PopplerCache.o PopplerCache.cc

${OBJECTDIR}/PreScanOutputDev.o: PreScanOutputDev.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/PreScanOutputDev.o PreScanOutputDev.cc

${OBJECTDIR}/ProfileData.o: ProfileData.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/ProfileData.o ProfileData.cc

${OBJECTDIR}/Rendition.o: Rendition.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/Rendition.o Rendition.cc

${OBJECTDIR}/SecurityHandler.o: SecurityHandler.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/SecurityHandler.o SecurityHandler.cc

${OBJECTDIR}/SignatureHandler.o: SignatureHandler.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/SignatureHandler.o SignatureHandler.cc

${OBJECTDIR}/SignatureInfo.o: SignatureInfo.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/SignatureInfo.o SignatureInfo.cc

${OBJECTDIR}/Sound.o: Sound.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/Sound.o Sound.cc

${OBJECTDIR}/SplashOutputDev.o: SplashOutputDev.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/SplashOutputDev.o SplashOutputDev.cc

${OBJECTDIR}/StdinCachedFile.o: StdinCachedFile.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/StdinCachedFile.o StdinCachedFile.cc

${OBJECTDIR}/StdinPDFDocBuilder.o: StdinPDFDocBuilder.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/StdinPDFDocBuilder.o StdinPDFDocBuilder.cc

${OBJECTDIR}/Stream.o: Stream.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/Stream.o Stream.cc

${OBJECTDIR}/StructElement.o: StructElement.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/StructElement.o StructElement.cc

${OBJECTDIR}/StructTreeRoot.o: StructTreeRoot.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/StructTreeRoot.o StructTreeRoot.cc

${OBJECTDIR}/TextOutputDev.o: TextOutputDev.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/TextOutputDev.o TextOutputDev.cc

${OBJECTDIR}/UTF.o: UTF.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/UTF.o UTF.cc

${OBJECTDIR}/UnicodeMap.o: UnicodeMap.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/UnicodeMap.o UnicodeMap.cc

${OBJECTDIR}/UnicodeTypeTable.o: UnicodeTypeTable.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/UnicodeTypeTable.o UnicodeTypeTable.cc

${OBJECTDIR}/ViewerPreferences.o: ViewerPreferences.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/ViewerPreferences.o ViewerPreferences.cc

${OBJECTDIR}/XRef.o: XRef.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/XRef.o XRef.cc

${OBJECTDIR}/XpdfPluginAPI.o: XpdfPluginAPI.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/XpdfPluginAPI.o XpdfPluginAPI.cc

${OBJECTDIR}/common_types.h.gch: common_types.h
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/nspr -I/usr/include/nss -I/usr/include/freetype2 -I../openjpeg/openjpeg-v2.3.0-linux-x86_64/include/openjpeg-2.3 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o "$@" common_types.h

# Subprojects
.build-subprojects:

# Clean Targets
.clean-conf: ${CLEAN_SUBPROJECTS}
	${RM} -r ${CND_BUILDDIR}/${CND_CONF}

# Subprojects
.clean-subprojects:

# Enable dependency checking
.dep.inc: .depcheck-impl

include .dep.inc
