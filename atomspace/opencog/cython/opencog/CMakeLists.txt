#
# Need to use -fno-strict-aliasing when compiling cython code, in order
# to avoid nasty compiler warnings about aliasing.  Cython explicitly
# performs aliasing, in order to emulate python object inheritance.
# See, for example,
# https://groups.google.com/forum/#!topic/cython-users/JV1-KvIUeIg
#
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fno-strict-aliasing")

MESSAGE(STATUS "Setting python RPATH to ${PYTHON_DEST}")
SET(CMAKE_SHARED_LINKER_FLAGS
	"${CMAKE_SHARED_LINKER_FLAGS} -Wl,-rpath -Wl,${PYTHON_DEST}")
SET(CMAKE_SHARED_LIBRARY_SUFFIX .so)
SET(CMAKE_INSTALL_RPATH
   "${CMAKE_INSTALL_PREFIX}/lib/opencog"
   "${PYTHON_DEST}")

# Search path for module load paths in load_scm_file_relative()
ADD_DEFINITIONS(
	-DCMAKE_INSTALL_PREFIX="\\"${CMAKE_INSTALL_PREFIX}\\""
)

INCLUDE_DIRECTORIES(
	${Python3_INCLUDE_DIRS}
	${CMAKE_CURRENT_SOURCE_DIR}
	${CMAKE_CURRENT_BINARY_DIR}
)

# SET(CYTHON_FLAGS "-3" "-f" "-Wextra" "-Werror")
SET(CYTHON_FLAGS "-3" "-f" "-Wextra")

###################### logger ##########################################
CYTHON_ADD_MODULE_PYX(logger)

ADD_LIBRARY(logger_cython
	logger.cpp
)

TARGET_LINK_LIBRARIES(logger_cython
	${COGUTIL_LIBRARY}
	${Python3_LIBRARIES}
)

# Python is expecting the shared object to be called `logger.so` and
# not `liblogger_something.so`
SET_TARGET_PROPERTIES(logger_cython PROPERTIES
	PREFIX ""
	OUTPUT_NAME logger)

###################### atomspace ####################################

CYTHON_ADD_MODULE_PYX(atomspace
	"atom.pyx" "nameserver.pyx" "truth_value.pyx"
	"atomspace_details.pyx" "value.pyx" "float_value.pyx" "string_value.pyx"
	"link_value.pyx" "queue_value.pyx" "uniset_value.pyx" "bool_value.pyx" opencog_atom_types
	"../../atoms/truthvalue/TruthValue.h" "../../atoms/truthvalue/SimpleTruthValue.h"
	"../../atoms/atom_types/NameServer.h" "../../atoms/base/Handle.h"
	"../../atomspace/AtomSpace.h"
)

list(APPEND ADDITIONAL_MAKE_CLEAN_FILES "atomspace_api.h")

# opencog.atomspace Python bindings
ADD_LIBRARY(atomspace_cython
	ExecuteStub.cc
	atomspace.cpp
)

# The atomspace_api.h must be generated before PythonEval is compiled, thus
# this phony-target is created. Why not add_dependencies between PythonEval
# and atomspace_cython? -> Because that results in a cyclic dependency.
ADD_CUSTOM_TARGET(py_atomspace_header
	DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/atomspace.cpp)

# XXX FIXME Cython should not static link the atom-types, but
# but should instead dynamic-load them, as needed.
ADD_DEPENDENCIES(atomspace_cython opencog_atom_types)

TARGET_LINK_LIBRARIES(atomspace_cython
	${NO_AS_NEEDED}
	atomspace
	${Python3_LIBRARIES}
)

IF(HAVE_GUILE)
	TARGET_LINK_LIBRARIES(atomspace_cython smob)
ENDIF(HAVE_GUILE)

SET_TARGET_PROPERTIES(atomspace_cython PROPERTIES
	PREFIX ""
	OUTPUT_NAME atomspace)

