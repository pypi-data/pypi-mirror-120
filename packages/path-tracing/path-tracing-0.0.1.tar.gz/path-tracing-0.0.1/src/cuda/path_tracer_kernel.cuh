#pragma once

#include "camera.h"
#include "scene.h"

#include <cassert>

namespace cuda {

void path_tracer_kernel_launch(const Image &kernel_image, const Camera &camera, int num_samples, const Scene &scene);

} // namespace cuda
