#include "path_tracer.h"

#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace cpu;

class PyTexture : public Texture {
  public:
    using Texture::Texture;
    Vec3f color(float u, float v) const override { PYBIND11_OVERRIDE_PURE(Vec3f, Texture, color, u, v); }
};

class PyMaterial : public Material {
  public:
    using Material::Material;
    Scatter scatter(const Ray &ray, const Hit &hit, RandomGenerator &rand) const override {
        PYBIND11_OVERRIDE_PURE(Scatter, Material, scatter, ray, hit, rand);
    }
};

class PyObject3d : public Object {
  public:
    using Object::Object;
    void intersect(const Ray &ray, Hit &hit) const override {
        PYBIND11_OVERRIDE_PURE(void, Object, intersect, ray, hit);
    }
};

PYBIND11_MODULE(_C, m) {
    m.doc() = "path tracer python binding";

    py::class_<PathTracer>(m, "PathTracer").def(py::init<DeviceType>()).def("render", &PathTracer::render);
    py::enum_<DeviceType>(m, "DeviceType")
        .value("DEVICE_CPU", DEVICE_CPU)
        .value("DEVICE_CUDA", DEVICE_CUDA)
        .export_values();
    py::class_<Image>(m, "Image", py::buffer_protocol())
        .def(py::init([](const py::array_t<float, py::array::c_style | py::array::forcecast> &array) {
            if (array.ndim() != 3 || array.shape(2) != 3) {
                throw std::runtime_error("Invalid image, expect an RGB image");
            }
            ssize_t height = array.shape(0);
            ssize_t width = array.shape(1);
            return std::make_unique<Image>((uint8_t *)array.data(), height, width);
        }))
        .def("numpy", [](const Image &self) {
            Image out = self.post_process();
            std::vector<ssize_t> shapes{out.height(), out.width(), 3};
            std::vector<ssize_t> strides{(ssize_t)(sizeof(Vec3f) * out.width()), sizeof(Vec3f), sizeof(float)};
            return py::array_t<float>(py::buffer_info((uint8_t *)out.data(), sizeof(float),
                                                      py::format_descriptor<float>::format(), 3, shapes, strides));
        });

    py::class_<Camera>(m, "Camera")
        .def(py::init<const Vec3f &, const Vec3f &, const Vec3f &, int, int, float>())
        .def("shoot_ray", &Camera::shoot_ray);

    py::class_<Scene>(m, "Scene").def(py::init<std::vector<std::shared_ptr<Object>>, Vec3f>());

    py::class_<Object, PyObject3d, std::shared_ptr<Object>>(m, "Object3d").def(py::init());
    py::class_<Sphere, Object, std::shared_ptr<Sphere>>(m, "Sphere")
        .def(py::init<Vec3f, float, std::shared_ptr<Material>>());
    py::class_<Plane, Object, std::shared_ptr<Plane>>(m, "Plane")
        .def(py::init<const Vec3f &, float, std::shared_ptr<Material>>());
    py::class_<RectXY, Object, std::shared_ptr<RectXY>>(m, "RectXY")
        .def(py::init<const Vec3f &, const Vec3f &, std::shared_ptr<Material>>());
    py::class_<RectYZ, Object, std::shared_ptr<RectYZ>>(m, "RectYZ")
        .def(py::init<const Vec3f &, const Vec3f &, std::shared_ptr<Material>>());
    py::class_<RectXZ, Object, std::shared_ptr<RectXZ>>(m, "RectXZ")
        .def(py::init<const Vec3f &, const Vec3f &, std::shared_ptr<Material>>());
    py::class_<Circle, Object, std::shared_ptr<Circle>>(m, "Circle")
        .def(py::init<const Vec3f &, float, const Vec3f &, std::shared_ptr<Material>>());
    py::class_<Mesh, Object, std::shared_ptr<Mesh>>(m, "Mesh").def(
        py::init<const std::string &, std::shared_ptr<Material>>());

    py::class_<Material, PyMaterial, std::shared_ptr<Material>>(m, "Material").def(py::init());
    py::class_<Diffusive, Material, std::shared_ptr<Diffusive>>(m, "Diffusive")
        .def(py::init<std::shared_ptr<Texture>>());
    py::class_<Reflective, Material, std::shared_ptr<Reflective>>(m, "Reflective")
        .def(py::init<std::shared_ptr<Texture>>());
    py::class_<Dielectric, Material, std::shared_ptr<Dielectric>>(m, "Dielectric")
        .def(py::init<std::shared_ptr<Texture>>());
    py::class_<Light, Material, std::shared_ptr<Light>>(m, "Light").def(py::init<Vec3f>());

    py::class_<Texture, PyTexture, std::shared_ptr<Texture>>(m, "Texture").def(py::init());
    py::class_<SolidColorTexture, Texture, std::shared_ptr<SolidColorTexture>>(m, "SolidColorTexture")
        .def(py::init<Vec3f>());
    py::class_<CheckedTexture, Texture, std::shared_ptr<CheckedTexture>>(m, "CheckedTexture")
        .def(py::init<float, Vec3f, Vec3f>());

    py::class_<Vec3f>(m, "Vec3f").def(py::init<float, float, float>());
}
