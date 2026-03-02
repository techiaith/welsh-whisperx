# WhisperX Server Makefile
#
# Quick Start:
#   make build-gpu    # Build and run with GPU support (production)
#   make build-cpu    # Build and run with CPU support (development/testing)
#   make help         # Show all available commands

# Default device: reads from .device (set during build), falls back to gpu
DEVICE ?= $(shell cat .device 2>/dev/null || echo gpu)

.PHONY: help
help:
	@echo "WhisperX Server - Available Commands"
	@echo "====================================="
	@echo ""
	@echo "Setup:"
	@echo "  make setup            Initialize environment files"
	@echo ""
	@echo "GPU Deployment (Fast, Requires NVIDIA GPU):"
	@echo "  make build-gpu                       Build and run with GPU support (default)"
	@echo "  make up-gpu                          Start existing GPU containers"
	@echo "  make scale-high-gpu N=2              Scale high-priority GPU workers"
	@echo "  make scale-default-gpu N=3           Scale default GPU workers"
	@echo ""
	@echo "CPU Deployment (Slower, Runs Anywhere):"
	@echo "  make build-cpu                       Build and run with CPU support"
	@echo "  make up-cpu                          Start existing CPU containers"
	@echo "  make scale-high-cpu N=2              Scale high-priority CPU workers"
	@echo "  make scale-default-cpu N=2           Scale default CPU workers"
	@echo ""
	@echo "General Commands:"
	@echo "  make logs             View container logs (follows current DEVICE)"
	@echo "  make down             Stop all containers"
	@echo "  make test             Run API endpoint tests"
	@echo "  make health           Check service health"
	@echo "  make ready            Wait for workers to finish loading models"
	@echo "  make status           Show running containers"
	@echo ""
	@echo "Maintenance:"
	@echo "  make update           Pull latest code from git"
	@echo "  make clean            Stop and remove containers/images"
	@echo "  make purge            Stop and remove containers/images/volumes"
	@echo ""
	@echo "Performance Comparison:"
	@echo "  GPU: ~30 seconds per 5-min audio file (100+ files/hour)"
	@echo "  CPU: ~5-8 minutes per 5-min audio file (10-15 files/hour)"
	@echo ""
	@echo "Current Settings:"
	@echo "  DEVICE = ${DEVICE}"
	@echo ""

# Default target
.DEFAULT_GOAL := help

# Legacy default for backward compatibility
default: build-gpu

# Setup environment files
.PHONY: setup
setup:
	@echo "Setting up environment files..."
	@if [ ! -f .env.secrets ]; then \
		echo "Creating .env.secrets from template..."; \
		cp .env.secrets.example .env.secrets; \
		echo "⚠️  Please edit .env.secrets and add your HF_AUTH_TOKEN"; \
	else \
		echo "✓ .env.secrets already exists"; \
	fi
	@echo "Merging config.env and .env.secrets into .env..."
	@cat config.env > .env
	@echo "" >> .env
	@echo "# Secrets (from .env.secrets)" >> .env
	@if [ -f .env.secrets ]; then \
		cat .env.secrets >> .env; \
	fi
	@echo "✓ Environment setup complete!"
	@echo ""
	@echo "Configuration:"
	@echo "  - config.env         (transparent, in git)"
	@echo "  - .env.secrets       (secret, gitignored)"
	@echo "  - .env               (generated, gitignored)"
	@echo ""
	@if grep -q "your_huggingface_token_here" .env.secrets 2>/dev/null; then \
		echo "⚠️  Remember to edit .env.secrets with your actual HF_AUTH_TOKEN"; \
		echo "   Get your token from: https://huggingface.co/settings/tokens"; \
	fi
	@echo ""

# Configuration helper
config:
	$(eval DOCKER_COMPOSE = docker compose -f docker-compose.${DEVICE}.yml --env-file .env --project-name whisperx-server)

# GPU-specific targets
.PHONY: build-gpu up-gpu scale-high-gpu scale-default-gpu
build-gpu:
	@echo "======================================"
	@echo "Building WhisperX Server with GPU"
	@echo "======================================"
	@echo "Requirements: NVIDIA GPU, nvidia-docker2"
	@echo "Performance: ~30 seconds per 5-min audio"
	@echo "======================================"
	@$(MAKE) DEVICE=gpu build

up-gpu:
	@$(MAKE) DEVICE=gpu up

