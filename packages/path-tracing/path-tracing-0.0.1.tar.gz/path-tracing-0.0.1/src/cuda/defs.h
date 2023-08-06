#pragma once

#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cuda_runtime.h>
#include <curand_kernel.h>

namespace cuda {

static inline void check_cuda_status(cudaError status, const char *file, int line) {
    if (status != cudaSuccess) {
        fprintf(stderr, "%s:%d: cuda error: %s\n", file, line, cudaGetErrorString(status));
        cudaDeviceReset();
        exit(EXIT_FAILURE);
    }
}

#define CHECK_CUDA(call) check_cuda_status((call), __FILE__, __LINE__)

static constexpr float INF = 1e20;
static constexpr float EPS = 1e-3;

__device__ static inline bool is_close(float x, float y) { return std::abs(x - y) < EPS; }

__device__ static inline float square(float x) { return x * x; }

template <typename T>
__device__ static inline void swap(T &a, T &b) {
    T tmp = a;
    a = b;
    b = tmp;
}

struct RandomGenerator {
    curandState state;

    __device__ RandomGenerator(uint64_t seed) { curand_init(seed, 0, 0, &state); }

    __device__ float next() { return curand_uniform(&state); }
};

} // namespace cuda