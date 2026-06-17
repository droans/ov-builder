cd /openvino_src
echo OpenVINO: Build as ZE debug.
echo Updating OpenVINO
git pull
git submodule update --init --recursive
source .venv/bin/activate
echo Configuring OpenVINO build...
cmake \
  -G 'Ninja Multi-Config' \
  -DCMAKE_BUILD_TYPE=Debug \
  -DENABLE_DEBUG_CAPS=ON \
  -DENABLE_CPU_DEBUG_CAPS=ON \
  -DENABLE_GPU_DEBUG_CAPS=ON \
  -DENABLE_SNIPPETS_DEBUG_CAPS=ON \
  -DENABLE_NPU_DEBUG_CAPS=ON \
  -DENABLE_PYTHON=ON \
  -DENABLE_WHEEL=ON \
  -DPython3_EXECUTABLE=$(which python3) \
  -DCMAKE_CXX_FLAGS="-D_GLIBCXX_USE_CXX11_ABI=0" \
  -DCMAKE_C_FLAGS="-D_GLIBCXX_USE_CXX11_ABI=0" \
  -DENABLE_NCC_STYLE=OFF \
  -DENABLE_TESTS=ON \
  -DENABLE_STRICT_DEPENDENCIES=OFF \
  -DENABLE_SYSTEM_OPENCL=ON \
  -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
  -DCPACK_GENERATOR=TGZ \
  -DCMAKE_COMPILE_WARNING_AS_ERROR=ON \
  -DGPU_RT_TYPE=L0 \
  -S ./ \
  -B ./build
cd build
echo OpenVINO build configured...
echo Building OpenVINO.
cmake --build ./  --parallel $(nproc) --target ie_wheel
echo OpenVINO built.
uv pip install wheels/*whl
mv wheels/*whl ${WHEEL_DIR}
