# Path Tracing (WIP)

A path tracing renderer in Python accelerated by OpenMP & CUDA.

<!-- |  |  |
|----------------------------------------------------|------------------------------------------------------|
| 1,000,000 spp (15 min)                             | 50,000 spp (21 min)                                  | -->

<!-- |  | ![Dragon Corner](docs/fig/dragon_corner.png) |
|:--------------------------------------------------:|:--------------------------------------------:|
|          100,000 spp (1.5 min)                     |              50,000 spp (21 min)             | -->

| <img src="docs/fig/cornell_box.png" width="600"/> | <img src="docs/fig/dragon_corner.png" width="800"/> |
|:-------------------------------------------------:|:---------------------------------------------------:|
| 100,000 spp (1.5 min)                             | 50,000 spp (21 min)                                 |

## Getting Started

First of all, clone the repo recursively to your local environment.

```sh
git clone --recursive https://github.com/li-plus/path-tracing.git && cd path-tracing
```

If you miss the `--recursive` argument, you could still fetch the submodules in this way.

```sh
git clone https://github.com/li-plus/path-tracing.git && cd path-tracing
git submodule update --init
```

### Python API

Install the python package from source.

```sh
sudo apt install gcc g++ cmake libeigen3-dev python3-dev python3-pip
pip install .
```

Run the Python example.

```sh
cd examples/python
python3 main.py --device cuda --num-samples 1000 --save-path scene.png --scene cornell_box
```

### C++ API

> C++ API is not yet stable. Please consider using Python API instead for the time being.

Install dependencies needed to build the C++ example.

```sh
sudo apt install gcc g++ cmake libeigen3-dev libopencv-dev libgflags-dev
```

Build the path tracing library and the C++ example.

```sh
mkdir -p build && cd build
cmake .. && make -j
```

Run the C++ example.

```sh
./bin/pt -device cuda -num_samples 1000 -save_path scene.png -scene cornell_box
```

## Docker

For those who do not have root privilege, we offer an alternative to build & run path tracing within a docker container. For GPU support, [nvidia-docker](https://github.com/NVIDIA/nvidia-docker) should be further installed.

Build a docker image with everything installed for development.

```sh
docker build ./docker -t pt:latest
```

Start a docker container, with project directory mapped to `/opt/path-tracing`.

```sh
docker run -it --rm --runtime nvidia -v $PWD:/opt/path-tracing -w /opt/path-tracing pt:latest bash
```

## References

+ [smallpt](https://www.kevinbeason.com/smallpt/)
+ [scratchapixel](https://www.scratchapixel.com/index.php)
+ [Ray Tracing in One Weekend](https://raytracing.github.io/)
+ [Schlick's approximation](https://en.wikipedia.org/wiki/Schlick%27s_approximation)
+ [CUDA Texture Funcions](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#texture-functions)
