#include "cuda_path_tracer_impl.h"

#include "path_tracer_kernel.cuh"

namespace cuda {

cpu::Image CudaPathTracerImpl::render(const cpu::Scene *cpu_scene, const cpu::Camera &cpu_camera,
                                      int num_samples) const {
    Camera camera = Camera::from_cpu(cpu_camera);

    Scene scene;
    scene.create(*cpu_scene);

    Image kernel_image;
    kernel_image.create(camera.width, camera.height);

    path_tracer_kernel_launch(kernel_image, camera, num_samples, scene);

    cpu::Image cpu_image = kernel_image.to_cpu(camera.width, camera.height);

    scene.destroy();

    kernel_image.destroy();

    return cpu_image;
}

} // namespace cuda
