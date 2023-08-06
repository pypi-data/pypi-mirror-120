#pragma once

#include "ray.h"
#include "vec.h"

#ifndef __NVCC__
#include "cpu/image.h"
#endif

namespace cuda {

struct Image {
    Vec3f *data;

    __device__ Image() : data(nullptr) {}

#ifndef __NVCC__
    void create(int width, int height) { CHECK_CUDA(cudaMalloc(&data, sizeof(Vec3f) * width * height)); }

    void destroy() {
        CHECK_CUDA(cudaFree(data));
        data = nullptr;
    }

    cpu::Image to_cpu(int width, int height) const {
        cpu::Image cpu_image(width, height);
        CHECK_CUDA(cudaMemcpy(cpu_image.data(), data, sizeof(Vec3f) * width * height, cudaMemcpyDeviceToHost));
        return cpu_image;
    }
#endif
};

struct Camera {
    // Extrinsic parameters
    Vec3f center;
    Vec3f direct;
    Vec3f up;
    Vec3f right;
    // Image size
    int width;
    int height;
    // Lens parameters for Depth of Field (DOF)
    float aperture;
    float focal_dist;

    __device__ Ray shoot_ray(float x, float y) const {
        Vec3f dir = (x / (float)width - .5f) * right + (y / (float)height - .5f) * up + direct;
        Ray ray(center, dir.normalized());
        //        if (aperture > 0) {
        //            // Perform depth of field
        //            Vec3f hit_pos = ray.point_at(focal_dist / ray.dir.dot(direct));
        //            float theta = 2.f * M_PIf32 * rand.next();
        //            float radius = rand.next() * aperture;
        //            ray.org += (std::cos(theta) * right + std::sin(theta) * up) * radius;
        //            ray.dir = (hit_pos - ray.org).normalized();
        //        }
        return ray;
    }

#ifndef __NVCC__
    static Camera from_cpu(const cpu::Camera &cpu_camera) {
        Camera camera{};
        camera.center = Vec3f::from_cpu(cpu_camera.center);
        camera.direct = Vec3f::from_cpu(cpu_camera.direct);
        camera.up = Vec3f::from_cpu(cpu_camera.up);
        camera.right = Vec3f::from_cpu(cpu_camera.right);
        camera.width = cpu_camera.width;
        camera.height = cpu_camera.height;
        camera.aperture = cpu_camera.aperture;
        camera.focal_dist = cpu_camera.focal_dist;
        return camera;
    }
#endif
};

} // namespace cuda