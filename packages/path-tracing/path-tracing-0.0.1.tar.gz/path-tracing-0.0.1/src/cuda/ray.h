#pragma once

#include "vec.h"

namespace cuda {

struct Material;

struct Hit {
    float t;
    Vec3f normal;
    bool into;
    const Material *material;
    Vec2f uv;

    __device__ Hit() : t(INF), normal(Vec3f::Zero()), into(true), material(nullptr), uv(Vec2f::Zero()) {}

    __device__ Hit(float t_, const Vec3f &normal_, bool into_, const Material *material_, const Vec2f &uv_)
        : t(t_), normal(normal_), into(into_), material(material_), uv(uv_) {}

    __device__ bool is_hit() const { return t < INF; }
};

struct Ray {
    Vec3f org;
    Vec3f dir;

    Ray() = default;
    __device__ Ray(const Vec3f &org_, const Vec3f &dir_) : org(org_), dir(dir_) {}

    __device__ Vec3f point_at(float t) const { return org + dir * t; }

    __device__ Vec3f reflect(const Vec3f &hit_pos, const Vec3f &normal) const {
        Vec3f refl_dir = dir - 2 * normal.dot(dir) * normal;
        return refl_dir;
    }

    __device__ Vec3f refract(const Vec3f &hit_pos, const Vec3f &normal, float etai_over_etat, float cos_i,
                             float cos_t) const {
        Vec3f refr_dir = (etai_over_etat * dir + (etai_over_etat * cos_i - cos_t) * normal).normalized();
        return refr_dir;
    }
};

} // namespace cuda