#pragma once

#include <Eigen/Dense>
#include <memory>

namespace cpu {

typedef Eigen::Vector3f Vec3f;

struct Ray {
    Vec3f org; // origin
    Vec3f dir; // direction

    Ray() = default;

    Ray(Vec3f org_, Vec3f dir_) : org(std::move(org_)), dir(std::move(dir_)) {}

    Vec3f point_at(float t) const { return org + dir * t; }

    Vec3f reflect(const Vec3f &hit_pos, const Vec3f &normal) const {
        Vec3f refl_dir = dir - 2 * normal.dot(dir) * normal;
        return refl_dir;
    }

    Vec3f refract(const Vec3f &hit_pos, const Vec3f &normal, float etai_over_etat, float cos_i, float cos_t) const {
        Vec3f refr_dir = (etai_over_etat * dir + (etai_over_etat * cos_i - cos_t) * normal).normalized();
        return refr_dir;
    }
};

} // namespace cpu