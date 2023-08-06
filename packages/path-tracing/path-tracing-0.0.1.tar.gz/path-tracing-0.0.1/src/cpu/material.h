#pragma once

#include "image.h"
#include "texture.h"

#include <Eigen/Dense>

namespace cpu {

typedef Eigen::Vector3f Vec3f;

struct Scatter {
    Ray ray;
    Vec3f color;

    Scatter() = default;
    Scatter(Ray ray_, Vec3f color_) : ray(std::move(ray_)), color(std::move(color_)) {}
};

struct Material {
    virtual ~Material() = default;
    virtual Vec3f emittance() { return Vec3f::Zero(); }
    virtual Scatter scatter(const Ray &ray, const Hit &hit, RandomGenerator &rand) const = 0;
};

struct Diffusive : public Material {
    std::shared_ptr<Texture> texture;

    Diffusive() = default;
    Diffusive(std::shared_ptr<Texture> texture_) : texture(std::move(texture_)) {}
    Diffusive(Vec3f color_) : texture(std::make_unique<SolidColorTexture>(std::move(color_))) {}

    Scatter scatter(const Ray &ray, const Hit &hit, RandomGenerator &rand) const override {
        Vec3f hit_pos = ray.point_at(hit.t);

        float phi = 2.f * M_PIf32 * rand.next();
        float sin2_theta = rand.next();
        float sin_theta = std::sqrt(sin2_theta);
        float cos_theta = std::sqrt(1 - sin2_theta);
        Vec3f w = hit.normal;
        Vec3f u = (std::abs(w.x()) > .5f ? Vec3f::UnitY() : Vec3f::UnitX()).cross(w).normalized();
        Vec3f v = w.cross(u);
        Vec3f diff_dir = u * std::cos(phi) * sin_theta + v * std::sin(phi) * sin_theta + w * cos_theta;
        assert(is_close(diff_dir.norm(), 1));
        Ray diff_ray(hit_pos, diff_dir);
        Vec3f color = texture->color(hit.uv_pos.x(), hit.uv_pos.y());
        Scatter scat(diff_ray, color);
        return scat;
    }
};

struct Reflective : public Material {
    std::shared_ptr<Texture> texture;

    Reflective() = default;
    Reflective(std::shared_ptr<Texture> texture_) : texture(std::move(texture_)) {}
    Reflective(Vec3f color_) : texture(std::make_unique<SolidColorTexture>(std::move(color_))) {}

    Scatter scatter(const Ray &ray, const Hit &hit, RandomGenerator &rand) const override {
        Vec3f hit_pos = ray.point_at(hit.t);
        Vec3f refl_dir = ray.reflect(hit_pos, hit.normal);
        assert(is_close(refl_dir.norm(), 1));
        Ray refl_ray(hit_pos, refl_dir);
        Vec3f color = texture->color(hit.uv_pos.x(), hit.uv_pos.y());
        Scatter scat(refl_ray, color);
        return scat;
    }
};

struct Dielectric : public Material {
    std::shared_ptr<Texture> texture;

    Dielectric() = default;
    Dielectric(std::shared_ptr<Texture> texture_) : texture(std::move(texture_)) {}
    Dielectric(Vec3f color_) : texture(std::make_unique<SolidColorTexture>(std::move(color_))) {}

    Scatter scatter(const Ray &ray, const Hit &hit, RandomGenerator &rand) const override {
        Vec3f hit_pos = ray.point_at(hit.t);
        Vec3f refl_dir = ray.reflect(hit_pos, hit.normal);
        assert(ray.dir.dot(hit.normal) <= 0);
        assert(is_close(refl_dir.norm(), 1));
        constexpr float nc = 1, ng = 1.5;             // refraction index: vacuum = 1, glass = 1.5
        float eta = hit.into ? (nc / ng) : (ng / nc); // eta = n_incidence / n_transmission
        float cosi = -ray.dir.dot(hit.normal);
        float cos2t = 1 - eta * eta * (1 - cosi * cosi);
        Ray scat_ray;
        if (cos2t < 0) {
            // total internal reflection
            scat_ray = Ray(hit_pos, refl_dir);
        } else {
            float cost = std::sqrt(cos2t);
            Vec3f refr_dir = ray.refract(hit_pos, hit.normal, eta, cosi, cost);
            // Approximation of Fresnel effect
            // paper: An inexpensive BRDF model for physically‐based rendering
            float R0 = square(ng - nc) / square(ng + nc);
            float c = 1 - (hit.into ? cosi : cost);
            float Re = R0 + (1 - R0) * c * c * c * c * c;

            if (rand.next() < Re) {
                scat_ray = Ray(hit_pos, refl_dir);
            } else {
                scat_ray = Ray(hit_pos, refr_dir);
            }
        }
        Vec3f color = texture->color(hit.uv_pos.x(), hit.uv_pos.y());
        return Scatter(scat_ray, color);
    }
};

struct Light : public Material {
    Vec3f emit;

    Light() = default;
    Light(Vec3f emit_) : emit(std::move(emit_)) {}

    Vec3f emittance() override { return emit; }

    Scatter scatter(const Ray &ray, const Hit &hit, RandomGenerator &rand) const override {
        return Scatter(ray, Vec3f::Zero());
    }
};

} // namespace cpu
