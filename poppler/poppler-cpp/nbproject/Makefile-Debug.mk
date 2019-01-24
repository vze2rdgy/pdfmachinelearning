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
	${OBJECTDIR}/poppler-document.o \
	${OBJECTDIR}/poppler-embedded-file.o \
	${OBJECTDIR}/poppler-font.o \
	${OBJECTDIR}/poppler-global.o \
	${OBJECTDIR}/poppler-image.o \
	${OBJECTDIR}/poppler-page-renderer.o \
	${OBJECTDIR}/poppler-page-transition.o \
	${OBJECTDIR}/poppler-page.o \
	${OBJECTDIR}/poppler-private.o \
	${OBJECTDIR}/poppler-rectangle.o \
	${OBJECTDIR}/poppler-toc.o \
	${OBJECTDIR}/poppler-version.o


# C Compiler Flags
CFLAGS=

# CC Compiler Flags
CCFLAGS=
CXXFLAGS=

# Fortran Compiler Flags
FFLAGS=

# Assembler Flags
ASFLAGS=

# Link Libraries and Options
LDLIBSOPTIONS=-L/usr/lib/x86_64-linux-gnu -L../output/../output/${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM} -Wl,-rpath,'./' -lnss3 -lgoo -lfofi -lpoppler -lsplash

# Build Targets
.build-conf: ${BUILD_SUBPROJECTS}
	"${MAKE}"  -f nbproject/Makefile-${CND_CONF}.mk ../output/${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/libpoppler-cpp.${CND_DLIB_EXT}

../output/${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/libpoppler-cpp.${CND_DLIB_EXT}: ${OBJECTFILES}
	${MKDIR} -p ../output/${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}
	${LINK.cc} -o ../output/${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/libpoppler-cpp.${CND_DLIB_EXT} ${OBJECTFILES} ${LDLIBSOPTIONS} -shared -fPIC

${OBJECTDIR}/poppler-document.o: poppler-document.cpp
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/poppler-document.o poppler-document.cpp

${OBJECTDIR}/poppler-embedded-file.o: poppler-embedded-file.cpp
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/poppler-embedded-file.o poppler-embedded-file.cpp

${OBJECTDIR}/poppler-font.o: poppler-font.cpp
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/poppler-font.o poppler-font.cpp

${OBJECTDIR}/poppler-global.o: poppler-global.cpp
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/poppler-global.o poppler-global.cpp

${OBJECTDIR}/poppler-image.o: poppler-image.cpp
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/poppler-image.o poppler-image.cpp

${OBJECTDIR}/poppler-page-renderer.o: poppler-page-renderer.cpp
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/poppler-page-renderer.o poppler-page-renderer.cpp

${OBJECTDIR}/poppler-page-transition.o: poppler-page-transition.cpp
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/poppler-page-transition.o poppler-page-transition.cpp

${OBJECTDIR}/poppler-page.o: poppler-page.cpp
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/poppler-page.o poppler-page.cpp

${OBJECTDIR}/poppler-private.o: poppler-private.cpp
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/poppler-private.o poppler-private.cpp

${OBJECTDIR}/poppler-rectangle.o: poppler-rectangle.cpp
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/poppler-rectangle.o poppler-rectangle.cpp

${OBJECTDIR}/poppler-toc.o: poppler-toc.cpp
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/poppler-toc.o poppler-toc.cpp

${OBJECTDIR}/poppler-version.o: poppler-version.cpp
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/poppler-version.o poppler-version.cpp

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
