#pragma once

#include "array.h"
#include "object.h"

namespace cuda {

struct Scene {
    Vec3f background;

    Array<Sphere> spheres;
    Array<Plane> planes;
    Array<Circle> circles;
    Array<Mesh> meshes;
    Array<RectXY> rect_xys;
    Array<RectYZ> rect_yzs;
    Array<RectXZ> rect_xzs;

#ifndef __NVCC__
    void create(const cpu::Scene &cpu_scene) {
        std::vector<Sphere> host_spheres;
        std::vector<Plane> host_planes;
        std::vector<Circle> host_circles;
        std::vector<Mesh> host_meshes;
        std::vector<RectXY> host_rect_xys;
        std::vector<RectYZ> host_rect_yzs;
        std::vector<RectXZ> host_rect_xzs;
        for (const auto &obj : cpu_scene.objects) {
            if (const auto cpu_sphere = dynamic_cast<cpu::Sphere *>(obj.get())) {
                host_spheres.emplace_back(Sphere::from_cpu(*cpu_sphere));
            } else if (const auto cpu_plane = dynamic_cast<cpu::Plane *>(obj.get())) {
                host_planes.emplace_back(Plane::from_cpu(*cpu_plane));
            } else if (const auto cpu_circle = dynamic_cast<cpu::Circle *>(obj.get())) {
                host_circles.emplace_back(Circle::from_cpu(*cpu_circle));
            } else if (const auto cpu_mesh = dynamic_cast<cpu::Mesh *>(obj.get())) {
                Mesh mesh;
                mesh.create(*cpu_mesh);
                host_meshes.emplace_back(mesh);
            } else if (const auto cpu_rect_xy = dynamic_cast<cpu::RectXY *>(obj.get())) {
                host_rect_xys.emplace_back(RectXY::from_cpu(*cpu_rect_xy));
            } else if (const auto cpu_rect_yz = dynamic_cast<cpu::RectYZ *>(obj.get())) {
                host_rect_yzs.emplace_back(RectYZ::from_cpu(*cpu_rect_yz));
            } else if (const auto cpu_rect_xz = dynamic_cast<cpu::RectXZ *>(obj.get())) {
                host_rect_xzs.emplace_back(RectXZ::from_cpu(*cpu_rect_xz));
            } else {
                throw std::runtime_error("Unknown object");
            }
        }

        background = Vec3f::from_cpu(cpu_scene.background);
        spheres.create(host_spheres);
        planes.create(host_planes);
        circles.create(host_circles);
        meshes.create(host_meshes);
        rect_xys.create(host_rect_xys);
        rect_yzs.create(host_rect_yzs);
        rect_xzs.create(host_rect_xzs);
    }

    void destroy() {
        std::vector<Mesh> host_meshes(meshes.size);
        CHECK_CUDA(cudaMemcpy(host_meshes.data(), meshes.data, sizeof(Mesh) * meshes.size, cudaMemcpyDeviceToHost));
        for (auto &host_mesh : host_meshes) {
            host_mesh.destroy();
        }
        spheres.destroy();
        planes.destroy();
        circles.destroy();
        meshes.destroy();
        rect_xys.destroy();
        rect_yzs.destroy();
        rect_xzs.destroy();
    }
#endif

    __device__ void intersect(const Ray &ray, Hit &hit) const {
        for (int i = 0; i < planes.size; i++) {
            planes[i].intersect(ray, hit);
        }
        for (int i = 0; i < spheres.size; i++) {
            spheres[i].intersect(ray, hit);
        }
        for (int i = 0; i < circles.size; i++) {
            circles[i].intersect(ray, hit);
        }
        for (int i = 0; i < meshes.size; i++) {
            meshes[i].intersect(ray, hit);
        }
        for (int i = 0; i < rect_xys.size; i++) {
            rect_xys[i].intersect(ray, hit);
        }
        for (int i = 0; i < rect_yzs.size; i++) {
            rect_yzs[i].intersect(ray, hit);
        }
        for (int i = 0; i < rect_xzs.size; i++) {
            rect_xzs[i].intersect(ray, hit);
        }
    }
};

} // namespace cuda