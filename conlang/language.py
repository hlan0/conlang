import numpy as np
import warnings

from typing import List, Optional
from .swadesh import SWADESH
from .vocabulary import Vocabulary
from .language_config import LanguageConfig
from .word import Word
from .utils import is_acceptable


MAX_ATTEMPTS = 10


class Language:
    """
    Represents a language, including its configuration and vocabulary.

    Attributes:
        name (str): The name of the language.
        config (LanguageConfig): The configuration for phonemes, patterns, and stress.
        vocabulary (Vocabulary): The generated vocabulary for the language.
    """
    def __init__(self, name: str, config: LanguageConfig, vocabulary: Optional[Vocabulary] = None):
        self.name = name
        self.config = config
        self.vocabulary = vocabulary or Vocabulary()

    def generate_word(self, rank: int = -1) -> str:
        """
        Generates a word based on the language's configuration and word frequency rank.

        Args:
            rank (int): The rank of the word for frequency purposes. Defaults to -1.

        Returns:
            str: The generated word.
        """
        # Select a pattern based on rank (common words have simpler patterns)
        patterns = self.config.patterns[:2] if 0 <= rank < 25 else self.config.patterns
        pattern = np.random.choice(patterns)

        word = Word(''.join(np.random.choice(self.config.phonemes[k]) for k in pattern))

        stressed_index = np.random.choice(self.config.stress)
        word.set_stress(stressed_index)

        return word

    def generate_vocabulary(self, glosses: Optional[List[str]] = None):
        """
        Generates a vocabulary for the language based on glosses.

        Args:
            glosses (List[str], optional): A list of glosses to use for the vocabulary. 
                                           Defaults to the SWADESH list.
        """
        self.vocabulary = Vocabulary()

        glosses = glosses or SWADESH

        for gloss in glosses:
            rank = SWADESH.index(gloss) if gloss in SWADESH else -1
            attempts = 0

            while attempts < MAX_ATTEMPTS:
                word = self.generate_word(rank=rank)
                if is_acceptable(word) and not self.vocabulary.has_word(word):
                    break
                attempts += 1
            self.vocabulary.add_item(word, gloss)

            if attempts == MAX_ATTEMPTS:
                warnings.warn(f"Failed to generate unique acceptable word for '{gloss}'. Please, check your configuration.")

    def __str__(self) -> str:
        """
        Returns a string representation of the language.
        """
        return f"{self.name}\n\n{self.config}\n\n{self.vocabulary}"

    def __repr__(self):
        """
        Returns a string representation of the language.
        """
        return self.__str__()

    @staticmethod
    def from_vocabulary(name: str, vocabulary: Vocabulary) -> 'Language':
        """
        Create a new Language instance from a vocabulary.

        Args:
            name (str): The name of the language.
            vocabulary (Vocabulary): The vocabulary for the language.

        Returns:
            Language: A new Language instance.
        """
        config = LanguageConfig.from_vocabulary(vocabulary)
        return Language(name, config, vocabulary)
