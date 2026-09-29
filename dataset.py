"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
SAMPLE_POSTS += [
    "Lowkey stressed but kind of proud of myself",
    "no cap this is the best day ever 😂",
    "I absolutely love getting stuck in traffic",
    "highkey done with this week fr",
    "just chilling, nothing special :)",
    "I'm fine I guess 🙃",
    "lost my job today but at least I have my friends",
    "ugh Mondays 💀",
]

TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
    "mixed",     # "Lowkey stressed but kind of proud of myself"
    "positive",  # "no cap this is the best day ever 😂"
    "negative",  # "I absolutely love getting stuck in traffic" (sarcasm)
    "negative",  # "highkey done with this week fr"
    "positive",  # "just chilling, nothing special :)"
    "mixed",     # "I'm fine I guess 🙃" (ambiguous, sounds unconvinced)
    "mixed",     # "lost my job today but at least I have my friends"
    "negative",  # "ugh Mondays 💀"
]

# Remember to keep them aligned:
#   len(SAMPLE_POSTS) == len(TRUE_LABELS)
assert len(SAMPLE_POSTS) == len(TRUE_LABELS)
