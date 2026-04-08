from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _default_device() -> str:
    try:
        import torch

        return "cuda" if torch.cuda.is_available() else "cpu"
    except Exception:
        return "cpu"


@dataclass(frozen=True)
class Settings:
    root_dir: Path
    output_dir: Path
    host: str
    port: int
    default_model_id: str
    default_negative_prompt: str
    device: str
    dtype: str
    variant: str | None
    use_safetensors: bool
    hf_cache_dir: Path | None
    hf_token: str | None
    max_width: int
    max_height: int
    default_steps: int
    default_guidance_scale: float
    default_strength: float


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    root_dir = Path(__file__).resolve().parent
    output_dir = Path(os.getenv("NYMPHS2D2_OUTPUT_DIR", root_dir / "outputs")).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)

    hf_cache_raw = os.getenv("NYMPHS3D_HF_CACHE_DIR")
    hf_cache_dir = Path(hf_cache_raw).expanduser() if hf_cache_raw else None

    return Settings(
        root_dir=root_dir,
        output_dir=output_dir,
        host=os.getenv("NYMPHS2D2_HOST", "0.0.0.0"),
        port=int(os.getenv("NYMPHS2D2_PORT", "8090")),
        default_model_id=os.getenv(
            "NYMPHS2D2_MODEL_ID",
            "playgroundai/playground-v2.5-1024px-aesthetic",
        ),
        default_negative_prompt=os.getenv("NYMPHS2D2_DEFAULT_NEGATIVE_PROMPT", ""),
        device=os.getenv("NYMPHS2D2_DEVICE", _default_device()),
        dtype=os.getenv("NYMPHS2D2_DTYPE", "float16"),
        variant=os.getenv("NYMPHS2D2_MODEL_VARIANT") or None,
        use_safetensors=_env_bool("NYMPHS2D2_USE_SAFETENSORS", True),
        hf_cache_dir=hf_cache_dir,
        hf_token=os.getenv("NYMPHS3D_HF_TOKEN") or None,
        max_width=int(os.getenv("NYMPHS2D2_MAX_WIDTH", "1536")),
        max_height=int(os.getenv("NYMPHS2D2_MAX_HEIGHT", "1536")),
        default_steps=int(os.getenv("NYMPHS2D2_DEFAULT_STEPS", "30")),
        default_guidance_scale=float(os.getenv("NYMPHS2D2_DEFAULT_GUIDANCE_SCALE", "3.0")),
        default_strength=float(os.getenv("NYMPHS2D2_DEFAULT_STRENGTH", "0.45")),
    )
