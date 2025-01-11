import numpy as np

from .presets import PRESETS


class LanguageConfig:
    def __init__(self, phonemes: dict, patterns: list, stress: list):
        self.phonemes = phonemes
        self.patterns = patterns
        self.stress = stress

    @staticmethod
    def from_txt(file_path: str) -> 'LanguageConfig':
        phonemes = {}
        patterns = []
        stress = []

        with open(file_path, 'r') as f:
            for line in f:
                if ':' in line:
                    line = line.split(':')
                    phonemes[line[0]] = line[1].strip().split()
                elif '-' in line:
                    stress.extend(line.strip().split())
                elif line.isupper():
                    patterns.extend(line.strip().split())

        stress = [int(s) for s in stress]

        return LanguageConfig(phonemes, patterns, stress)

    @staticmethod
    def random() -> 'LanguageConfig':
        preset = PRESETS[np.random.choice(list(PRESETS.keys()))]
        return LanguageConfig(preset['phonemes'], preset['patterns'], preset['stress'])
