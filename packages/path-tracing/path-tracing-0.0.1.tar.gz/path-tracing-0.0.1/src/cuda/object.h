#pragma once

#include "array.h"
#include "material.h"
#include "ray.h"

#ifndef __NVCC__
#include "cpu/object.h"
#endif

#include <algorithm>
#include <cassert>
#include <cuda_runtime.h>
#include <queue>

namespace cuda {

struct Sphere {
    Vec3f center;
    float radius;
    Material material;

    __device__ Sphere(const Vec3f &center_, float radius_, Material material_)
        : center(center_), radius(radius_), material(material_) {}

    __device__ void intersect(const Ray &ray, Hit &hit) const {
        Vec3f op = center - ray.org;
        float b = op.dot(ray.dir);
        float det = b * b - op.dot(op) + radius * radius;
        if (det < 0) {
            return;
        }
        det = sqrtf(det);
        float t;
        bool into = true;
        if (b - det > EPS) {
            t = b - det;
        } else if (b + det > EPS) {
            t = b + det;
            into = false;
        } else {
            t = INF;
        }
        if (t < hit.t) {
            Vec3f hit_pos = ray.point_at(t);
            Vec3f normal = (hit_pos - center).normalized();
            float theta = acosf(normal.y);
            float phi = atan2f(normal.z, normal.x) + M_PIf32;
            Vec2f uv(phi, theta);
            if (!into) {
                normal = -normal;
            }
            hit = Hit(t, normal, into, &material, uv);
        }
    }

#ifndef __NVCC__
    static Sphere from_cpu(const cpu::Sphere &cpu_sphere) {
        Sphere sphere(Vec3f::from_cpu(cpu_sphere.center), cpu_sphere.radius, Material::from_cpu(*cpu_sphere.material));
        return sphere;
    }
#endif
};

struct RectXY {
    Vec3f minv;
    Vec3f maxv;
    Material material;

    RectXY() = default;

    __device__ RectXY(const Vec3f &a, const Vec3f &b, const Material &material_) : material(material_) {
        minv = a.cwiseMin(b);
        maxv = a.cwiseMax(b);
        assert(is_close(minv.z, maxv.z));
    }

    __device__ void intersect(const Ray &ray, Hit &hit) const {
        if (is_close(ray.dir.z, 0)) {
            return;
        }
        float t = (minv.z - ray.org.z) / ray.dir.z;
        if (EPS < t && t < hit.t) {
            auto pos = ray.point_at(t);
            if (!(minv.x <= pos.x && pos.x <= maxv.x && minv.y <= pos.y && pos.y <= maxv.y)) {
                return;
            }
            Vec3f normal = (ray.dir.z < 0) ? Vec3f(0, 0, 1) : Vec3f(0, 0, -1);
            float u = pos.x - minv.x;
            float v = pos.y - minv.y;
            hit = Hit(t, normal, true, &material, Vec2f(u, v));
        }
    }

#ifndef __NVCC__
    static RectXY from_cpu(const cpu::RectXY &cpu_rect_xy) {
        return RectXY(Vec3f::from_cpu(cpu_rect_xy.minv), Vec3f::from_cpu(cpu_rect_xy.maxv),
                      Material::from_cpu(*cpu_rect_xy.material));
    }
#endif
};

struct RectYZ {
    Vec3f minv;
    Vec3f maxv;
    Material material;

    RectYZ() = default;

    __device__ RectYZ(const Vec3f &a, const Vec3f &b, const Material &material_) : material(material_) {
        minv = a.cwiseMin(b);
        maxv = a.cwiseMax(b);
        assert(is_close(minv.x, maxv.x));
    }

    __device__ void intersect(const Ray &ray, Hit &hit) const {
        if (is_close(ray.dir.x, 0)) {
            return;
        }
        float t = (minv.x - ray.org.x) / ray.dir.x;
        if (EPS < t && t < hit.t) {
            auto pos = ray.point_at(t);
            if (!(minv.y <= pos.y && pos.y <= maxv.y && minv.z <= pos.z && pos.z <= maxv.z)) {
                return;
            }
            Vec3f normal = (ray.dir.x < 0) ? Vec3f(1, 0, 0) : Vec3f(-1, 0, 0);
            float u = pos.z - minv.z;
            float v = pos.y - minv.y;
            hit = Hit(t, normal, true, &material, Vec2f(u, v));
        }
    }

#ifndef __NVCC__
    static RectYZ from_cpu(const cpu::RectYZ &cpu_rect_yz) {
        return RectYZ(Vec3f::from_cpu(cpu_rect_yz.minv), Vec3f::from_cpu(cpu_rect_yz.maxv),
                      Material::from_cpu(*cpu_rect_yz.material));
    }
#endif
};

struct RectXZ {
    Vec3f minv;
    Vec3f maxv;
    Material material;

