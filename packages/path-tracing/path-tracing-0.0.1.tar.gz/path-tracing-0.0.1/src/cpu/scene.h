#pragma once

#include "object.h"

namespace cpu {

typedef Eigen::Vector3f Vec3f;

struct Scene {
    std::vector<std::shared_ptr<Object>> objects;
    Vec3f background;

    Scene() : background(Vec3f::Zero()) {}
    Scene(std::vector<std::shared_ptr<Object>> objects_, Vec3f background_)
        : objects(std::move(objects_)), background(std::move(background_)) {}

    void intersect(const Ray &ray, Hit &hit) const {
        for (auto &obj : objects) {
            obj->intersect(ray, hit);
        }
    }
};

} // namespace cpu
