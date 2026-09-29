# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""

import re
import string
from typing import List, Dict, Tuple, Optional

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS

# Common text emoticons, longest first so e.g. ":-)" matches before ":)"
# would even get a chance to grab just part of it.
_EMOTICONS = sorted(
    [":)", ":-)", ":(", ":-(", ":'(", ":')", ";)", ";-)", ":d", ":-d", ":p", ":-p", ":/", ":-/"],
    key=len,
    reverse=True,
)
EMOTICON_PATTERN = re.compile("|".join(re.escape(e) for e in _EMOTICONS))

# Broad ranges covering most common unicode emoji (🥲, 😂, 💀, etc.).
UNICODE_EMOJI_PATTERN = re.compile("[\U0001F300-\U0001FAFF☀-➿]")

# Words that flip the sentiment of the token right after them
# ("not happy" -> negative). Written without apostrophes because
# preprocess() strips punctuation before these are checked.
NEGATION_WORDS = {
    "not", "no", "never", "cant", "dont", "wont", "isnt",
    "wasnt", "arent", "couldnt", "shouldnt", "wouldnt", "cannot",
}


class MoodAnalyzer:
    """
    A very simple, rule based mood classifier.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        # Use the default lists from dataset.py if none are provided.
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        # Store as sets for faster lookup.
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens the model can work with.

        TODO: Improve this method.

        Right now, it does the minimum:
          - Strips leading and trailing whitespace
          - Converts everything to lowercase
          - Splits on spaces

        Ideas to improve:
          - Remove punctuation
          - Handle simple emojis separately (":)", ":-(", "🥲", "😂")
          - Normalize repeated characters ("soooo" -> "soo")
        """
        cleaned = text.strip().lower()

        # Pull emoticons out first (e.g. ":)" or ":-(") so stripping
        # punctuation below doesn't destroy them, and space-pad unicode
        # emoji (e.g. "🥲") so they split into their own tokens even when
        # glued to a word, like "great😂".
        emoticons = EMOTICON_PATTERN.findall(cleaned)
        cleaned = EMOTICON_PATTERN.sub(" ", cleaned)
        cleaned = UNICODE_EMOJI_PATTERN.sub(r" \g<0> ", cleaned)

        # Now it's safe to strip the remaining punctuation.
        cleaned = cleaned.translate(str.maketrans("", "", string.punctuation))

        tokens = cleaned.split() + emoticons

        # Normalize repeated characters ("soooo" -> "soo") so minor
        # spelling variations still match the word lists.
        tokens = [re.sub(r"(.)\1{2,}", r"\1\1", token) for token in tokens]

        return tokens

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def score_text(self, text: str) -> int:
        """
        Compute a numeric "mood score" for the given text.

        Positive words add 1, negative words subtract 1. A word immediately
        after a negation word (NEGATION_WORDS, e.g. "not", "never") has its
        sign flipped instead, so "not happy" subtracts and "not bad" adds.

        Negation only looks one token ahead, so "not very happy" misses the
        flip ("very" isn't a sentiment word, so it resets the negation
        before "happy" is checked). Catching that would mean carrying the
        negation across non-sentiment words, which is more correct but
        harder to read and reason about than this one-word window.
        """
        tokens = self.preprocess(text)
        score = 0
        negated = False

        for token in tokens:
            if token in NEGATION_WORDS:
                negated = True
                continue

            if token in self.positive_words:
                score += -1 if negated else 1
            elif token in self.negative_words:
                score += 1 if negated else -1

            negated = False

        return score

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Turn the numeric score for a piece of text into a mood label.

        The default mapping is:
          - score > 0  -> "positive"
          - score < 0  -> "negative"
          - score == 0 -> "neutral"

        TODO: You can adjust this mapping if it makes sense for your model.
        For example:
          - Use different thresholds (for example score >= 2 to be "positive")
          - Add a "mixed" label for scores close to zero
        Just remember that whatever labels you return should match the labels
        you use in TRUE_LABELS in dataset.py if you care about accuracy.
        """
        # TODO: Implement this method.
        #   1. Call self.score_text(text) to get the numeric score.
        #   2. Return "positive" if the score is above 0.
        #   3. Return "negative" if the score is below 0.
        #   4. Return "neutral" otherwise.
        pass

    # ---------------------------------------------------------------------
    # Explanations (optional but recommended)
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """
        Return a short string explaining WHY the model chose its label.

        TODO:
          - Look at the tokens and identify which ones counted as positive
            and which ones counted as negative.
          - Show the final score.
          - Return a short human readable explanation.

        Example explanation (your exact wording can be different):
          'Score = 2 (positive words: ["love", "great"]; negative words: [])'

        The current implementation is a placeholder so the code runs even
        before you implement it.
        """
        tokens = self.preprocess(text)

        positive_hits: List[str] = []
        negative_hits: List[str] = []
        score = 0

        for token in tokens:
            if token in self.positive_words:
                positive_hits.append(token)
                score += 1
            if token in self.negative_words:
                negative_hits.append(token)
                score -= 1

        return (
            f"Score = {score} "
            f"(positive: {positive_hits or '[]'}, "
            f"negative: {negative_hits or '[]'})"
        )
