cuda_add_library(path_tracing_cuda SHARED
        path_tracer_kernel.cu cuda_path_tracer_impl.cpp)
target_link_libraries(path_tracing_cuda Eigen3::Eigen)