scale-high-gpu:
	@if [ -z "$(N)" ]; then \
		echo "Error: Please specify number of workers with N=<count>"; \
		echo "Example: make scale-high-gpu N=2"; \
		exit 1; \
	fi
	@echo "Scaling high-priority GPU workers to $(N)..."
	@$(MAKE) DEVICE=gpu _scale-high N=$(N)

scale-default-gpu:
	@if [ -z "$(N)" ]; then \
		echo "Error: Please specify number of workers with N=<count>"; \
		echo "Example: make scale-default-gpu N=3"; \
		exit 1; \
	fi
	@echo "Scaling default GPU workers to $(N)..."
	@$(MAKE) DEVICE=gpu _scale-default N=$(N)

# CPU-specific targets
.PHONY: build-cpu up-cpu scale-high-cpu scale-default-cpu
build-cpu:
	@echo "======================================"
	@echo "Building WhisperX Server with CPU"
	@echo "======================================"
	@echo "Requirements: Docker (no GPU needed)"
	@echo "Performance: ~5-8 minutes per 5-min audio"
	@echo "======================================"
	@$(MAKE) DEVICE=cpu build

up-cpu:
	@$(MAKE) DEVICE=cpu up

scale-high-cpu:
	@if [ -z "$(N)" ]; then \
		echo "Error: Please specify number of workers with N=<count>"; \
		echo "Example: make scale-high-cpu N=2"; \
		exit 1; \
	fi
	@echo "Scaling high-priority CPU workers to $(N)..."
	@$(MAKE) DEVICE=cpu _scale-high N=$(N)

scale-default-cpu:
	@if [ -z "$(N)" ]; then \
		echo "Error: Please specify number of workers with N=<count>"; \
		echo "Example: make scale-default-cpu N=2"; \
		exit 1; \
	fi
	@echo "Scaling default CPU workers to $(N)..."
	@$(MAKE) DEVICE=cpu _scale-default N=$(N)

# Internal scaling helpers
.PHONY: _scale-high _scale-default
_scale-high: config
	${DOCKER_COMPOSE} up -d --scale worker-high=$(N)
	@echo "✓ High-priority workers scaled to $(N)"

_scale-default: config
	${DOCKER_COMPOSE} up -d --scale worker-default=$(N)
	@echo "✓ Default workers scaled to $(N)"

# Core build command (used by build-gpu and build-cpu)
.PHONY: build
build: config
	@echo "${DEVICE}" > .device
	@echo "Copying shared folder to build contexts..."
	@./copy-shared.sh
	@echo "Building ${DEVICE} base image (techiaith/whisperx-device)..."
	@docker build --rm -f Dockerfile.${DEVICE} -t techiaith/whisperx-device .
	@echo "Building and starting containers..."
	${DOCKER_COMPOSE} up -d --build
	@echo ""
	@echo "✓ WhisperX Server started successfully!"
	@echo ""
	@echo "Service URLs:"
	@echo "  API:    http://localhost:5511"
	@echo "  Health: http://localhost:5511/health/"
	@echo "  Docs:   http://localhost:5511/docs"
	@echo ""
	@echo "Useful commands:"
	@echo "  make ready     - Wait for models to finish loading"
	@echo "  make logs      - View container logs"
	@echo "  make status    - Check container status"
	@echo "  make health    - Check service health"
	@echo "  make down      - Stop all containers"
	@echo ""

.PHONY: up
up: config
	@echo "Starting WhisperX Server (${DEVICE} mode)..."
	${DOCKER_COMPOSE} up -d
	@echo ""
	@echo "✓ WhisperX Server started successfully!"
	@echo ""
	@echo "Service URLs:"
	@echo "  API:    http://localhost:5511"
	@echo "  Health: http://localhost:5511/health/"
	@echo ""
	@echo "Useful commands:"
	@echo "  make ready     - Wait for models to finish loading"
	@echo "  make logs      - View container logs"
	@echo "  make status    - Check container status"
	@echo "  make health    - Check service health"
	@echo ""

# View logs
.PHONY: logs
logs: config
	${DOCKER_COMPOSE} logs -f

# Stop containers
.PHONY: down
down: config
	@echo "Stopping WhisperX Server..."
	${DOCKER_COMPOSE} stop
	@echo "✓ Containers stopped"

