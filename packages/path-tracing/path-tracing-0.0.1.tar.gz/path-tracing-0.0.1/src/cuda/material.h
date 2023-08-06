#pragma once

#include "defs.h"
#include "texture.h"

namespace cuda {

struct Scatter {
    Ray ray;
    Vec3f color;

    Scatter() = default;
    __device__ Scatter(const Ray &ray_, const Vec3f &color_) : ray(ray_), color(color_) {}
};

struct Material {
    enum Type { TYPE_DIFFUSIVE, TYPE_REFLECTIVE, TYPE_DIELECTRIC, TYPE_LIGHT };

    Type type;
    Vec3f emit;
    Texture texture;

    Material() = default;
    __device__ Material(Type type_, const Vec3f &emit_, const Texture &texture_)
        : type(type_), emit(emit_), texture(texture_) {}

#ifndef __NVCC__
    static Material from_cpu(const cpu::Material &cpu_material) {
        if (auto light = dynamic_cast<const cpu::Light *>(&cpu_material)) {
            return Material(TYPE_LIGHT, Vec3f::from_cpu(light->emit), {});
        } else if (auto diffusive = dynamic_cast<const cpu::Diffusive *>(&cpu_material)) {
            return Material(TYPE_DIFFUSIVE, Vec3f::Zero(), Texture::from_cpu(*diffusive->texture));
        } else if (auto reflective = dynamic_cast<const cpu::Reflective *>(&cpu_material)) {
            return Material(TYPE_REFLECTIVE, Vec3f::Zero(), Texture::from_cpu(*reflective->texture));
        } else if (auto dielectric = dynamic_cast<const cpu::Dielectric *>(&cpu_material)) {
            return Material(TYPE_DIELECTRIC, Vec3f::Zero(), Texture::from_cpu(*dielectric->texture));
        } else {
            throw std::runtime_error("Unknown material");
        }
    }
#else
    __device__ Scatter scatter(const Ray &ray, const Hit &hit, RandomGenerator &rand) const {
        if (type == TYPE_LIGHT) {
            return light_scatter(ray);
        } else if (type == TYPE_DIFFUSIVE) {
            return diffusive_scatter(ray, hit, rand);
        } else if (type == TYPE_REFLECTIVE) {
            return reflective_scatter(ray, hit, rand);
        } else {
            assert(type == TYPE_DIELECTRIC);
            return dielectric_scatter(ray, hit, rand);
        }
    }

    __device__ Scatter light_scatter(const Ray &ray) const { return Scatter(ray, Vec3f::Zero()); }

    __device__ Scatter diffusive_scatter(const Ray &ray, const Hit &hit, RandomGenerator &rand) const {
        Vec3f hit_pos = ray.point_at(hit.t);

        float phi = 2.f * M_PIf32 * rand.next();
        float sin2_theta = rand.next();
        float sin_theta = sqrtf(sin2_theta);
        float cos_theta = sqrtf(1 - sin2_theta);
        Vec3f w = hit.normal;
        Vec3f u = (std::abs(w.x) > .5f ? Vec3f::UnitY() : Vec3f::UnitX()).cross(w).normalized();
        Vec3f v = w.cross(u);
        Vec3f diff_dir = u * std::cos(phi) * sin_theta + v * std::sin(phi) * sin_theta + w * cos_theta;
        assert(is_close(diff_dir.norm(), 1));
        Ray diff_ray(hit_pos, diff_dir);
        Vec3f color = texture.color_at(hit.uv);
        Scatter scat(diff_ray, color);
        return scat;
    }

    __device__ Scatter reflective_scatter(const Ray &ray, const Hit &hit, RandomGenerator &rand) const {
        Vec3f hit_pos = ray.point_at(hit.t);
        Vec3f refl_dir = ray.reflect(hit_pos, hit.normal);
        assert(is_close(refl_dir.norm(), 1));
        Ray refl_ray(hit_pos, refl_dir);
        Vec3f color = texture.color_at(hit.uv);
        Scatter scat(refl_ray, color);
        return scat;
    }

    __device__ Scatter dielectric_scatter(const Ray &ray, const Hit &hit, RandomGenerator &rand) const {
        Vec3f hit_pos = ray.point_at(hit.t);
        Vec3f refl_dir = ray.reflect(hit_pos, hit.normal);
        assert(ray.dir.dot(hit.normal) <= 0);
        assert(is_close(refl_dir.norm(), 1));
        float nc = 1, ng = 1.5;                       // refraction index: vacuum = 1, glass = 1.5
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
        Vec3f color = texture.color_at(hit.uv);
        return Scatter(scat_ray, color);
    }
#endif
};

} // namespace cuda