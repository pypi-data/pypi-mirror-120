#pragma once

#include "defs.h"

#ifndef __NVCC__
#include <Eigen/Dense>
#endif

namespace cuda {

struct Vec3f {
    float x, y, z;

    Vec3f() = default;
    __device__ Vec3f(float x_, float y_, float z_) : x(x_), y(y_), z(z_) {}

    __device__ static Vec3f Zero() { return {0, 0, 0}; }
    __device__ static Vec3f One() { return {1, 1, 1}; }

    __device__ static Vec3f UnitX() { return {1, 0, 0}; }
    __device__ static Vec3f UnitY() { return {0, 1, 0}; }
    __device__ static Vec3f UnitZ() { return {0, 0, 1}; }

    __device__ bool operator==(const Vec3f &o) const { return x == o.x && y == o.y && z == o.z; }
    __device__ bool operator!=(const Vec3f &o) const { return !(*this == o); }

    __device__ Vec3f operator+(const Vec3f &o) const { return {x + o.x, y + o.y, z + o.z}; }
    __device__ Vec3f &operator+=(const Vec3f &o) { return *this = *this + o; }

    __device__ Vec3f operator-(const Vec3f &o) const { return {x - o.x, y - o.y, z - o.z}; }
    __device__ Vec3f &operator-=(const Vec3f &o) { return *this = *this - o; }
    __device__ Vec3f operator-() const { return {-x, -y, -z}; }

    __device__ friend Vec3f operator*(float s, const Vec3f &v) { return v * s; }
    __device__ Vec3f operator*(float s) const { return {x * s, y * s, z * s}; }
    __device__ Vec3f &operator*=(float s) { return *this = *this * s; }

    __device__ friend Vec3f operator/(float s, const Vec3f &v) { return {s / v.x, s / v.y, s / v.z}; }
    __device__ Vec3f operator/(float s) const { return {x / s, y / s, z / s}; }
    __device__ Vec3f &operator/=(float s) { return *this = *this / s; }

    __device__ Vec3f cwiseProduct(const Vec3f &o) const { return {x * o.x, y * o.y, z * o.z}; }

    __device__ float dot(const Vec3f &o) const { return x * o.x + y * o.y + z * o.z; }

    __device__ Vec3f cross(const Vec3f &o) const { return {y * o.z - z * o.y, z * o.x - x * o.z, x * o.y - y * o.x}; }

    __device__ float squaredNorm() const { return x * x + y * y + z * z; }

    __device__ float norm() const { return sqrtf(squaredNorm()); }

    __device__ void normalize() {
        float norm_ = norm();
        if (!is_close(norm_, 0)) {
            *this /= norm_;
        }
    }

    __device__ Vec3f normalized() const {
        Vec3f out = *this;
        out.normalize();
        return out;
    }

    __device__ Vec3f clip(float minv, float maxv) const { return cwiseMax(minv).cwiseMin(maxv); }

    __device__ Vec3f cwiseMin(float v) const { return {fminf(x, v), fminf(y, v), fminf(z, v)}; }
    __device__ Vec3f cwiseMin(const Vec3f &o) const { return {fminf(x, o.x), fminf(y, o.y), fminf(z, o.z)}; }

    __device__ Vec3f cwiseMax(float v) const { return {fmaxf(x, v), fmaxf(y, v), fmaxf(z, v)}; }
    __device__ Vec3f cwiseMax(const Vec3f &o) const { return {fmaxf(x, o.x), fmaxf(y, o.y), fmaxf(z, o.z)}; }

#ifndef __NVCC__
    static Vec3f from_cpu(const Eigen::Vector3f &cpu_vec) { return {cpu_vec.x(), cpu_vec.y(), cpu_vec.z()}; }
#endif
};

struct Vec2f {
    float x;
    float y;

    Vec2f() = default;

    __device__ Vec2f(float x_, float y_) : x(x_), y(y_) {}

    __device__ static Vec2f Zero() { return {0, 0}; }

    __device__ static Vec2f One() { return {1, 1}; }
};

struct Vec3i {
    int x;
    int y;
    int z;

    Vec3i() = default;

    __device__ Vec3i(int x_, int y_, int z_) : x(x_), y(y_), z(z_) {}

    __device__ int operator[](size_t i) const { return (&x)[i]; }

    __device__ int &operator[](size_t i) { return (&x)[i]; }

#ifndef __NVCC__
    static Vec3i from_cpu(const Eigen::Vector3i &cpu_vec) { return {cpu_vec.x(), cpu_vec.y(), cpu_vec.z()}; }
#endif
};

struct Affine2f {
    float r00, r01, r10, r11;
    float tx, ty;

    __device__ Affine2f() : r00(1), r01(0), r10(0), r11(1), tx(0), ty(0) {}

    __device__ Affine2f(float r00_, float r01_, float r10_, float r11_, float tx_, float ty_)
        : r00(r00_), r01(r01_), r10(r10_), r11(r11_), tx(tx_), ty(ty_) {}

    __device__ Vec2f operator*(const Vec2f &uv) const {
        float u = uv.x, v = uv.y;
        return {r00 * u + r01 * v + tx, r10 * u + r11 * v + ty};
    }

#ifndef __NVCC__
    static Affine2f from_cpu(const Eigen::Affine2f &cpu_affine) {
        const auto &mat = cpu_affine.matrix();
        return {mat(0, 0), mat(0, 1), mat(1, 0), mat(1, 1), mat(0, 2), mat(1, 2)};
    }
#endif
};

} // namespace cuda