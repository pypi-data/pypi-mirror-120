#pragma once

#include <Eigen/Dense>
#include <vector>

namespace cpu {

typedef Eigen::Vector3f Vec3f;

class Image {
  public:
    Image() : _width(0), _height(0) {}
    Image(int width_, int height_) : _width(width_), _height(height_), _data(width_ * height_) {}
    Image(int width_, int height_, const Vec3f &fill_val_)
        : _width(width_), _height(height_), _data(width_ * height_, fill_val_) {}
    Image(uint8_t *ptr, int width_, int height_) : _width(width_), _height(height_), _data(width_ * height_) {
        std::memcpy((uint8_t *)_data.data(), ptr, sizeof(Vec3f) * width_ * height_);
    }

    bool empty() const { return _data.empty(); }
    int width() const { return _width; }
    int height() const { return _height; }
    const Vec3f *data() const { return _data.data(); }
    Vec3f *data() { return _data.data(); }

    static Image zeros(int width, int height) { return Image(width, height, Vec3f::Zero()); }
    static Image ones(int width, int height) { return Image(width, height, Vec3f::Ones()); }

    Image pre_process() const {
        Image in = *this;
        in.gamma(2.2);
        in.vertical_flip();
        return in;
    }

    Image post_process() const {
        Image out = *this;
        out.gamma(1 / 2.2);
        // flip y axis so that (0,0) is bottom left corner
        out.vertical_flip();
        return out;
    }

    void set_pixel(int x, int y, const Vec3f &color) { _data[idx(x, y)] = color; }
    Vec3f get_pixel(int x, int y) const { return _data[idx(x, y)]; }

    void gamma(float p) {
        for (auto &pix : _data) {
            pix = pix.array().pow(p);
        }
    }

    void vertical_flip() {
        for (int y1 = 0, y2 = _height - 1; y1 < y2; y1++, y2--) {
            for (int x = 0; x < _width; x++) {
                std::swap(_data[idx(x, y1)], _data[idx(x, y2)]);
            }
        }
    }

  private:
    int idx(int x, int y) const { return y * _width + x; }

  private:
    int _width;
    int _height;
    std::vector<Vec3f> _data;
};

} // namespace cpu