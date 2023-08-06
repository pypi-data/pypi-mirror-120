#pragma once

#include "defs.h"
#include "ray.h"

#include <Eigen/Dense>

namespace cpu {

typedef Eigen::Vector3f Vec3f;

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

    Camera() = default;

    Camera(const Vec3f &center_, const Vec3f &direct_, const Vec3f &up_, int width_, int height_, float vfov_) {
        center = center_;
        float aspect_ratio = (float)width_ / (float)height_;
        float view_height = 2.f * std::tan(vfov_ * .5f);
        float view_width = aspect_ratio * view_height;
        direct = direct_.normalized();
        right = direct_.cross(up_).normalized() * view_width;
        up = right.cross(direct).normalized() * view_height;

        width = width_;
        height = height_;

        aperture = -1;
        focal_dist = -1;
    }

    void set_lens(float aperture_, float focal_dist_) {
        aperture = aperture_;
        focal_dist = focal_dist_;
    }

    Ray shoot_ray(float x, float y, RandomGenerator &rand) const {
        Vec3f dir = (x / (float)width - .5f) * right + (y / (float)height - .5f) * up + direct;
        Ray ray(center, dir.normalized());
        if (aperture > 0) {
            // Perform depth of field
            Vec3f hit_pos = ray.point_at(focal_dist / ray.dir.dot(direct));
            float theta = 2.f * M_PIf32 * rand.next();
            float radius = rand.next() * aperture;
            ray.org += (std::cos(theta) * right + std::sin(theta) * up) * radius;
            ray.dir = (hit_pos - ray.org).normalized();
        }
        return ray;
    }
};

} // namespace cpu
