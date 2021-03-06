//========================================================================
//
// SplashFontEngine.cc
//
//========================================================================

//========================================================================
//
// Modified under the Poppler project - http://poppler.freedesktop.org
//
// All changes made under the Poppler project to this file are licensed
// under GPL version 2 or later
//
// Copyright (C) 2006 Takashi Iwai <tiwai@suse.de>
// Copyright (C) 2009 Petr Gajdos <pgajdos@novell.com>
// Copyright (C) 2009 Kovid Goyal <kovid@kovidgoyal.net>
// Copyright (C) 2009 Albert Astals Cid <aacid@kde.org>
// Copyright (C) 2011 Andreas Hartmetz <ahartmetz@gmail.com>
// Copyright (C) 2013 Thomas Freitag <Thomas.Freitag@alfa.de>
// Copyright (C) 2015 Dmytro Morgun <lztoad@gmail.com>
// Copyright (C) 2017 Adrian Johnson <ajohnson@redneon.com>
//
// To see a description of the changes please see the Changelog file that
// came with your tarball or type make ChangeLog if you are building from git
//
//========================================================================

#include "../config.h"

#ifdef USE_GCC_PRAGMAS
#pragma implementation
#endif

#include <stdlib.h>
#include <stdio.h>
#ifdef HAVE_UNISTD_H
#  include <unistd.h>
#endif
#include "../goo/gmem.h"
#include "../goo/GooString.h"
#include "SplashMath.h"
#include "SplashFTFontEngine.h"
#include "SplashFontFile.h"
#include "SplashFontFileID.h"
#include "SplashFont.h"
#include "SplashFontEngine.h"

#ifdef VMS
#if (__VMS_VER < 70000000)
extern "C" int unlink(char *filename);
#endif
#endif

#ifdef VMS
#if (__VMS_VER < 70000000)
extern "C" int unlink(char *filename);
#endif
#endif

//------------------------------------------------------------------------
// SplashFontEngine
//------------------------------------------------------------------------

SplashFontEngine::SplashFontEngine(
				   GBool enableFreeType,
				   GBool enableFreeTypeHinting,
				   GBool enableSlightHinting,
				   GBool aa) {
  int i;

  for (i = 0; i < splashFontCacheSize; ++i) {
    fontCache[i] = NULL;
  }

  if (enableFreeType) {
    ftEngine = SplashFTFontEngine::init(aa, enableFreeTypeHinting, enableSlightHinting);
  } else {
    ftEngine = NULL;
  }
}

SplashFontEngine::~SplashFontEngine() {
  int i;

  for (i = 0; i < splashFontCacheSize; ++i) {
    if (fontCache[i]) {
      delete fontCache[i];
    }
  }

  if (ftEngine) {
    delete ftEngine;
  }
}

SplashFontFile *SplashFontEngine::getFontFile(SplashFontFileID *id) {
  SplashFontFile *fontFile;
  int i;

  for (i = 0; i < splashFontCacheSize; ++i) {
    if (fontCache[i]) {
      fontFile = fontCache[i]->getFontFile();
      if (fontFile && fontFile->getID()->matches(id)) {
	return fontFile;
      }
    }
  }
  return NULL;
}

SplashFontFile *SplashFontEngine::loadType1Font(SplashFontFileID *idA,
						SplashFontSrc *src,
						const char **enc) {
  SplashFontFile *fontFile;

  fontFile = NULL;
  if (!fontFile && ftEngine) {
    fontFile = ftEngine->loadType1Font(idA, src, enc);
  }

  // delete the (temporary) font file -- with Unix hard link
  // semantics, this will remove the last link; otherwise it will
  // return an error, leaving the file to be deleted later (if
  // loadXYZFont failed, the file will always be deleted)
  if (src->isFile)
    src->unref();

  return fontFile;
}

SplashFontFile *SplashFontEngine::loadType1CFont(SplashFontFileID *idA,
						 SplashFontSrc *src,
						 const char **enc) {
  SplashFontFile *fontFile;

  fontFile = NULL;
  if (!fontFile && ftEngine) {
    fontFile = ftEngine->loadType1CFont(idA, src, enc);
  }

  // delete the (temporary) font file -- with Unix hard link
  // semantics, this will remove the last link; otherwise it will
  // return an error, leaving the file to be deleted later (if
  // loadXYZFont failed, the file will always be deleted)
  if (src->isFile)
    src->unref();

  return fontFile;
}

