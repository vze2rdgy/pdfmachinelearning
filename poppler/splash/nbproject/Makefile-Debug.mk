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
	${OBJECTDIR}/Splash.o \
	${OBJECTDIR}/SplashBitmap.o \
	${OBJECTDIR}/SplashClip.o \
	${OBJECTDIR}/SplashFTFont.o \
	${OBJECTDIR}/SplashFTFontEngine.o \
	${OBJECTDIR}/SplashFTFontFile.o \
	${OBJECTDIR}/SplashFont.o \
	${OBJECTDIR}/SplashFontEngine.o \
	${OBJECTDIR}/SplashFontFile.o \
	${OBJECTDIR}/SplashFontFileID.o \
	${OBJECTDIR}/SplashPath.o \
	${OBJECTDIR}/SplashPattern.o \
	${OBJECTDIR}/SplashScreen.o \
	${OBJECTDIR}/SplashState.o \
	${OBJECTDIR}/SplashXPath.o \
	${OBJECTDIR}/SplashXPathScanner.o


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
LDLIBSOPTIONS=

# Build Targets
.build-conf: ${BUILD_SUBPROJECTS}
	"${MAKE}"  -f nbproject/Makefile-${CND_CONF}.mk ../output/${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/libsplash.${CND_DLIB_EXT}

../output/${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/libsplash.${CND_DLIB_EXT}: ${OBJECTFILES}
	${MKDIR} -p ../output/${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}
	${LINK.cc} -o ../output/${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/libsplash.${CND_DLIB_EXT} ${OBJECTFILES} ${LDLIBSOPTIONS} -shared -fPIC

${OBJECTDIR}/Splash.o: Splash.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/freetype2 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/Splash.o Splash.cc

${OBJECTDIR}/SplashBitmap.o: SplashBitmap.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/freetype2 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/SplashBitmap.o SplashBitmap.cc

${OBJECTDIR}/SplashClip.o: SplashClip.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/freetype2 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/SplashClip.o SplashClip.cc

${OBJECTDIR}/SplashFTFont.o: SplashFTFont.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/freetype2 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/SplashFTFont.o SplashFTFont.cc

${OBJECTDIR}/SplashFTFontEngine.o: SplashFTFontEngine.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/freetype2 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/SplashFTFontEngine.o SplashFTFontEngine.cc

${OBJECTDIR}/SplashFTFontFile.o: SplashFTFontFile.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/freetype2 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/SplashFTFontFile.o SplashFTFontFile.cc

${OBJECTDIR}/SplashFont.o: SplashFont.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/freetype2 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/SplashFont.o SplashFont.cc

${OBJECTDIR}/SplashFontEngine.o: SplashFontEngine.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/freetype2 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/SplashFontEngine.o SplashFontEngine.cc

${OBJECTDIR}/SplashFontFile.o: SplashFontFile.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/freetype2 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/SplashFontFile.o SplashFontFile.cc

${OBJECTDIR}/SplashFontFileID.o: SplashFontFileID.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/freetype2 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/SplashFontFileID.o SplashFontFileID.cc

${OBJECTDIR}/SplashPath.o: SplashPath.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/freetype2 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/SplashPath.o SplashPath.cc

${OBJECTDIR}/SplashPattern.o: SplashPattern.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/freetype2 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/SplashPattern.o SplashPattern.cc

${OBJECTDIR}/SplashScreen.o: SplashScreen.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/freetype2 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/SplashScreen.o SplashScreen.cc

${OBJECTDIR}/SplashState.o: SplashState.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/freetype2 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/SplashState.o SplashState.cc

${OBJECTDIR}/SplashXPath.o: SplashXPath.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/freetype2 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/SplashXPath.o SplashXPath.cc

${OBJECTDIR}/SplashXPathScanner.o: SplashXPathScanner.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -I/usr/include/freetype2 -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/SplashXPathScanner.o SplashXPathScanner.cc

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
