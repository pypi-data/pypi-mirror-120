#pragma once

#include "path_tracer_impl.h"

namespace cuda {

struct CudaPathTracerImpl : public PathTracerImpl {
    cpu::Image render(const cpu::Scene *cpu_scene, const cpu::Camera &camera, int num_samples) const override;
};

} // namespace cuda