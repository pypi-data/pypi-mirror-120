#include "cpu_path_tracer_impl.h"

#include "timer.h"

namespace cpu {

Image CpuPathTracerImpl::render(const Scene *scene, const Camera &camera, int num_samples) const {
    num_samples /= 4;
    Image img(camera.width, camera.height);

    Timer timer;
    int timestamp = timer.timestamp();

#pragma omp parallel for schedule(dynamic, 1)
    for (int y = 0; y < camera.height; y++) {
        //        fprintf(stderr, "\rRendering (%d spp) %.2f%% %.3fs", num_samples * 4, 100. * (y + 1) / camera.height,
        //                timer.count_seconds());
        RandomGenerator rand(y, (timestamp >> 16) & 0xffff, timestamp & 0xffff);
        for (int x = 0; x < camera.width; x++) {
            Vec3f color = Vec3f::Zero();
            for (int sy = 0; sy < 2; sy++) {     // 2x2 subpixel rows
                for (int sx = 0; sx < 2; sx++) { // 2x2 subpixel cols
                    Vec3f r = Vec3f::Zero();
                    for (int s = 0; s < num_samples; s++) {
                        float r1 = 2.f * rand.next();
                        float dx = r1 < 1 ? std::sqrt(r1) - 1 : 1 - std::sqrt(2 - r1);
                        float r2 = 2.f * rand.next();
                        float dy = r2 < 1 ? std::sqrt(r2) - 1 : 1 - std::sqrt(2 - r2);
                        Ray ray = camera.shoot_ray(((float)sx - .5f + dx) / 2 + (float)x,
                                                   ((float)sy - .5f + dy) / 2 + (float)y, rand);
                        r += radiance(scene, ray, rand);
                    }
                    color += clip(r / num_samples);
                }
            }
            color /= 4;
            color = clip(color);
            img.set_pixel(x, y, color);
        }
    }
    //    fprintf(stderr, "\n");
    return img;
}

Vec3f CpuPathTracerImpl::radiance(const Scene *scene, Ray ray, RandomGenerator &rand) {
    constexpr int MAX_DEPTH = 5;
    int depth = 0;
    Vec3f factor = Vec3f::Ones();
    Vec3f color = Vec3f::Zero();
    while (true) {
        assert(is_close(ray.dir.norm(), 1));
        Hit hit;
        scene->intersect(ray, hit);
        if (!hit.is_hit()) {
            color += factor.cwiseProduct(scene->background);
            break;
        }
        color += factor.cwiseProduct(hit.material->emittance());
        if (depth >= MAX_DEPTH) {
            break;
        }
        Scatter scat = hit.material->scatter(ray, hit, rand);
        if (scat.color == Vec3f::Zero()) {
            break;
        }
        factor = factor.cwiseProduct(scat.color);
        ray = scat.ray;
        depth++;
    }
    return color;
}

} // namespace cpu