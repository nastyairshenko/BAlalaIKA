import numpy as np

# Простейшее слабое семантическое пространство (weak semantic map)
# Оси: Valence, Arousal, Dominance (VAD) — каноника для eBICA-подобных карт.
VAD_DIM = 3

def zero_vad():
    return np.zeros(VAD_DIM, dtype=float)
