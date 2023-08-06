#pragma once

#include "defs.h"

#include <Eigen/Dense>
#include <memory>

namespace cpu {

typedef Eigen::Vector3f Vec3f;
typedef Eigen::Vector2f Vec2f;

struct Material;

struct Hit {
    float t;
    Vec3f normal;
    bool into; // is ray shooting into the object?
    Material *material;
    Vec2f uv_pos; // uv position on surface coordinates

    Hit() : t(INF), normal(Vec3f::Zero()), into(true), material(nullptr) {}

    Hit(float t_, Vec3f normal_, bool into_, Material *material_, Vec2f uv_pos_)
        : t(t_), normal(std::move(normal_)), into(into_), material(material_), uv_pos(std::move(uv_pos_)) {}

    bool is_hit() const { return t < INF; }
};

} // namespace cpu