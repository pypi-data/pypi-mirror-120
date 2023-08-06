#pragma once

#include "bvhtree.h"
#include "hit.h"
#include "material.h"
#include "ray.h"

#include <fstream>
#include <iostream>
#include <tinyobjloader/tiny_obj_loader.h>
#include <vector>

namespace cpu {

typedef Eigen::Vector3f Vec3f;
typedef Eigen::Vector3i Vec3i;
typedef Eigen::Vector2f Vec2f;

struct Object {
    std::shared_ptr<Material> material;

    Object() : material(nullptr) {}

    Object(std::shared_ptr<Material> material_) : material(std::move(material_)) {}

    virtual ~Object() = default;

    virtual void intersect(const Ray &ray, Hit &hit) const = 0;
};

struct Sphere : public Object {
    Vec3f center;
    float radius;

    Sphere() : center(Vec3f::Zero()), radius(1) {}

    Sphere(Vec3f center_, float radius_, std::shared_ptr<Material> material_)
        : Object(std::move(material_)), center(std::move(center_)), radius(radius_) {}

    void intersect(const Ray &ray, Hit &hit) const override {
        Vec3f op = center - ray.org; // Solve t^2*d.d + 2*t*(o-c).d + (o-c).(o-c)-R^2 = 0
        float b = op.dot(ray.dir);
        float det = b * b - op.dot(op) + radius * radius;
        if (det < 0) {
            return;
        }
        det = std::sqrt(det);
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
            float theta = std::acos(normal.y());
            float phi = std::atan2(normal.z(), normal.x()) + M_PIf32;
            if (!into) {
                normal = -normal;
            }
            hit = Hit(t, std::move(normal), into, material.get(), Vec2f(phi, theta));
        }
    }
};

struct RectXY : public Object {
    Vec3f minv;
    Vec3f maxv;

    RectXY(const Vec3f &a, const Vec3f &b, std::shared_ptr<Material> material_) : Object(std::move(material_)) {
        minv = a.cwiseMin(b);
        maxv = a.cwiseMax(b);
        assert(is_close(minv.z(), maxv.z()));
    }

    void intersect(const Ray &ray, Hit &hit) const override {
        if (is_close(ray.dir.z(), 0)) {
            return;
        }
        float t = (minv.z() - ray.org.z()) / ray.dir.z();
        if (EPS < t && t < hit.t) {
            auto pos = ray.point_at(t);
            if (!(minv.x() <= pos.x() && pos.x() <= maxv.x() && minv.y() <= pos.y() && pos.y() <= maxv.y())) {
                return;
            }
            Vec3f normal = (ray.dir.z() < 0) ? Vec3f(0, 0, 1) : Vec3f(0, 0, -1);
            float u = pos.x() - minv.x();
            float v = pos.y() - minv.y();
            hit = Hit(t, std::move(normal), true, material.get(), Vec2f(u, v));
        }
    }
};

struct RectYZ : public Object {
    Vec3f minv;
    Vec3f maxv;

    RectYZ(const Vec3f &a, const Vec3f &b, std::shared_ptr<Material> material_) : Object(std::move(material_)) {
        minv = a.cwiseMin(b);
        maxv = a.cwiseMax(b);
        assert(is_close(minv.x(), maxv.x()));
    }

    void intersect(const Ray &ray, Hit &hit) const override {
        if (is_close(ray.dir.x(), 0)) {
            return;
        }
        float t = (minv.x() - ray.org.x()) / ray.dir.x();
        if (EPS < t && t < hit.t) {
            auto pos = ray.point_at(t);
            if (!(minv.y() <= pos.y() && pos.y() <= maxv.y() && minv.z() <= pos.z() && pos.z() <= maxv.z())) {
                return;
            }
            Vec3f normal = (ray.dir.x() < 0) ? Vec3f(1, 0, 0) : Vec3f(-1, 0, 0);
            float u = pos.z() - minv.z();
            float v = pos.y() - minv.y();
            hit = Hit(t, std::move(normal), true, material.get(), Vec2f(u, v));
        }
    }
};

struct RectXZ : public Object {
    Vec3f minv;
    Vec3f maxv;

    RectXZ(const Vec3f &a, const Vec3f &b, std::shared_ptr<Material> material_) : Object(std::move(material_)) {
        minv = a.cwiseMin(b);
        maxv = a.cwiseMax(b);
        assert(is_close(minv.y(), maxv.y()));
    }

    void intersect(const Ray &ray, Hit &hit) const override {
        if (is_close(ray.dir.y(), 0)) {
            return;
        }
        float t = (minv.y() - ray.org.y()) / ray.dir.y();
        if (EPS < t && t < hit.t) {
            auto pos = ray.point_at(t);
            if (!(minv.x() <= pos.x() && pos.x() <= maxv.x() && minv.z() <= pos.z() && pos.z() <= maxv.z())) {
                return;
            }
            Vec3f normal = (ray.dir.y() < 0) ? Vec3f(0, 1, 0) : Vec3f(0, -1, 0);
            float u = pos.x() - minv.x();
            float v = pos.z() - minv.z();
            hit = Hit(t, std::move(normal), true, material.get(), Vec2f(u, v));
        }
    }
};

