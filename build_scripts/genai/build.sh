VIRTUAL_ENV=/app/.venv
. ${VIRTUAL_ENV}/bin/activate
echo GenAI: Build

uv pip install 'py-build-cmake==0.5.0'

cd /genai_src
echo Updating GenAI
git pull
git submodule update --init --recursive

rm -rf .py-build-cmake_cache

echo Building GenAI.
OpenVINO_DIR=${VIRTUAL_ENV}/lib/python3.12/site-packages/openvino/cmake \
  CMAKE_CXX_FLAGS="-D_GLIBCXX_USE_CXX11_ABI=0" \
  CMAKE_C_FLAGS="-D_GLIBCXX_USE_CXX11_ABI=0" \
  CMAKE_BUILD_TYPE=Release \
  ENABLE_SYSTEM_TBB=ON \
  python -m pip wheel . --no-deps --no-build-isolation \
    --extra-index-url https://storage.openvinotoolkit.org/simple/wheels/pre-release \
    --extra-index-url https://storage.openvinotoolkit.org/simple/wheels/nightly \
    --wheel-dir ${WHEEL_DIR}
echo GenAI built.
