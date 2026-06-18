# ============================================================================
# OpenVINO Builder Image
# ============================================================================

FROM ubuntu:24.04
LABEL org.opencontainers.image.source="https://github.com/droans/ov-builder"
LABEL org.opencontainers.image.version="builder"
ENV DEBIAN_FRONTEND=noninteractive

# ============================================================================
# System Dependencies
# ============================================================================


RUN apt-get update && apt-get install -y \
    software-properties-common
RUN apt-get update && apt-get install -y \
    gpg \
    gpg-agent \
    wget \
    ca-certificates \
    curl \
    git \
    nano \
    pkg-config \
    make \
    gcc \
    g++ \
    clang-15 \
    libclang-15-dev \
    cmake \
    build-essential \
    python3 \
    python3-venv \
    python3-dev \
    python3-pip && \
    rm -rf /var/lib/apt/lists/*
RUN
RUN wget -qO - https://repositories.intel.com/gpu/intel-graphics.key | \
    gpg --dearmor --output /usr/share/keyrings/intel-graphics.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/intel-graphics.gpg] https://repositories.intel.com/gpu/ubuntu noble client" | \
    tee /etc/apt/sources.list.d/intel-gpu-noble.list && \
    wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | \
    gpg --dearmor | tee /usr/share/keyrings/oneapi-archive-keyring.gpg > /dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" | \
    tee /etc/apt/sources.list.d/oneAPI.list && \
    add-apt-repository ppa:kobuk-team/intel-graphics -n

RUN apt-get update && apt-get install -y \
    intel-ocloc \
    intel-opencl-icd \
    libze1 \
    libze-dev \
    libze-intel-gpu1 \
    libze-intel-gpu-dev \
    libze-intel-gpu-raytracing \
    intel-media-va-driver-non-free \
    libmfx-gen1 \
    libvpl2 \
    libegl-mesa0 \
    libegl1-mesa-dev \
    libgbm1 \
    libgl1-mesa-dev \
    libgl1-mesa-dri \
    libglapi-mesa \
    libgles2-mesa-dev \
    libglx-mesa0 \
    libigdgmm12 \
    libxatracker2 \
    mesa-va-drivers \
    mesa-vdpau-drivers \
    mesa-vulkan-drivers \
    va-driver-all \
    vainfo \
    hwinfo \
    clinfo \
    libigc-dev \
    libigdfcl-dev \
    libigfxcmrt-dev \
    libze-dev \
    intel-oneapi-toolkit && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3 1 && \
    rm -rf /var/lib/apt/lists/*

# ============================================================================
# Get OpenVINO sources
# ============================================================================

RUN mkdir /openvino_src && \
    cd /openvino_src && \
    git clone --recursive https://github.com/openvinotoolkit/openvino.git /openvino_src && \
    git submodule update --init --recursive
# ============================================================================
# Get OpenVINO-GenAI sources
# ============================================================================

RUN mkdir /genai_src && \
    cd /genai_src && \
    git clone --recursive https://github.com/openvinotoolkit/openvino.genai.git /genai_src && \
    git submodule update --init --recursive

# ============================================================================
# Install uv package manager
# ============================================================================
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# ============================================================================
# Environmental variables
# ============================================================================

# ======================================
# Update variables
#
# UPDATE_XXXX: 1=Update, 0=Skip (Default: 1)
# XXXX_GIT_REMOTE: Remote to use for pulling from git (Default: main repositories)
# XXXX_GIT_BRANCH: Remote branch to use (Default: main)
# XXXX_GIT_PR: PR to use for remote (Default: Unset)
#   * If both XXXX_GIT_BRANCH and XXXX_GIT_PR are set, XXXX_GIT_PR will take priority.
# XXXX_GIT_PR_USE_MERGED: 1=Yes, 0=No (Default: 1)
#   * If Yes, will use the PR merged with the main branch. If no, will use the current
#     head of the branch.
# ======================================

# ======================================
# Update OpenVINO
# ======================================
# 1=Update, 0=Skip
ENV UPDATE_OPENVINO=1

ENV OPENVINO_GIT_REMOTE="openvinotoolkit/openvino"
ENV OPENVINO_GIT_BRANCH="master"
ENV OPENVINO_GIT_PR=""
ENV OPENVINO_GIT_PR_USE_MERGED=1

# Build type to use (ze, ocl, sycl, debug-ocl)
ENV OPENVINO_BUILD_TYPE="ocl"
# Build file to use instead of build type.
# If both OPENVINO_BUILD_TYPE and OPENVINO_BUILD_FILE are set, OPENVINO_BUILD_FILE will
#   take priority.
ENV OPENVINO_BUILD_FILE=""

# ======================================
# Update OpenVINO-GenAI
# ======================================
ENV UPDATE_GENAI=1
ENV GENAI_REPO="openvinotoolkit/openvino.genai"
ENV GENAI_GIT_BRANCH="master"
ENV GENAI_GIT_PR=""
ENV GENAI_GIT_PR_USE_MERGED=1

# ======================================
# Update OpenVINO Tokenizers
# ======================================
ENV UPDATE_TOKENIZERS=1

# Directory to save wheels
ENV OUTPUT_DIR="/output"
# Use dated folders (eg, OUTPUT_DIR/2026_06_17) to keep regular backups. 1=Yes, 0=No (Default: 1)
ENV USE_DATED_FOLDERS=1
# Save update environmental variables with the built wheels. 1=Yes, 0=No (Default: 1)
ENV SAVE_UPDATE_ENVS=1

# ============================================================================
# Clone and setup program
# ============================================================================
COPY ./LICENSE /app/LICENSE
COPY ./pyproject.toml /app/pyproject.toml
COPY ./src /app/src
COPY ./main.py /app/main.py
COPY ./build_scripts /build_scripts

WORKDIR /app
RUN cd /app && \
    uv venv && \
    uv sync && \
    uv pip install pip
ENV PATH="/app/.venv/bin:$PATH"

CMD ["bash", "-c", "python /app/main.py"]