    RectXZ() = default;

    __device__ RectXZ(const Vec3f &a, const Vec3f &b, const Material &material_) : material(material_) {
        minv = a.cwiseMin(b);
        maxv = a.cwiseMax(b);
        assert(is_close(minv.y, maxv.y));
    }

    __device__ void intersect(const Ray &ray, Hit &hit) const {
        if (is_close(ray.dir.y, 0)) {
            return;
        }
        float t = (minv.y - ray.org.y) / ray.dir.y;
        if (EPS < t && t < hit.t) {
            auto pos = ray.point_at(t);
            if (!(minv.x <= pos.x && pos.x <= maxv.x && minv.z <= pos.z && pos.z <= maxv.z)) {
                return;
            }
            Vec3f normal = (ray.dir.y < 0) ? Vec3f(0, 1, 0) : Vec3f(0, -1, 0);
            float u = pos.x - minv.x;
            float v = pos.z - minv.z;
            hit = Hit(t, normal, true, &material, Vec2f(u, v));
        }
    }

#ifndef __NVCC__
    static RectXZ from_cpu(const cpu::RectXZ &cpu_rect_xz) {
        return RectXZ(Vec3f::from_cpu(cpu_rect_xz.minv), Vec3f::from_cpu(cpu_rect_xz.maxv),
                      Material::from_cpu(*cpu_rect_xz.material));
    }
#endif
};

struct Plane {
    // extrinsic params
    Vec3f normal;
    float dist;
    // surface coordinates
    Vec3f uv_org; // origin of surface coordinates
    Vec3f u_dir;  // u direction unit vector
    Vec3f v_dir;  // v direction unit vector
    // material
    Material material;

    __device__ Plane(const Vec3f &normal_, float dist_, const Vec3f &uv_org_, const Vec3f &u_dir_, const Vec3f &v_dir_,
                     Material material_)
        : normal(normal_), dist(dist_), uv_org(uv_org_), u_dir(u_dir_), v_dir(v_dir_), material(material_) {}

    __device__ static float intersect_plane(const Ray &ray, const Vec3f &normal, float dist) {
        assert(is_close(ray.dir.norm(), 1));
        float norm = ray.dir.dot(normal);
        if (is_close(norm, 0)) {
            return INF;
        }
        float t = (dist - ray.org.dot(normal)) / norm;
        if (t < EPS) {
            return INF;
        }
        return t;
    }

    __device__ void intersect(const Ray &ray, Hit &hit) const {
        float t = intersect_plane(ray, normal, dist);
        if (t < hit.t) {
            Vec3f hit_pos = ray.point_at(t);
            Vec3f surf_vec = hit_pos - uv_org;
            float u = surf_vec.dot(u_dir);
            float v = surf_vec.dot(v_dir);
            Vec3f hit_normal = (normal.dot(ray.dir) < 0) ? normal : -normal;
            hit = Hit(t, hit_normal, true, &material, {u, v});
        }
    }

#ifndef __NVCC__
    static Plane from_cpu(const cpu::Plane &cpu_plane) {
        Plane plane(Vec3f::from_cpu(cpu_plane.normal), cpu_plane.dist, Vec3f::from_cpu(cpu_plane.uv_origin),
                    Vec3f::from_cpu(cpu_plane.u_dir), Vec3f::from_cpu(cpu_plane.v_dir),
                    Material::from_cpu(*cpu_plane.material));
        return plane;
    }
#endif
};

struct Circle {
    Vec3f center;
    float radius2;
    Vec3f normal;
    float dist;
    Material material;

    __device__ Circle(const Vec3f &center_, float radius_, const Vec3f &normal_, const Material &material_) {
        center = center_;
        radius2 = radius_ * radius_;
        normal = normal_.normalized();
        dist = normal.dot(center);
        material = material_;
    }

    __device__ void intersect(const Ray &ray, Hit &hit) const {
        float t = Plane::intersect_plane(ray, normal, dist);
        if (t < INF) {
            Vec3f pos = ray.point_at(t);
            if ((pos - center).squaredNorm() > radius2) {
                t = INF;
            }
        }
        if (t < hit.t) {
            Vec3f hit_normal = (normal.dot(ray.dir) < 0) ? normal : -normal;
            hit = Hit(t, hit_normal, true, &material, Vec2f::Zero()); // TODO: support uv texture
        }
    }

#ifndef __NVCC__
    static Circle from_cpu(const cpu::Circle &cpu_circle) {
        Circle circle(Vec3f::from_cpu(cpu_circle.center), sqrt(cpu_circle.radius2), Vec3f::from_cpu(cpu_circle.normal),
                      Material::from_cpu(*cpu_circle.material));
        return circle;
    }
#endif
};

struct AABB {
    Vec3f minv;
    Vec3f maxv;