struct Plane : public Object {
    Vec3f normal;
    float dist;
    // surface coordinates
    Vec3f uv_origin; // origin of surface coordinates
    Vec3f u_dir;     // u direction unit vector
    Vec3f v_dir;     // v direction unit vector

    Plane() : normal(Vec3f::UnitZ()), dist(0) {}

    // Equation: ax + by + cz = d, or n.dot(x) = d, where n = (a,b,c)
    Plane(const Vec3f &normal_, float dist_, std::shared_ptr<Material> material_) : Object(std::move(material_)) {
        normal = normal_.normalized();
        dist = dist_;
        Vec3f vec = is_close(std::abs(normal.y()), 1) ? Vec3f::UnitZ() : Vec3f::UnitY();
        u_dir = normal.cross(vec).normalized();
        v_dir = normal.cross(u_dir);
        uv_origin = normal * dist;
    }

    void intersect(const Ray &ray, Hit &hit) const override {
        // solve (o + td).dot(n) = d
        float t = intersect_plane(ray, normal, dist);
        if (t < hit.t) {
            Vec3f hit_pos = ray.point_at(t);
            Vec3f surf_vec = hit_pos - uv_origin;
            float u = surf_vec.dot(u_dir);
            float v = surf_vec.dot(v_dir);
            Vec3f hit_normal = (normal.dot(ray.dir) < 0) ? normal : -normal;
            hit = Hit(t, std::move(hit_normal), true, material.get(), Vec2f(u, v));
        }
    }

    static float intersect_plane(const Ray &ray, const Vec3f &normal, float dist) {
        // solve: n.dot(o + td) = d
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
};

struct Circle : public Object {
    Vec3f center;
    float radius2;
    Vec3f normal;
    float dist;

    Circle(const Vec3f &center_, float radius_, const Vec3f &normal_, std::shared_ptr<Material> material_)
        : Object(std::move(material_)) {
        center = center_;
        radius2 = radius_ * radius_;
        normal = normal_.normalized();
        dist = normal.dot(center);
    }

    void intersect(const Ray &ray, Hit &hit) const override {
        float t = Plane::intersect_plane(ray, normal, dist);
        if (t < INF) {
            Vec3f pos = ray.point_at(t);
            if ((pos - center).squaredNorm() > radius2) {
                t = INF;
            }
        }
        if (t < hit.t) {
            Vec3f hit_normal = (normal.dot(ray.dir) < 0) ? normal : -normal;
            hit = Hit(t, std::move(hit_normal), true, material.get(), Vec2f::Zero()); // TODO: support uv texture
        }
    }
};

struct TriangleFace {
    Vec3i vi;
    Vec3i vn;
    Vec3f normal;
};

struct Mesh : public Object {
    std::vector<Vec3f> vertices;
    std::vector<TriangleFace> facets;
    std::vector<Vec3f> vertex_normals;
    BVHTree bvh;

    Mesh(const std::string &path_, std::shared_ptr<Material> material_) : Object(std::move(material_)) {
        tinyobj::ObjReaderConfig reader_config;
        reader_config.mtl_search_path = "./";

        tinyobj::ObjReader reader;

        if (!reader.ParseFromFile(path_, reader_config)) {
            if (!reader.Error().empty()) {
                fprintf(stderr, "TinyObjReader: %s\n", reader.Error().c_str());
            }
            throw std::runtime_error("Failed to parse obj file " + path_);
        }

        if (!reader.Warning().empty()) {
            std::cout << "TinyObjReader: " << reader.Warning() << std::endl;
        }

        auto &attrib = reader.GetAttrib();
        auto &shapes = reader.GetShapes();

        // build vertices
        assert(attrib.vertices.size() % 3 == 0);
        for (size_t i = 0; i < attrib.vertices.size(); i += 3) {
            vertices.emplace_back(attrib.vertices[i], attrib.vertices[i + 1], attrib.vertices[i + 2]);
        }

        // build vertex normals
        assert(attrib.normals.size() % 3 == 0);
        for (size_t i = 0; i < attrib.normals.size(); i += 3) {
            vertex_normals.emplace_back(attrib.normals[i], attrib.normals[i + 1], attrib.normals[i + 2]);
        }

        // build facets
        // loop over shapes
        for (auto &shape : shapes) {
            // loop over faces (polygon)
            size_t index_offset = 0;
            for (size_t f = 0; f < shape.mesh.num_face_vertices.size(); f++) {
                size_t fv = shape.mesh.num_face_vertices[f];
                assert(fv == 3);

                TriangleFace facet;
                Vec3i vertex_normal(-1, -1, -1);
                // loop over vertices in the face.
                for (size_t v = 0; v < fv; v++) {
                    // access to vertex
                    tinyobj::index_t idx = shape.mesh.indices[index_offset + v];
                    facet.vi[v] = idx.vertex_index;

                    // Check if `normal_index` is zero or positive. negative = no normal data
                    if (idx.normal_index >= 0) {
                        facet.vn[v] = idx.normal_index;
                    } else {
                        facet.vn[v] = -1;
                    }
                }
                facets.emplace_back(std::move(facet));
                index_offset += fv;
            }
        }

        // compute normal vectors
        for (auto &tri : facets) {
            auto &a = vertices[tri.vi.x()];
            auto &b = vertices[tri.vi.y()];
            auto &c = vertices[tri.vi.z()];
            tri.normal = (c - a).cross(b - a).normalized();
        }
        build_bvh();
    }

