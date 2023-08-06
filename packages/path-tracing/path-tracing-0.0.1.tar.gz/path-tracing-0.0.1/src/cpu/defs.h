#pragma once

#include <cmath>

namespace cpu {

static constexpr float INF = 1e20;
static constexpr float EPS = 1e-3;

static inline float radians(float degrees) { return degrees * M_PIf32 / 180.f; }

static inline float degrees(float radians) { return radians * 180.f / M_PIf32; }

static inline float square(float x) { return x * x; }

static inline bool is_close(float x, float y) { return std::abs(x - y) < EPS; }

struct RandomGenerator {
    unsigned short seed[3];

    RandomGenerator(unsigned short x0, unsigned short x1, unsigned short x2) : seed{x0, x1, x2} {}

    float next() { return (float)erand48(seed); }
};

} // namespace cpu