    AABB() = default;

    __device__ AABB(const Vec3f &minv_, const Vec3f &maxv_) : minv(minv_), maxv(maxv_) {}

    __device__ float intersect(const Ray &ray) const {
        Vec3f inv_dir(inverse(ray.dir.x), inverse(ray.dir.y), inverse(ray.dir.z));

        Vec3f tmins = (minv - ray.org).cwiseProduct(inv_dir);
        Vec3f tmaxs = (maxv - ray.org).cwiseProduct(inv_dir);

        float tmin = tmins.x;
        float tmax = tmaxs.x;
        if (tmin > tmax) {
            swap(tmin, tmax);
        }

        float tymin = tmins.y;
        float tymax = tmaxs.y;
        if (tymin > tymax) {
            swap(tymin, tymax);
        }

        if (tmin > tymax || tymin > tmax) {
            return INF;
        }

        tmin = fmaxf(tmin, tymin);
        tmax = fminf(tmax, tymax);

        float tzmin = tmins.z;
        float tzmax = tmaxs.z;
        if (tzmin > tzmax) {
            swap(tzmin, tzmax);
        }

        if (tmin > tzmax || tzmin > tmax) {
            return INF;
        }

        tmin = fmaxf(tmin, tzmin);
        if (tmin < EPS) {
            return INF;
        }

        return tmin;
    }

#ifndef __NVCC__
    static AABB from_cpu(const cpu::AABB &cpu_aabb) {
        return {Vec3f::from_cpu(cpu_aabb.minv), Vec3f::from_cpu(cpu_aabb.maxv)};
    }
#endif

  private:
    __device__ static float inverse(float x) { return std::abs(x) < (1.f / INF) ? INF : 1.f / x; }
};

struct BVHInnerNode {
    AABB bbox;
};

struct BVHLeafNode {
    static constexpr int MAX_FACETS = 16;

    AABB bbox;
    int facet_idxs[MAX_FACETS];
    int num_facets;
};

struct BVHTree {
    static constexpr int ROOT_ID = 1;

    Array<BVHInnerNode> inner_nodes;
    Array<BVHLeafNode> leaf_nodes;

    BVHTree() = default;

    __device__ static int left(int id) { return id * 2; }
    __device__ static int right(int id) { return id * 2 + 1; }
    __device__ static int parent(int id) { return id / 2; }

    __device__ bool is_leaf(int id) const { return id >= inner_nodes.size; }
    __device__ const BVHLeafNode *get_leaf_node(int id) const { return &leaf_nodes[id - inner_nodes.size]; }
    __device__ const BVHInnerNode *get_inner_node(int id) const { return &inner_nodes[id]; }

    __device__ const AABB &get_aabb(int id) const {
        if (is_leaf(id)) {
            return get_leaf_node(id)->bbox;
        } else {
            return get_inner_node(id)->bbox;
        }
    }

#ifndef __NVCC__
    void create(const cpu::BVHTree &cpu_bvh) {
        std::vector<BVHInnerNode> vec_inner_nodes(1 << (cpu_bvh.height - 1));
        std::vector<BVHLeafNode> vec_leaf_nodes(1 << (cpu_bvh.height - 1));

        std::queue<cpu::BVHNode *> q;
        q.push(cpu_bvh.root.get());
        int id = 1;
        while (!q.empty()) {
            const auto cpu_node = q.front();
            q.pop();
            if (!cpu_node->is_leaf()) {
                BVHInnerNode &node = vec_inner_nodes[id];
                node.bbox = AABB::from_cpu(cpu_node->bbox);
                q.push(cpu_node->left.get());
                q.push(cpu_node->right.get());
            } else {
                BVHLeafNode &node = vec_leaf_nodes[id - vec_inner_nodes.size()];
                node.bbox = AABB::from_cpu(cpu_node->bbox);
                node.num_facets = cpu_node->facet_indices.size();
                assert(node.num_facets <= BVHLeafNode::MAX_FACETS);
                std::copy(cpu_node->facet_indices.begin(), cpu_node->facet_indices.end(), node.facet_idxs);
            }
            id++;
        }
        assert(id == (1 << cpu_bvh.height));

        inner_nodes.create(vec_inner_nodes);
        leaf_nodes.create(vec_leaf_nodes);
    }

