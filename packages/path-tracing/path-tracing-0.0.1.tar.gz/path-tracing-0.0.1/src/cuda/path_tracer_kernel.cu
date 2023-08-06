#include "path_tracer_kernel.cuh"

#include "camera.h"
#include "scene.h"

#include <algorithm>
#include <cstdio>

namespace cuda {

__device__ static Vec3f radiance(Ray ray, const Scene &scene, RandomGenerator &rand) {
    constexpr int MAX_DEPTH = 5;
    int depth = 0;
    Vec3f factor = Vec3f::One();
    Vec3f color = Vec3f::Zero();
    while (true) {
        assert(is_close(ray.dir.norm(), 1));
        Hit hit;
        scene.intersect(ray, hit);
        if (!hit.is_hit()) {
            color += factor.cwiseProduct(scene.background);
            break;
        }
        color += factor.cwiseProduct(hit.material->emit);
        if (depth >= MAX_DEPTH) {
            break;
        }
        Scatter scat = hit.material->scatter(ray, hit, rand);
        if (scat.color == Vec3f::Zero()) {
            break;
        }
        factor = factor.cwiseProduct(scat.color);
        ray = scat.ray;
        depth++;
    }
    return color;
}

static constexpr int BLOCK_SIZE = 32;

__global__ static void path_tracer_kernel(Image image, Camera camera, int num_samples, Scene scene) {
    //    if (blockIdx.x == 0 && blockIdx.y == 0 && threadIdx.x == 0) {
    //        for (int i = 0; i < meshes.size; i++) {
    //            auto &mesh = meshes[i];
    //            for (int k = 0; k < mesh.bvh.inner_nodes.size; k++) {
    //                auto &bbox = mesh.bvh.inner_nodes[k].bbox;
    //                printf("GLOBAL MIN (%f %f %f) MAX (%f %f %f)\n", bbox.minv.x, bbox.minv.y, bbox.minv.z,
    //                bbox.maxv.x,
    //                       bbox.maxv.y, bbox.maxv.z);
    //            }
    //            for (int k = 0; k < mesh.bvh.leaf_nodes.size; k++) {
    //                auto &bbox = mesh.bvh.leaf_nodes[k].bbox;
    //                printf("GLOBAL MIN (%f %f %f) MAX (%f %f %f)\n", bbox.minv.x, bbox.minv.y, bbox.minv.z,
    //                bbox.maxv.x,
    //                       bbox.maxv.y, bbox.maxv.z);
    //            }
    //        }
    //    }
    int x = (int)(blockIdx.x * BLOCK_SIZE + threadIdx.x);
    int y = (int)blockIdx.y;
    if (x >= camera.width) {
        return;
    }
    int idx = y * camera.width + x;

    num_samples /= 4;

    Vec3f color = Vec3f::Zero();

    RandomGenerator rand(idx);

    for (int sy = 0; sy < 2; sy++) {     // 2x2 subpixel rows
        for (int sx = 0; sx < 2; sx++) { // 2x2 subpixel cols
            Vec3f r = Vec3f::Zero();
            for (int s = 0; s < num_samples; s++) {
                float r1 = 2.f * rand.next();
                float dx = r1 < 1 ? sqrt(r1) - 1 : 1 - sqrt(2 - r1);
                float r2 = 2.f * rand.next();
                float dy = r2 < 1 ? sqrt(r2) - 1 : 1 - sqrt(2 - r2);
                Ray ray =
                    camera.shoot_ray(((float)sx - .5f + dx) / 2 + (float)x, ((float)sy - .5f + dy) / 2 + (float)y);
                r += radiance(ray, scene, rand);
            }
            color += (r / (float)num_samples).clip(0, 1);
        }
    }
    color /= 4;
    color = color.clip(0, 1);

    image.data[idx] = color;
}

static inline int ceil_div(int x, int y) { return (x + y - 1) / y; }

void path_tracer_kernel_launch(const Image &kernel_image, const Camera &camera, int num_samples, const Scene &scene) {
    dim3 grid_size(ceil_div(camera.width, BLOCK_SIZE), camera.height);
    path_tracer_kernel<<<grid_size, BLOCK_SIZE>>>(kernel_image, camera, num_samples, scene);
    CHECK_CUDA(cudaDeviceSynchronize());
}

} // namespace cuda