# Health check
.PHONY: health
health:
	@echo "Checking WhisperX Server health..."
	@echo ""
	@echo "=== Service Health ==="
	@curl -s http://localhost:5511/health/ | python3 -m json.tool || echo "❌ Service not responding"
	@echo ""
	@echo "=== Queue Status ==="
	@curl -s http://localhost:5511/queue/status/ | python3 -m json.tool || echo "❌ Queue endpoint not responding"

# Wait for workers to load models and become ready
.PHONY: ready
ready:
	@echo "Waiting for workers to load models..."
	@timeout=300; elapsed=0; \
	while [ $$elapsed -lt $$timeout ]; do \
		result=$$(curl -s http://localhost:5511/health/ 2>/dev/null); \
		models=$$(echo "$$result" | python3 -c "import sys,json; print(json.load(sys.stdin)['checks'].get('models',''))" 2>/dev/null); \
		status=$$(echo "$$result" | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])" 2>/dev/null); \
		if [ -n "$$models" ] && echo "$$models" | grep -qv "^0 "; then \
			echo "✓ $$models"; \
			echo "✓ Status: $$status"; \
			exit 0; \
		fi; \
		printf "\r  ⏳ Models loading... (%ds)" "$$elapsed"; \
		sleep 5; \
		elapsed=$$((elapsed + 5)); \
	done; \
	echo ""; \
	echo "⚠️  Timeout after $${timeout}s. Check logs: make logs"; \
	exit 1

# Show container status
.PHONY: status
status:
	@echo "WhisperX Server Status:"
	@echo ""
	@docker ps --filter "name=whisperx" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Update from git
.PHONY: update
update:
	@echo "Pulling latest changes..."
	-git pull --recurse-submodules
	@echo "✓ Update complete. Run 'make build-gpu' or 'make build-cpu' to rebuild."

# Test API endpoints
.PHONY: test
test:
	@echo "Testing WhisperX API endpoints..."
	@echo ""
	@echo "=== Testing /transcribe/ ==="
	-curl -F 'soundfile=@speech.wav' localhost:5511/transcribe/ && echo "\n"
	@echo ""
	@echo "=== Testing /transcribe_long_form/ ==="
	-curl -F 'soundfile=@speech.wav' localhost:5511/transcribe_long_form/ && echo "\n"
	@echo ""
	@echo "=== Testing /keyboard/ ==="
	-curl --location 'http://localhost:5511/keyboard/' --form 'audio_file=@"speech.wav"' && echo "\n"
	@echo ""
	@echo "=== Testing /translate/ ==="
	-curl -F 'soundfile=@speech.wav' localhost:5511/translate/ && echo "\n"
	@echo ""
	@echo "=== Testing /translate_long_form/ ==="
	-curl -F 'soundfile=@speech.wav' localhost:5511/translate_long_form/ && echo "\n"
	@echo ""
	@echo "=== Testing /align/ ==="
	-curl -F 'soundfile=@speech.wav' -F 'text=Mae ganddynt dau o blant, mab a merch' localhost:5511/align/ && echo "\n"

# Clean up containers and images
.PHONY: clean
clean: config down
	@echo "Removing containers and images..."
	${DOCKER_COMPOSE} down --rmi all
	-@docker rmi techiaith/whisperx-device 2>/dev/null && echo "Removed techiaith/whisperx-device" || true
	@echo "✓ Cleanup complete"

# Purge everything including volumes
.PHONY: purge
purge: config down
	@echo "⚠️  WARNING: This will remove all containers, images, and data volumes!"
	@echo "Press Ctrl+C to cancel, or Enter to continue..."
	@read confirmation
	${DOCKER_COMPOSE} down --volumes --rmi all
	-@docker rmi techiaith/whisperx-device 2>/dev/null && echo "Removed techiaith/whisperx-device" || true
	@echo "✓ Full purge complete"

# Quick reference
.PHONY: quick
quick:
	@echo "Quick Reference:"
	@echo ""
	@echo "First Time Setup:"
	@echo "  1. make setup"
	@echo "  2. Edit .env.secrets and add your HF_AUTH_TOKEN"
	@echo "  3. make setup  (to regenerate .env with your token)"
	@echo "  4. make build-gpu  (or make build-cpu for CPU-only)"
	@echo ""
	@echo "Daily Usage:"
	@echo "  make up-gpu        Start GPU version"
	@echo "  make up-cpu        Start CPU version"
	@echo "  make logs          View logs"
	@echo "  make health        Check if running"
	@echo "  make down          Stop everything"
	@echo ""
	@echo "For full help: make help"
