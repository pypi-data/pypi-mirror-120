cmake_minimum_required(VERSION 3.12)
project(PathTracing LANGUAGES CXX)

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib CACHE STRING "")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib CACHE STRING "")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin CACHE STRING "")

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g -Wall")

if (NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif ()

if (NOT DEFINED PT_ENABLE_CUDA)
    # PT_ENABLE_CUDA not specified: enable cuda if found
    find_package(CUDA)
    set(PT_ENABLE_CUDA ${CUDA_FOUND})
endif ()

if (PT_ENABLE_CUDA)
    enable_language(CUDA)
    find_package(CUDA REQUIRED)
    add_compile_definitions(PT_ENABLE_CUDA)
    set(CUDA_NVCC_FLAGS_DEBUG "${CUDA_NVCC_FLAGS_DEBUG} -g")
    set(CUDA_NVCC_FLAGS_RELEASE "${CUDA_NVCC_FLAGS_RELEASE} -DNDEBUG -O3 --use_fast_math")
endif ()

# OpenMP
find_package(OpenMP REQUIRED)

# Eigen
find_package(Eigen3 3.3 REQUIRED NO_MODULE)

# third-party libraries
include_directories(third_party)
add_subdirectory(third_party)

# sources
add_subdirectory(src)

set(PT_ENABLE_EXAMPLES ON CACHE BOOL "")
if (PT_ENABLE_EXAMPLES)
    include_directories(src)
    add_subdirectory(examples/cpp)
endif ()

# clang-format
set(SRC_DIR ${CMAKE_CURRENT_SOURCE_DIR}/src)
file(GLOB_RECURSE LIB_SRCS ${SRC_DIR}/*.cpp ${SRC_DIR}/*.h ${SRC_DIR}/*.cu ${SRC_DIR}/*.cuh)
set(EXAMPLE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/examples)
file(GLOB_RECURSE EXAMPLE_SRCS ${EXAMPLE_DIR}/*.cpp ${EXAMPLE_DIR}/*.h ${EXAMPLE_DIR}/*.cu ${EXAMPLE_DIR}/*.cuh)
add_custom_target(format COMMAND clang-format -i ${LIB_SRCS} ${EXAMPLE_SRCS})