SplashFontFile *SplashFontEngine::loadOpenTypeT1CFont(SplashFontFileID *idA,
						      SplashFontSrc *src,
						      const char **enc) {
  SplashFontFile *fontFile;

  fontFile = NULL;
  if (!fontFile && ftEngine) {
    fontFile = ftEngine->loadOpenTypeT1CFont(idA, src, enc);
  }

  // delete the (temporary) font file -- with Unix hard link
  // semantics, this will remove the last link; otherwise it will
  // return an error, leaving the file to be deleted later (if
  // loadXYZFont failed, the file will always be deleted)
  if (src->isFile)
    src->unref();

  return fontFile;
}

SplashFontFile *SplashFontEngine::loadCIDFont(SplashFontFileID *idA,
					      SplashFontSrc *src) {
  SplashFontFile *fontFile;

  fontFile = NULL;
  if (!fontFile && ftEngine) {
    fontFile = ftEngine->loadCIDFont(idA, src);
  }

  // delete the (temporary) font file -- with Unix hard link
  // semantics, this will remove the last link; otherwise it will
  // return an error, leaving the file to be deleted later (if
  // loadXYZFont failed, the file will always be deleted)
  if (src->isFile)
    src->unref();

  return fontFile;
}

SplashFontFile *SplashFontEngine::loadOpenTypeCFFFont(SplashFontFileID *idA,
						      SplashFontSrc *src,
                                                      int *codeToGID,
                                                      int codeToGIDLen) {
  SplashFontFile *fontFile;

  fontFile = NULL;
  if (!fontFile && ftEngine) {
    fontFile = ftEngine->loadOpenTypeCFFFont(idA, src, codeToGID, codeToGIDLen);
  }

  // delete the (temporary) font file -- with Unix hard link
  // semantics, this will remove the last link; otherwise it will
  // return an error, leaving the file to be deleted later (if
  // loadXYZFont failed, the file will always be deleted)
  if (src->isFile)
    src->unref();

  return fontFile;
}

SplashFontFile *SplashFontEngine::loadTrueTypeFont(SplashFontFileID *idA,
						   SplashFontSrc *src,
						   int *codeToGID,
						   int codeToGIDLen,
						   int faceIndex) {
  SplashFontFile *fontFile;

  fontFile = NULL;
  if (!fontFile && ftEngine) {
    fontFile = ftEngine->loadTrueTypeFont(idA, src,
                                        codeToGID, codeToGIDLen, faceIndex);
  }

  if (!fontFile) {
    gfree(codeToGID);
  }

  // delete the (temporary) font file -- with Unix hard link
  // semantics, this will remove the last link; otherwise it will
  // return an error, leaving the file to be deleted later (if
  // loadXYZFont failed, the file will always be deleted)
  if (src->isFile)
    src->unref();

  return fontFile;
}

GBool SplashFontEngine::getAA() {
  return (ftEngine == NULL) ? gFalse : ftEngine->getAA();
}

void SplashFontEngine::setAA(GBool aa) {
  if (ftEngine != NULL) {
    ftEngine->setAA(aa);
  }
}

SplashFont *SplashFontEngine::getFont(SplashFontFile *fontFile,
				      SplashCoord *textMat,
				      SplashCoord *ctm) {
  SplashCoord mat[4];
  SplashFont *font;
  int i, j;

  mat[0] = textMat[0] * ctm[0] + textMat[1] * ctm[2];
  mat[1] = -(textMat[0] * ctm[1] + textMat[1] * ctm[3]);
  mat[2] = textMat[2] * ctm[0] + textMat[3] * ctm[2];
  mat[3] = -(textMat[2] * ctm[1] + textMat[3] * ctm[3]);
  if (!splashCheckDet(mat[0], mat[1], mat[2], mat[3], 0.01)) {
    // avoid a singular (or close-to-singular) matrix
    mat[0] = 0.01;  mat[1] = 0;
    mat[2] = 0;     mat[3] = 0.01;
  }

  font = fontCache[0];
  if (font && font->matches(fontFile, mat, textMat)) {
    return font;
  }
  for (i = 1; i < splashFontCacheSize; ++i) {
    font = fontCache[i];
    if (font && font->matches(fontFile, mat, textMat)) {
      for (j = i; j > 0; --j) {
	fontCache[j] = fontCache[j-1];
      }
      fontCache[0] = font;
      return font;
    }
  }
  font = fontFile->makeFont(mat, textMat);
  if (fontCache[splashFontCacheSize - 1]) {
    delete fontCache[splashFontCacheSize - 1];
  }
  for (j = splashFontCacheSize - 1; j > 0; --j) {
    fontCache[j] = fontCache[j-1];
  }
  fontCache[0] = font;
  return font;
}
