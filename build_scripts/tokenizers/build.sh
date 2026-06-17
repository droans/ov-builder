VIRTUAL_ENV=/app/.venv
. ${VIRTUAL_ENV}/bin/activate
echo Tokenizers: Build

uv pip install 'py-build-cmake==0.4.3'

cd /genai_src/thirdparty/openvino_tokenizers
rm -rf .py-build-cmake_cache

echo Building Tokenizers.
OpenVINO_DIR=${VIRTUAL_ENV}/lib/python3.12/site-packages/openvino/cmake \
  python -m pip wheel . --no-deps --no-build-isolation \
  --wheel-dir ${WHEEL_DIR}
echo Tokenizers built.
