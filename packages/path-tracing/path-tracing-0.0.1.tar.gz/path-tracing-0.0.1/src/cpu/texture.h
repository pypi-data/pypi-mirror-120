#pragma once

#include "image.h"

namespace cpu {

typedef Eigen::Vector3f Vec3f;
typedef Eigen::Vector2f Vec2f;

struct Texture {
    virtual ~Texture() = default;
    virtual Vec3f color(float u, float v) const = 0;
};

struct SolidColorTexture : public Texture {
    Vec3f solid_color;

    SolidColorTexture() = default;
    SolidColorTexture(Vec3f color_) : solid_color(std::move(color_)) {}

    Vec3f color(float u, float v) const override { return solid_color; }
};

struct CheckedTexture : public Texture {
    float period;
    Vec3f dark_color;
    Vec3f light_color;

    CheckedTexture(float period_ = 64, Vec3f dark_color_ = Vec3f::Zero(), Vec3f light_color_ = Vec3f::Ones())
        : period(period_), dark_color(std::move(dark_color_)), light_color(std::move(light_color_)) {}

    Vec3f color(float u, float v) const override {
        u = fractional(u / period);
        v = fractional(v / period);
        if ((u > 0.5) ^ (v > 0.5)) {
            return dark_color;
        } else {
            return light_color;
        }
    }

    static float fractional(float x) { return x - std::floor(x); }
};

struct ImageTexture : public Texture {
    Image image;
    Eigen::Affine2f affine;

    ImageTexture() = default;
    ImageTexture(Image image_, const Eigen::Affine2f &affine_) : image(std::move(image_)), affine(affine_) {}

    Vec3f color(float u, float v) const override {
        Vec2f map_uv = affine * Vec2f(u, v);
        float iu = map_uv.x() - std::floor(map_uv.x());
        float iv = map_uv.y() - std::floor(map_uv.y());
        int x = (int)std::round(iu * (float)(image.width() - 1));
        int y = (int)std::round(iv * (float)(image.height() - 1));
        return image.get_pixel(x, y);
    }
};

} // namespace cpu