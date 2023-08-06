from path_tracing import _C


def _parse_device(device) -> _C.DeviceType:
    device_map = {
        'cpu': _C.DEVICE_CPU,
        'cuda': _C.DEVICE_CUDA,
    }
    if device not in device_map:
        raise RuntimeError(f'Unknown device {device}')
    return device_map[device]


def _parse_vec3f(pos) -> _C.Vec3f:
    x, y, z = pos
    return _C.Vec3f(float(x), float(y), float(z))


def _parse_color(color) -> _C.Vec3f:
    if isinstance(color, str):
        pass
    return _parse_vec3f(color)


class PathTracer(_C.PathTracer):
    def __init__(self, device='cpu') -> None:
        device = _parse_device(device)
        super().__init__(device)

    def render(self, scene, camera, num_samples):
        return super().render(scene, camera, num_samples)


class Scene(_C.Scene):
    def __init__(self, objects, background) -> None:
        background = _parse_vec3f(background)
        super().__init__(objects, background)


class Camera(_C.Camera):
    def __init__(self, center, direction, up, width, height, vfov) -> None:
        center = _parse_vec3f(center)
        direction = _parse_vec3f(direction)
        up = _parse_vec3f(up)
        super().__init__(center, direction, up, width, height, vfov)


class Sphere(_C.Sphere):
    def __init__(self, center, radius, material) -> None:
        center = _parse_vec3f(center)
        super().__init__(center, radius, material)


class RectXY(_C.RectXY):
    def __init__(self, minv, maxv, material) -> None:
        minv = _parse_vec3f(minv)
        maxv = _parse_vec3f(maxv)
        super().__init__(minv, maxv, material)


class RectYZ(_C.RectYZ):
    def __init__(self, minv, maxv, material) -> None:
        minv = _parse_vec3f(minv)
        maxv = _parse_vec3f(maxv)
        super().__init__(minv, maxv, material)


class RectXZ(_C.RectXZ):
    def __init__(self, minv, maxv, material) -> None:
        minv = _parse_vec3f(minv)
        maxv = _parse_vec3f(maxv)
        super().__init__(minv, maxv, material)


class Plane(_C.Plane):
    def __init__(self, normal, dist, material) -> None:
        normal = _parse_vec3f(normal)
        super().__init__(normal, dist, material)


class Circle(_C.Circle):
    def __init__(self, center, radius, normal, material) -> None:
        center = _parse_vec3f(center)
        normal = _parse_vec3f(normal)
        super().__init__(center, radius, normal, material)


class Diffusive(_C.Diffusive):
    def __init__(self, texture) -> None:
        super().__init__(texture)


class Reflective(_C.Reflective):
    def __init__(self, texture) -> None:
        super().__init__(texture)


class Dielectric(_C.Dielectric):
    def __init__(self, texture) -> None:
        super().__init__(texture)


class Light(_C.Light):
    def __init__(self, emittance) -> None:
        emittance = _parse_vec3f(emittance)
        super().__init__(emittance)


class SolidColorTexture(_C.SolidColorTexture):
    def __init__(self, color) -> None:
        color = _parse_color(color)
        super().__init__(color)


class CheckedTexture(_C.CheckedTexture):
    def __init__(self, period, dark_color, light_color) -> None:
        dark_color = _parse_color(dark_color)
        light_color = _parse_color(light_color)
        super().__init__(period, dark_color, light_color)
