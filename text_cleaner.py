import re
import string
import pandas as pd
from typing import Iterable
from nltk.tokenize import RegexpTokenizer


class Tokenizer:
    """tokenize text into words using a regular expression-based tokenizer
    """
    def __init__(self) -> None:
        self.tokenizer = RegexpTokenizer("[\w']+")

    def word_tokenizer(self, text) -> Iterable:
        """Tokenizes the input text into words

        Args:
            text (str): The text to be tokenized.

        Returns:
            Iterable: A list of tokens (words).
        """
        return self.tokenizer.tokenize(text)


class TextCleaner(Tokenizer):
    """A class for cleaning text data, extending the Tokenizer
    """
    def __init__(self) -> None:
        """Initialize the TextCleaner class by loading the acronyms and contractions dictionaries.
        """
        super().__init__()

        # the acronyms url
        self._acronyms_url = "https://raw.githubusercontent.com/sugatagh/E-commerce-Text-Classification/main/JSON/english_acronyms.json"

        # link to data where contractios list is present
        self._contractions_url = "https://raw.githubusercontent.com/sugatagh/E-commerce-Text-Classification/main/JSON/english_contractions.json"

        # load the acronym dict
        self._acronyms_dict = self.load_acronym()
        # load acronym list
        self._acronym_list = list(self._acronyms_dict.keys())

        # load the contractions dict
        self._contractions_dict = self.load_contractions()
        # load contractions list
        self._contractions_list = list(self._contractions_dict.keys())

    def load_acronym(self) -> pd.Series:
        """Loads the acronyms dictionary from the specified URL.
        Returns:
            pd.Series: Retrun dictionary as pandas series.
        """
        return pd.read_json(self._acronyms_url, typ="series")

    def load_contractions(self):
        """Loads the contractions dictionary from the specified URL.
        Returns:
            pd.Series: Retrun dictionary as pandas series.
        """
        return pd.read_json(self._contractions_url, typ="series")

    # Converting to lowercase
    def convert_to_lowercase(self, text):
        return text.lower()

    # remove whitespace from the text
    def remove_whitespace(self, text):
        return text.strip()

    # Removing punctuations from the given string
    def remove_punctuation(self, text):
        # get all the punctuations
        punct_str = string.punctuation

        # the apostrophe will be remove using contraction.
        punct_str = punct_str.replace("'", "")
        return text.translate(str.maketrans("", "", punct_str))

    # Remove any HTML if present in the text.
    def remove_html(self, text):
        html = re.compile(r"<.*?>")
        return html.sub(r"", text)

    # Remove URLs
    def remove_http(self, text):
        http = "https?://\S+|www\.\S+"  # matching strings beginning with http (but not just "http")
        pattern = r"({})".format(http)  # creating pattern
        return re.sub(pattern, "", text)

    # Remove any Emojis present in the text.
    def remove_emoji(self, text):
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+",
            flags=re.UNICODE,
        )
        return emoji_pattern.sub(r"", text)

    def convert_acronyms(self, text):
        words = []
        for word in self.word_tokenizer(text):
            if word in self._acronym_list:
                words = words + self._acronyms_dict[word].split()
            else:
                words = words + word.split()

        text_converted = " ".join(words)
        return text_converted

    def convert_contractions(self, text):
        words = []
        for word in self.word_tokenizer(text):
            if word in self._contractions_list:
                words = words + self._contractions_dict[word].split()
            else:
                words = words + word.split()

        text_converted = " ".join(words)
        return text_converted

    def __call__(self, text):
        """
        Cleans the input text.
        Applies a series of preprocessing steps, including:
        converting to lowercase, removing whitespace, punctuation, HTML tags, URLs, and emojis,
        and converting acronyms and contractions to their expanded forms.
        Args:
            text (str): The text to be cleaned.

        Returns:
            str: The cleaned text.
        """
        text = self.convert_to_lowercase(text=text)
        text = self.remove_whitespace(text=text)
        text = self.remove_html(text=text)
        text = self.remove_http(text=text)
        text = self.remove_punctuation(text=text)
        text = self.remove_emoji(text=text)
        text = self.convert_acronyms(text=text)
        text = self.convert_contractions(text=text)

        return text
    

