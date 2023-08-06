#pragma once

#include "vec.h"

#ifndef __NVCC__
#include "cpu/texture.h"
#endif

#include <cassert>

namespace cuda {

struct Texture {
    enum Type { TYPE_SOLID_COLOR, TYPE_CHECKED, TYPE_IMAGE };
    Type type;

    struct {
        Vec3f color;
    } solid_color;

    struct {
        float period;
        Vec3f dark_color;
        Vec3f light_color;
    } checked;

    struct {
        cudaTextureObject_t obj;
        int width;
        int height;
        Affine2f uv_affine;
    } image;

    Texture() = default;
    Texture(Type type_) : type(type_) {}

#ifndef __NVCC__
    static Texture from_cpu(const cpu::Texture &cpu_tex) {
        if (auto cpu_solid_color = dynamic_cast<const cpu::SolidColorTexture *>(&cpu_tex)) {
            return solid_color_from_cpu(*cpu_solid_color);
        } else if (auto cpu_checked = dynamic_cast<const cpu::CheckedTexture *>(&cpu_tex)) {
            return checked_from_cpu(*cpu_checked);
        } else if (auto cpu_image = dynamic_cast<const cpu::ImageTexture *>(&cpu_tex)) {
            return image_from_cpu(*cpu_image);
        } else {
            throw std::runtime_error("Unknown texture");
        }
    }
#else
    __device__ Vec3f color_at(const Vec2f &uv) const {
        if (type == TYPE_SOLID_COLOR) {
            return solid_color_at();
        } else if (type == TYPE_CHECKED) {
            return checked_color_at(uv);
        } else {
            assert(type == TYPE_IMAGE);
            return image_color_at(uv);
        }
    }
#endif

    // ===== begin solid color texture =====

    static Texture make_solid_color(const Vec3f &color) {
        Texture texture(TYPE_SOLID_COLOR);
        texture.solid_color.color = color;
        return texture;
    }

#ifndef __NVCC__
    static Texture solid_color_from_cpu(const cpu::SolidColorTexture &cpu_tex) {
        return make_solid_color(Vec3f::from_cpu(cpu_tex.solid_color));
    }
#endif

    __device__ Vec3f solid_color_at() const { return solid_color.color; }

    // ===== begin checked texture =====

    static Texture make_checked(float period, const Vec3f &dark_color, const Vec3f &light_color) {
        Texture texture(TYPE_CHECKED);
        texture.checked = {
            .period = period,
            .dark_color = dark_color,
            .light_color = light_color,
        };
        return texture;
    };

#ifndef __NVCC__
    static Texture checked_from_cpu(const cpu::CheckedTexture &cpu_tex) {
        return make_checked(cpu_tex.period, Vec3f::from_cpu(cpu_tex.dark_color), Vec3f::from_cpu(cpu_tex.light_color));
    }
#endif

    __device__ Vec3f checked_color_at(const Vec2f &uv) const {
        float u = fractional(uv.x / checked.period);
        float v = fractional(uv.y / checked.period);
        if ((u > 0.5) ^ (v > 0.5)) {
            return checked.dark_color;
        } else {
            return checked.light_color;
        }
    }

    __device__ static float fractional(float x) { return x - floorf(x); }

    // ===== begin image texture =====

    static Texture make_image(cudaTextureObject_t obj, int width, int height, Affine2f uv_affine) {
        Texture texture(TYPE_IMAGE);
        texture.image = {.obj = obj, .width = width, .height = height, .uv_affine = uv_affine};
        return texture;
    };

#ifndef __NVCC__
    static Texture image_from_cpu(const cpu::ImageTexture &cpu_tex) {
        const auto &cpu_image = cpu_tex.image;
        std::vector<uchar4> cpu_buf;
        cpu_buf.reserve(cpu_image.width() * cpu_image.height());
        for (int y = 0; y < cpu_image.height(); y++) {
            for (int x = 0; x < cpu_image.width(); x++) {
                Eigen::Vector3f cpu_color = cpu_image.get_pixel(x, y);
                cpu_buf.push_back({(uint8_t)(cpu_color.x() * 255), (uint8_t)(cpu_color.y() * 255),
                                   (uint8_t)(cpu_color.z() * 255), 0});
            }
        }

        cudaArray_t cuda_buf;
        auto channel_desc = cudaCreateChannelDesc<uchar4>();
        CHECK_CUDA(cudaMallocArray(&cuda_buf, &channel_desc, cpu_image.width(), cpu_image.height()));
        CHECK_CUDA(cudaMemcpy2DToArray(cuda_buf, 0, 0, cpu_buf.data(), cpu_image.width() * sizeof(uchar4),
                                       cpu_image.width() * sizeof(uchar4), cpu_image.height(), cudaMemcpyHostToDevice));

        cudaResourceDesc res_desc{};
        res_desc.resType = cudaResourceTypeArray;
        res_desc.res.array.array = cuda_buf;

        cudaTextureDesc tex_desc{};
        tex_desc.readMode = cudaReadModeNormalizedFloat;
        tex_desc.normalizedCoords = true;

        cudaTextureObject_t tex_obj{};
        CHECK_CUDA(cudaCreateTextureObject(&tex_obj, &res_desc, &tex_desc, nullptr));

        Texture texture(TYPE_IMAGE);
        texture.image.obj = tex_obj;
        texture.image.width = cpu_image.width();
        texture.image.height = cpu_image.height();
        texture.image.uv_affine = Affine2f::from_cpu(cpu_tex.affine);

        return texture;
    }
#endif

#ifdef __NVCC__
    __device__ Vec3f image_color_at(const Vec2f &uv) const {
        Vec2f tex_uv = image.uv_affine * uv;
        auto texel = tex2D<float4>(image.obj, tex_uv.x, tex_uv.y);
        return {texel.x, texel.y, texel.z};
    }
#endif
};

} // namespace cuda