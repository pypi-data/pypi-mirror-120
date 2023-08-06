include_directories(${CMAKE_CURRENT_SOURCE_DIR})

add_subdirectory(cpu)

add_library(path_tracing INTERFACE)
target_link_libraries(path_tracing INTERFACE path_tracing_cpu)

if (PT_ENABLE_CUDA)
    add_subdirectory(cuda)
    target_link_libraries(path_tracing INTERFACE path_tracing_cuda)
endif ()

set(PT_ENABLE_PYBIND OFF CACHE BOOL "")
if (PT_ENABLE_PYBIND)
    set(EXTENSION_NAME _C)
    pybind11_add_module(${EXTENSION_NAME} pybind.cpp)
    target_link_libraries(${EXTENSION_NAME} PRIVATE path_tracing)
    # set RPATH to $ORIGIN to prevent import error
    # ref: https://github.com/pybind/cmake_example/issues/11
    set_target_properties(${EXTENSION_NAME} PROPERTIES BUILD_WITH_INSTALL_RPATH TRUE)
    set_target_properties(${EXTENSION_NAME} PROPERTIES INSTALL_RPATH "$ORIGIN/")
    set_target_properties(${EXTENSION_NAME} PROPERTIES INSTALL_RPATH_USE_LINK_PATH TRUE)
endif ()
