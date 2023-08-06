#pragma once

#include <chrono>

struct Timer {
    std::chrono::system_clock::time_point start;

    Timer() { start = std::chrono::system_clock::now(); }

    float count_seconds() const {
        auto now = std::chrono::system_clock::now();
        std::chrono::duration<float> duration(now - start);
        return duration.count();
    }

    int timestamp() const { return std::chrono::duration_cast<std::chrono::seconds>(start.time_since_epoch()).count(); }
};