    void destroy() {
        inner_nodes.destroy();
        leaf_nodes.destroy();
    }
#endif
};

struct TriangleFace {
    Vec3i vi;
    Vec3f normal;

    TriangleFace() = default;
    TriangleFace(const Vec3i &vi_, const Vec3f &normal_) : vi(vi_), normal(normal_) {}
};

struct Mesh {
    Array<Vec3f> vertices;
    Array<TriangleFace> facets;
    BVHTree bvh;
    Material material;

    __device__ void intersect(const Ray &ray, Hit &hit) const {
        struct {
            int id;
            float tmin;
        } stk[20];
        int top = 0;

        int curr = BVHTree::ROOT_ID;
        float tmin = bvh.get_aabb(curr).intersect(ray);

        stk[top++] = {curr, tmin};
        while (top > 0) {
            top--;
            curr = stk[top].id;
            tmin = stk[top].tmin;
            if (hit.t <= tmin) {
                continue;
            }

            while (!bvh.is_leaf(curr)) {
                int left = BVHTree::left(curr);
                int right = BVHTree::right(curr);
                float tmin_left = bvh.get_aabb(left).intersect(ray);
                float tmin_right = bvh.get_aabb(right).intersect(ray);
                if (tmin_left > tmin_right) {
                    swap(left, right);
                    swap(tmin_left, tmin_right);
                }
                if (tmin_right < hit.t) {
                    curr = left;
                    stk[top++] = {right, tmin_right};
                } else if (tmin_left < hit.t) {
                    curr = left;
                } else {
                    curr = 0;
                    break;
                }
            }

            if (curr > 0) {
                const BVHLeafNode *node = bvh.get_leaf_node(curr);
                for (int i = 0; i < node->num_facets; i++) {
                    int fi = node->facet_idxs[i];
                    auto &facet = facets[fi];
                    auto &a = vertices[facet.vi.x];
                    auto &b = vertices[facet.vi.y];
                    auto &c = vertices[facet.vi.z];
                    float t = intersect_triangle(ray, a, b, c);
                    if (t < hit.t) {
                        //                        Vec3f normal;
                        //                        // normal vector
                        //                        if (facet.vn.x >= 0) {
                        //                            normal = (vertex_normals[facet.vn.x] * (1 - u - v) +
                        //                                      vertex_normals[facet.vn.y] * u +
                        //                                      vertex_normals[facet.vn.z] * v)
                        //                                    .normalized();
                        //                        } else {
                        //                            normal = facet.normal;
                        //                        }
                        Vec3f normal = facet.normal;
                        bool into = normal.dot(ray.dir) < 0;
                        if (!into) {
                            normal = -normal;
                        }
                        hit = Hit(t, normal, into, &material, Vec2f::Zero()); // TODO support uv texture
                    }
                }
            }
        }
    }

    __device__ static float intersect_triangle(const Ray &ray, const Vec3f &a, const Vec3f &b, const Vec3f &c) {
        Vec3f ab = b - a;
        Vec3f ac = c - a;
        Vec3f p = ray.dir.cross(ac);

        float det = p.dot(ab);
        if (is_close(det, 0)) {
            return INF;
        }
        float inv_det = 1.f / det;

        Vec3f ao = ray.org - a;
        float u = p.dot(ao) * inv_det;
        if (u < 0 || 1 < u) {
            return INF;
        }

        Vec3f q = ao.cross(ab);
        float v = q.dot(ray.dir) * inv_det;
        if (v < 0 || 1 < u + v) {
            return INF;
        }

        float t = q.dot(ac) * inv_det;
        if (t < EPS) {
            return INF;
        }

        return t;
    }

#ifndef __NVCC__
    void create(const cpu::Mesh &cpu_mesh) {
        material = Material::from_cpu(*cpu_mesh.material);

        std::vector<Vec3f> vec_vertices;
        vec_vertices.reserve(cpu_mesh.vertices.size());
        for (auto &cpu_vertex : cpu_mesh.vertices) {
            vec_vertices.emplace_back(Vec3f::from_cpu(cpu_vertex));
        }
        vertices.create(vec_vertices);

        std::vector<TriangleFace> vec_facets;
        vec_facets.reserve(cpu_mesh.facets.size());
        for (auto &cpu_facet : cpu_mesh.facets) {
            vec_facets.emplace_back(Vec3i::from_cpu(cpu_facet.vi), Vec3f::from_cpu(cpu_facet.normal));
        }
        facets.create(vec_facets);

        assert(!cpu_mesh.bvh.empty());
        bvh.create(cpu_mesh.bvh);
    }

    void destroy() {
        vertices.destroy();
        facets.destroy();
        bvh.destroy();
    }
#endif
};

} // namespace cuda