# The cogserver needs the atomspace.pxd file to get the Handle, Atom and
# AtomSpace definitions during compilation. So this must be installed.
INSTALL (FILES
	__init__.py
	atomspace.pxd
	logger.pxd
	value_types.pxd
	DESTINATION "include/opencog/cython/opencog"
)

############################## type constructors #####################

CYTHON_ADD_MODULE_PYX(type_constructors
	"atomspace.pxd" opencog_atom_types
)

ADD_LIBRARY(type_constructors
	type_constructors.cpp
)

TARGET_LINK_LIBRARIES(type_constructors
	${NO_AS_NEEDED}
	atomspace
	${Python3_LIBRARIES}
)

SET_TARGET_PROPERTIES(type_constructors PROPERTIES
	PREFIX ""
	OUTPUT_NAME type_constructors)


############################## utilities #####################
# Temporarily disabled due to Cython 3.x duplicate symbol issue
# CYTHON_ADD_MODULE_PYX(utilities
# 	"atomspace.pxd" opencog_atom_types
# )

# ADD_LIBRARY(utilities_cython
# 	Utilities.cc
# 	utilities.cpp
# 	type_constructors.cpp
# )

# TARGET_LINK_LIBRARIES(utilities_cython
# 	PythonEval
# 	atomspace
# 	# type_constructors
# 	executioncontext
# 	${Python3_LIBRARIES}
# )

# SET_TARGET_PROPERTIES(utilities_cython PROPERTIES
# 	PREFIX ""
# 	OUTPUT_NAME utilities)

# INSTALL (TARGETS utilities_cython EXPORT AtomSpaceTargets
#    DESTINATION "lib${LIB_DIR_SUFFIX}/opencog"
# )

# INSTALL (FILES
# 	Utilities.h
# 	DESTINATION "include/opencog/cython/opencog"
# )

############################## execute module #####################

CYTHON_ADD_MODULE_PYX(execute
	"atomspace.pxd"
	opencog_atom_types
)

ADD_LIBRARY(exec_cython
	"execute.cpp"
)

TARGET_LINK_LIBRARIES(exec_cython
	atomspace_cython
	atomspace
	${Python3_LIBRARIES}
)

SET_TARGET_PROPERTIES(exec_cython PROPERTIES
	PREFIX ""
	OUTPUT_NAME execute)

### Install the modules ###
INSTALL(TARGETS
	atomspace_cython
	exec_cython
	logger_cython
	type_constructors
	# utilities_cython  # Disabled due to Cython 3.x issue
	DESTINATION "${PYTHON_DEST}")

# This custom target allows *only* the Python bindings to be installed;
# this is intended for use when installing into a python virtual env.
# Unfortunately, this is a crummy solution, and really install should
# be fixed so that everything goes into the virtualenv, including guile.
# But guile wants to go into ${GUILE_SITE_DIR} and not into
# $ENV{VIRTUAL_ENV}, which is what python wants. Argh. Its a mess.
ADD_CUSTOM_TARGET(PythonBindings DEPENDS
	atomspace_cython
	exec_cython
	logger_cython
	type_constructors
	# utilities_cython  # Disabled due to Cython 3.x issue
)

IF (HAVE_GUILE)
	############################## scheme wrapper #####################

	CYTHON_ADD_MODULE_PYX(scheme
		"load-file.h"
		"PyScheme.h"
		"atomspace.pxd"
		opencog_atom_types
	)

	ADD_LIBRARY(scheme
		load-file.cc
		PyScheme.cc
		scheme.cpp
	)

	TARGET_LINK_LIBRARIES(scheme
		atomspace_cython
		atomspace
		smob
		${Python3_LIBRARIES}
	)

	SET_TARGET_PROPERTIES(scheme PROPERTIES
		PREFIX ""
		OUTPUT_NAME scheme)

	INSTALL (TARGETS
		scheme
		DESTINATION "${PYTHON_DEST}")
ENDIF (HAVE_GUILE)

##################################################
# Tell python where to find modules.

INSTALL (FILES
	__init__.py
	DESTINATION "${PYTHON_DEST}")