    void intersect(const Ray &ray, Hit &hit) const override {
        if (!bvh.empty()) {
            float t = bvh.root->bbox.intersect(ray);
            if (t < hit.t) {
                intersect_node(ray, bvh.root.get(), hit);
            }
        } else {
            for (const auto &facet : facets) {
                const auto &a = vertices[facet.vi.x()];
                const auto &b = vertices[facet.vi.y()];
                const auto &c = vertices[facet.vi.z()];
                intersect_triangle(ray, a, b, c);
                float t, u, v;
                std::tie(t, u, v) = intersect_triangle(ray, a, b, c);
                if (t < hit.t) {
                    hit = Hit(t, facet.normal, true, material.get(), Vec2f::Zero()); // TODO support uv texture
                }
            }
        }
    }

    void affine(const Eigen::Affine3f &trans) {
        for (auto &v : vertices) {
            v = trans * v;
        }
        build_bvh();
    }

    void build_bvh() {
        std::vector<Vec3i> vertex_indices;
        for (auto &tri : facets) {
            vertex_indices.emplace_back(tri.vi);
        }
        bvh = BVHTree(vertices, vertex_indices);
    }

    void print_bvh() const { bvh.print(); }

  private:
    void intersect_node(const Ray &ray, const BVHNode *node, Hit &hit) const {
        // at leaf node, intersect every facet
        if (node->is_leaf()) {
            for (int fi : node->facet_indices) {
                auto &facet = facets[fi];
                auto &a = vertices[facet.vi.x()];
                auto &b = vertices[facet.vi.y()];
                auto &c = vertices[facet.vi.z()];
                float t, u, v;
                std::tie(t, u, v) = intersect_triangle(ray, a, b, c);
                if (t < hit.t) {
                    Vec3f normal;
                    // normal vector
                    //                    if (facet.vn.x() >= 0) {
                    //                        normal = vertex_normals[facet.vn.x()] * (1 - u - v) +
                    //                        vertex_normals[facet.vn.y()] * u +
                    //                                 vertex_normals[facet.vn.z()] * v;
                    //                        normal.normalize();
                    //                    } else {
                    normal = facet.normal;
                    //                    }
                    bool into = normal.dot(ray.dir) < 0;
                    if (!into) {
                        normal = -normal;
                    }
                    hit = Hit(t, std::move(normal), into, material.get(), Vec2f::Zero()); // TODO support uv texture
                }
            }
            return;
        }

        float tmin_left = node->left->bbox.intersect(ray);
        float tmin_right = node->right->bbox.intersect(ray);
        if (tmin_left < tmin_right) {
            if (tmin_left < hit.t) {
                intersect_node(ray, node->left.get(), hit);
            }
            if (tmin_right < hit.t) {
                intersect_node(ray, node->right.get(), hit);
            }
        } else {
            if (tmin_right < hit.t) {
                intersect_node(ray, node->right.get(), hit);
            }
            if (tmin_left < hit.t) {
                intersect_node(ray, node->left.get(), hit);
            }
        }
    }

    static std::tuple<float, float, float> intersect_triangle(const Ray &ray, const Vec3f &a, const Vec3f &b,
                                                              const Vec3f &c) {
        Vec3f ab = b - a;
        Vec3f ac = c - a;
        Vec3f p = ray.dir.cross(ac);

        float det = p.dot(ab);
        if (is_close(det, 0)) {
            return std::make_tuple(INF, 0, 0);
        }
        float inv_det = 1.f / det;

        Vec3f ao = ray.org - a;
        float u = p.dot(ao) * inv_det;
        if (u < 0 || 1 < u) {
            return std::make_tuple(INF, 0, 0);
        }

        Vec3f q = ao.cross(ab);
        float v = q.dot(ray.dir) * inv_det;
        if (v < 0 || 1 < u + v) {
            return std::make_tuple(INF, 0, 0);
        }

        float t = q.dot(ac) * inv_det;
        if (t < EPS) {
            return std::make_tuple(INF, 0, 0);
        }

        return std::make_tuple(t, u, v);
    }
};

} // namespace cpu