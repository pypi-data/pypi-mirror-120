#include "camera.h"
#include "path_tracer_impl.h"
#include "scene.h"

#include <Eigen/Dense>

namespace cpu {

typedef Eigen::Vector3f Vec3f;

struct CpuPathTracerImpl : public PathTracerImpl {
    Image render(const Scene *scene, const Camera &camera, int num_samples) const override;

  private:
    static Vec3f radiance(const Scene *scene, Ray ray, RandomGenerator &rand);

    static Vec3f clip(const Vec3f &v, float minv = 0, float maxv = 1) { return v.cwiseMax(minv).cwiseMin(maxv); }
};

} // namespace cpu