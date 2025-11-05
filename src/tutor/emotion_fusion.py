import numpy as np
from .emotion_spaces import zero_vad

def fuse(text_sentiment: float | None, prosody_energy: float | None, vlm_label: str | None) -> np.ndarray:
    """Возвращает дельту VAD в [-1..1] по трём каналам, мягкий вес."""
    v = zero_vad()
    if text_sentiment is not None:
        v[0] += float(np.clip(text_sentiment, -1, 1)) * 0.4  # Valence
    if prosody_energy is not None:
        v[1] += float(np.clip(prosody_energy, -1, 1)) * 0.4  # Arousal
    if vlm_label in ("engaged", "focused"):
        v[2] += 0.2  # Dominance ~ уверенность/контроль
    elif vlm_label in ("bored", "confused"):
        v[2] -= 0.2
    return np.clip(v, -1, 1)
