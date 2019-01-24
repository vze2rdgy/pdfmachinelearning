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
	${OBJECTDIR}/FixedPoint.o \
	${OBJECTDIR}/GooHash.o \
	${OBJECTDIR}/GooList.o \
	${OBJECTDIR}/GooString.o \
	${OBJECTDIR}/GooTimer.o \
	${OBJECTDIR}/ImgWriter.o \
	${OBJECTDIR}/JpegWriter.o \
	${OBJECTDIR}/NetPBMWriter.o \
	${OBJECTDIR}/PNGWriter.o \
	${OBJECTDIR}/TiffWriter.o \
	${OBJECTDIR}/gfile.o \
	${OBJECTDIR}/glibc.o \
	${OBJECTDIR}/glibc_strtok_r.o \
	${OBJECTDIR}/gmem.o \
	${OBJECTDIR}/gmempp.o \
	${OBJECTDIR}/grandom.o \
	${OBJECTDIR}/gstrtod.o


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
LDLIBSOPTIONS=

# Build Targets
.build-conf: ${BUILD_SUBPROJECTS}
	"${MAKE}"  -f nbproject/Makefile-${CND_CONF}.mk ../output/${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/libgoo.${CND_DLIB_EXT}

../output/${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/libgoo.${CND_DLIB_EXT}: ${OBJECTFILES}
	${MKDIR} -p ../output/${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}
	${LINK.cc} -o ../output/${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/libgoo.${CND_DLIB_EXT} ${OBJECTFILES} ${LDLIBSOPTIONS} -shared -fPIC

${OBJECTDIR}/FixedPoint.o: FixedPoint.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/FixedPoint.o FixedPoint.cc

${OBJECTDIR}/GooHash.o: GooHash.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/GooHash.o GooHash.cc

${OBJECTDIR}/GooList.o: GooList.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/GooList.o GooList.cc

${OBJECTDIR}/GooString.o: GooString.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/GooString.o GooString.cc

${OBJECTDIR}/GooTimer.o: GooTimer.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/GooTimer.o GooTimer.cc

${OBJECTDIR}/ImgWriter.o: ImgWriter.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/ImgWriter.o ImgWriter.cc

${OBJECTDIR}/JpegWriter.o: JpegWriter.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/JpegWriter.o JpegWriter.cc

${OBJECTDIR}/NetPBMWriter.o: NetPBMWriter.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/NetPBMWriter.o NetPBMWriter.cc

${OBJECTDIR}/PNGWriter.o: PNGWriter.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/PNGWriter.o PNGWriter.cc

${OBJECTDIR}/TiffWriter.o: TiffWriter.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/TiffWriter.o TiffWriter.cc

${OBJECTDIR}/gfile.o: gfile.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/gfile.o gfile.cc

${OBJECTDIR}/glibc.o: glibc.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/glibc.o glibc.cc

${OBJECTDIR}/glibc_strtok_r.o: glibc_strtok_r.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/glibc_strtok_r.o glibc_strtok_r.cc

${OBJECTDIR}/gmem.o: gmem.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/gmem.o gmem.cc

${OBJECTDIR}/gmempp.o: gmempp.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/gmempp.o gmempp.cc

${OBJECTDIR}/grandom.o: grandom.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/grandom.o grandom.cc

${OBJECTDIR}/gstrtod.o: gstrtod.cc
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -g -std=c++14 -fPIC  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/gstrtod.o gstrtod.cc

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
