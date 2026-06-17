cd /openvino_src
echo OpenVINO: Build as OCL.
echo Updating OpenVINO
git pull
git submodule update --init --recursive
source .venv/bin/activate
echo Configuring OpenVINO build...
cmake \
  -DCMAKE_BUILD_TYPE=Release \
  -DENABLE_PYTHON=ON \
  -DENABLE_WHEEL=ON \
  -DPython3_EXECUTABLE=$(which python3) \
  -DCMAKE_CXX_FLAGS="-D_GLIBCXX_USE_CXX11_ABI=0" \
  -DCMAKE_C_FLAGS="-D_GLIBCXX_USE_CXX11_ABI=0" \
  -S ./ \
  -B ./build
cd build
echo OpenVINO build configured...
echo Building OpenVINO.
cmake --build ./  --parallel $(nproc) --target ie_wheel
echo OpenVINO built.
uv pip install wheels/*whl
mv wheels/*whl ${WHEEL_DIR}
