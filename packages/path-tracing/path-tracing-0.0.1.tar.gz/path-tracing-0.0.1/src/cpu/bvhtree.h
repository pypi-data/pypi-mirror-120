#pragma once

#include "defs.h"
#include "hit.h"
#include "ray.h"

#include <Eigen/Dense>
#include <memory>
#include <vector>

namespace cpu {

typedef Eigen::Vector3f Vec3f;
typedef Eigen::Vector3i Vec3i;

// Axis-Aligned Bounding Box
struct AABB {
    Vec3f minv;
    Vec3f maxv;

    AABB() = default;

    AABB(Vec3f minv_, Vec3f maxv_) : minv(std::move(minv_)), maxv(std::move(maxv_)) {}

    float intersect(const Ray &ray) const {
        Vec3f inv_dir(inverse(ray.dir.x()), inverse(ray.dir.y()), inverse(ray.dir.z()));

        Vec3f tmins = (minv - ray.org).cwiseProduct(inv_dir);
        Vec3f tmaxs = (maxv - ray.org).cwiseProduct(inv_dir);

        float tmin = tmins.x();
        float tmax = tmaxs.x();
        if (tmin > tmax) {
            std::swap(tmin, tmax);
        }

        float tymin = tmins.y();
        float tymax = tmaxs.y();
        if (tymin > tymax) {
            std::swap(tymin, tymax);
        }

        if (tmin > tymax || tymin > tmax) {
            return INF;
        }

        tmin = std::max(tmin, tymin);
        tmax = std::min(tmax, tymax);

        float tzmin = tmins.z();
        float tzmax = tmaxs.z();
        if (tzmin > tzmax) {
            std::swap(tzmin, tzmax);
        }

        if (tmin > tzmax || tzmin > tmax) {
            return INF;
        }

        tmin = std::max(tmin, tzmin);
        if (tmin < EPS) {
            return INF;
        }

        return tmin;
    }

  private:
    static float inverse(float x) { return std::abs(x) < (1.f / INF) ? INF : 1.f / x; }
};

struct BVHNode {
    // data
    AABB bbox;
    std::vector<int> facet_indices;
    // children
    std::unique_ptr<BVHNode> left;
    std::unique_ptr<BVHNode> right;

    bool is_leaf() const { return left == nullptr && right == nullptr; }
};

struct BVHTree {
    static constexpr int MAX_FACETS_PER_NODE = 16;

    std::unique_ptr<BVHNode> root;
    int height;

    BVHTree() = default;

    BVHTree(const std::vector<Vec3f> &vertices, const std::vector<Vec3i> &facets) {
        std::vector<int> facet_indices(facets.size());
        for (int i = 0; i < (int)facet_indices.size(); i++) {
            facet_indices[i] = i;
        }
        height = 1;
        while ((MAX_FACETS_PER_NODE << (height - 1)) < (int)facets.size()) {
            height++;
        }
        root = std::make_unique<BVHNode>();
        build_tree(vertices, facets, root.get(), facet_indices, 0, facet_indices.size(), 0);
    }

    bool empty() const { return root == nullptr; }

    void print() const { print_tree(root.get(), 0); }

  private:
    void build_tree(const std::vector<Vec3f> &vertices, const std::vector<Vec3i> &facets, BVHNode *node,
                    std::vector<int> &facet_indices, int lo, int hi, int depth) const {
        depth++;
        node->bbox = get_bbox(vertices, facets, facet_indices, lo, hi);
        if (depth >= height) {
            node->facet_indices.assign(facet_indices.begin() + lo, facet_indices.begin() + hi);
            return;
        }

        // Split the axis with the largest range
        Vec3f axis_range = node->bbox.maxv - node->bbox.minv;
        int axis = (axis_range.x() > axis_range.y()) ? ((axis_range.x() > axis_range.z()) ? 0 : 2)
                                                     : ((axis_range.y() > axis_range.z()) ? 1 : 2);
        auto cmp_less = [&](int fia, int fib) {
            auto &fa = facets[fia];
            auto &fb = facets[fib];
            auto &vax = vertices[fa.x()], &vay = vertices[fa.y()], &vaz = vertices[fa.z()];
            auto &vbx = vertices[fb.x()], &vby = vertices[fb.y()], &vbz = vertices[fb.z()];
            return std::min({vax[axis], vay[axis], vaz[axis]}) < std::min({vbx[axis], vby[axis], vbz[axis]});
        };
        int mid = (lo + hi) / 2;
        std::nth_element(facet_indices.begin() + lo, facet_indices.begin() + mid, facet_indices.begin() + hi, cmp_less);

        // Build children nodes recursively
        node->left = std::make_unique<BVHNode>();
        build_tree(vertices, facets, node->left.get(), facet_indices, lo, mid, depth);
        node->right = std::make_unique<BVHNode>();
        build_tree(vertices, facets, node->right.get(), facet_indices, mid, hi, depth);
    }

    static AABB get_bbox(const std::vector<Vec3f> &vertices, const std::vector<Vec3i> &facets,
                         const std::vector<int> &facet_indices, int lo, int hi) {
        Vec3f minv(INF, INF, INF);
        Vec3f maxv(-INF, -INF, -INF);
        for (auto fi = facet_indices.begin() + lo; fi != facet_indices.begin() + hi; fi++) {
            auto &facet = facets[*fi];
            minv = minv.cwiseMin(vertices[facet.x()]);
            maxv = maxv.cwiseMax(vertices[facet.x()]);
            minv = minv.cwiseMin(vertices[facet.y()]);
            maxv = maxv.cwiseMax(vertices[facet.y()]);
            minv = minv.cwiseMin(vertices[facet.z()]);
            maxv = maxv.cwiseMax(vertices[facet.z()]);
        }
        AABB bbox(std::move(minv), std::move(maxv));
        return bbox;
    }

    static void print_tree(const BVHNode *node, int offset) {
        if (!node) {
            return;
        }
        // print left child
        print_tree(node->left.get(), offset + 2);
        // print self
        printf("%*s", offset, "");
        if (node->is_leaf()) {
            printf("%d\n", (int)node->facet_indices.size());
        } else {
            printf("N\n");
        }
        // print right child
        print_tree(node->right.get(), offset + 2);
    }
};

} // namespace cpu
