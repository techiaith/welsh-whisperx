import os
import torch

import whisperx

from lingua import Language, LanguageDetectorBuilder

from celery import Task

class SpeechToTextTask(Task):
    """
    Abstraction of Celery's Task class to support loading ML models.
    Models are loaded once per worker process and shared across all task instances
    (speech_to_text, align_audio, etc.) via class-level attributes.

    Loading is triggered eagerly at worker startup via worker_process_init signal
    (see tasks.py), with lazy loading as a fallback on first task execution.
    """
    abstract = True

    # Class-level attributes to store models (shared across task instances)
    _model = None
    _align_model = None
    _align_metadata = None
    _diarize_model = None
    _lang_detector = None
    _device = None
    _models_loaded = False

    @classmethod
    def _ensure_models_loaded(cls):
        """
        Load all ML models into class-level attributes.
        Called eagerly at worker startup (worker_process_init signal)
        or lazily on first task execution as a fallback.
        Safe to call multiple times — skips if already loaded.
        """
        if cls._models_loaded:
            return

        import logging
        logger = logging.getLogger(__name__)

        logger.info("Initializing models...")

        # Add safe globals for PyTorch 2.8+ serialization
        # This allows loading trusted model checkpoints
        try:
            import pyannote.audio.core.task
            torch.serialization.add_safe_globals([
                torch.torch_version.TorchVersion,
                pyannote.audio.core.task.Specifications,
                pyannote.audio.core.task.Problem,
                pyannote.audio.core.task.Resolution
            ])
            logger.info("Added safe globals for PyTorch serialization")
        except Exception as e:
            logger.warning(f"Could not add safe globals (PyTorch version may not support it): {e}")

        # Authenticate with HuggingFace for private model access
        hf_token = os.environ.get('HF_AUTH_TOKEN')
        if hf_token:
            import time
            max_retries = 3
            retry_delay = 10  # seconds

            for attempt in range(max_retries):
                try:
                    from huggingface_hub import login
                    login(token=hf_token, add_to_git_credential=False)
                    logger.info("Successfully authenticated with HuggingFace")
                    break
                except Exception as e:
                    if "429" in str(e) or "Too Many Requests" in str(e):
                        if attempt < max_retries - 1:
                            wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
                            logger.warning(f"HF rate limit hit (attempt {attempt + 1}/{max_retries}), waiting {wait_time}s before retry: {e}")
                            time.sleep(wait_time)
                        else:
                            logger.warning(f"Failed to login to HuggingFace after {max_retries} attempts (rate limited): {e}")
                            logger.info("Continuing without HF authentication - only public models will be accessible")
                    else:
                        logger.warning(f"Failed to login to HuggingFace: {e}")
                        break
        else:
            logger.warning("No HF_AUTH_TOKEN found, will only be able to access public models")

        compute_type = "int8"
        cls._device = os.environ["WHISPER_MODEL_DEVICE"]
        if (cls._device == "gpu" or cls._device == "cuda") and torch.cuda.is_available():
            cls._device = "cuda"
        else:
            cls._device = "cpu"

        logger.info(f"Whisper model: {os.environ['WHISPER_MODEL_NAME']}")
        logger.info(f"Device: {cls._device}")

        asr_options = {
            "hotwords": None
        }

        logger.info("Loading Whisper model...")
        cls._model = whisperx.load_model(
            os.environ["WHISPER_MODEL_NAME"],
            device=cls._device,
            compute_type=compute_type,
            vad_method="silero",
            asr_options=asr_options
        )
        logger.info("Whisper model loaded successfully")

        logger.info("Loading alignment model...")
        cls._align_model, cls._align_metadata = whisperx.load_align_model(
            language_code=os.environ["WHISPER_MODEL_LANGUAGE"],
            model_name=os.environ["WAV2VEC2_MODEL"],
            device=cls._device
        )
        logger.info("Alignment model loaded successfully")

        logger.info("Loading diarization model...")
        cls._diarize_model = whisperx.diarize.DiarizationPipeline(
            use_auth_token=os.environ['HF_AUTH_TOKEN'],
            device=cls._device
        )
        logger.info("Diarization model loaded successfully")

        logger.info("Loading language detector for Welsh/English...")
        cls._lang_detector = LanguageDetectorBuilder.from_languages(
            Language.ENGLISH, Language.WELSH
        ).build()
        logger.info("Language detector loaded successfully")

        cls._models_loaded = True
        logger.info("All models initialized successfully")

    @property
    def model(self):
        type(self)._ensure_models_loaded()
        return type(self)._model

    @property
    def align_model(self):
        type(self)._ensure_models_loaded()
        return type(self)._align_model

    @property
    def align_metadata(self):
        type(self)._ensure_models_loaded()
        return type(self)._align_metadata

    @property
    def diarize_model(self):
        type(self)._ensure_models_loaded()
        return type(self)._diarize_model

    @property
    def lang_detector(self):
        type(self)._ensure_models_loaded()
        return type(self)._lang_detector

    @property
    def device(self):
        type(self)._ensure_models_loaded()
        return type(self)._device

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)
