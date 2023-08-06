add_library(path_tracing_cpu SHARED cpu_path_tracer_impl.cpp)
target_link_libraries(path_tracing_cpu
        tinyobjloader OpenMP::OpenMP_CXX Eigen3::Eigen)
