#pragma once

#include "defs.h"

#ifndef __NVCC__
#include <vector>
#endif

namespace cuda {

template <typename T>
struct Array {
    T *data;
    int size;

    __device__ Array() : data(nullptr), size(0) {}

    __device__ const T &operator[](int idx) const { return data[idx]; }

    __device__ T &operator[](int idx) { return data[idx]; }

#ifndef __NVCC__
    void create(const std::vector<T> &cpu_array) {
        if (data) {
            CHECK_CUDA(cudaFree(data));
        }
        CHECK_CUDA(cudaMalloc(&data, sizeof(T) * cpu_array.size()));
        CHECK_CUDA(cudaMemcpy(data, cpu_array.data(), sizeof(T) * cpu_array.size(), cudaMemcpyHostToDevice));
        size = cpu_array.size();
    }

    void destroy() {
        if (data) {
            CHECK_CUDA(cudaFree(data));
            data = nullptr;
            size = 0;
        }
    }
#endif
};

} // namespace cuda