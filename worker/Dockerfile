FROM techiaith/whisperx-device

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/London

# Build argument to determine device type (passed from docker-compose)
ARG DEVICE=gpu

RUN apt update -q \
 && apt install -y -qq tzdata bash build-essential git curl wget software-properties-common \
    vim ca-certificates libffi-dev libssl-dev libsndfile1 libbz2-dev liblzma-dev locales \
    libboost-all-dev libboost-tools-dev libboost-thread-dev cmake  \
    python3 python3-pip python3-setuptools python3-dev curl zip zlib1g-dev vim \
    ffmpeg sox alsa-utils protobuf-compiler \
 && python3 -m pip install --upgrade pip \
 && apt clean -q

# Download and install cuDNN 8 libraries alongside cuDNN 9 (GPU only, x86_64 only)
# For CPU builds or ARM architecture, this step is skipped
RUN if [ "$DEVICE" = "gpu" ] && [ "$(uname -m)" = "x86_64" ]; then \
        echo "Installing cuDNN 8 for x86_64 GPU..."; \
        wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb && \
        dpkg -i cuda-keyring_1.0-1_all.deb && \
        apt-get update && \
        apt-get install -y libcudnn8=8.9.7.29-1+cuda12.2 libcudnn8-dev=8.9.7.29-1+cuda12.2 && \
        rm cuda-keyring_1.0-1_all.deb; \
    elif [ "$DEVICE" = "gpu" ]; then \
        echo "Skipping cuDNN installation (not available for $(uname -m) architecture)"; \
    else \
        echo "Skipping cuDNN installation (CPU build)"; \
    fi

ARG WHISPER_MODEL_NAME
ENV WHISPER_MODEL_NAME=${WHISPER_MODEL_NAME}
ARG WHISPER_MODEL_DEVICE
ENV WHISPER_MODEL_DEVICE=${WHISPER_MODEL_DEVICE}
ARG WHISPER_MODEL_LANGUAGE
ENV WHISPER_MODEL_LANGUAGE=${WHISPER_MODEL_LANGUAGE}
ARG WAV2VEC2_MODEL
ENV WAV2VEC2_MODEL=${WAV2VEC2_MODEL}

WORKDIR /worker
COPY ./requirements.txt .

# Install all requirements from requirements.txt
# This now includes PyTorch, TorchVision, TorchAudio, and WhisperX
RUN pip install -r requirements.txt

COPY . .

# Copy shared logging module
COPY ./shared /app/shared

ENTRYPOINT ["./start_workers.sh"]
