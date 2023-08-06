#pragma once

#include "cpu/camera.h"
#include "cpu/image.h"
#include "cpu/scene.h"

struct PathTracerImpl {
    virtual ~PathTracerImpl() = default;

    virtual cpu::Image render(const cpu::Scene *scene, const cpu::Camera &camera, int num_samples) const = 0;
};
