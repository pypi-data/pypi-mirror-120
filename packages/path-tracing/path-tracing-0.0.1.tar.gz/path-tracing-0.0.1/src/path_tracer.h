#pragma once

#include "cpu/cpu_path_tracer_impl.h"
#ifdef PT_ENABLE_CUDA
#include "cuda/cuda_path_tracer_impl.h"
#endif

enum DeviceType { DEVICE_CPU, DEVICE_CUDA };

struct PathTracer {
    DeviceType device;
    std::unique_ptr<PathTracerImpl> impl;

    PathTracer(DeviceType device_ = DEVICE_CPU) : device(device_) {
        if (device_ == DEVICE_CPU) {
            impl = std::make_unique<cpu::CpuPathTracerImpl>();
        } else if (device_ == DEVICE_CUDA) {
#ifdef PT_ENABLE_CUDA
            impl = std::make_unique<cuda::CudaPathTracerImpl>();
#else
            throw std::runtime_error("CUDA is not enabled at compile time");
#endif
        } else {
            throw std::runtime_error("Unknown device");
        }
    }

    cpu::Image render(const cpu::Scene *scene, const cpu::Camera &camera, int num_samples) const {
        return impl->render(scene, camera, num_samples);
    }
};
