import re
import pandas as pd


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text):
    text = str(text).lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# ============================================================
# CLASSIFIER
# ============================================================

def classify_comment(comment):

    text = clean_text(comment)

    # --------------------------------------------------------
    # 1. SPAM
    # --------------------------------------------------------

    spam_patterns = [
        "subscribe my channel",
        "subscribe to my channel",
        "check my channel",
        "visit my channel",
        "visit my profile",
        "earn money",
        "make money",
        "free giveaway",
        "click here",
        "buy now",
        "promo code",
        "discount code",
        "whatsapp me",
        "telegram me",
        "dm me",
        "follow my channel",
        "follow me",
        "support my channel",
        "watch my video",
        "watch my channel"
    ]

    if any(pattern in text for pattern in spam_patterns):
        return "Spam"


    # --------------------------------------------------------
    # 2. TOXIC
    # --------------------------------------------------------

    toxic_words = [
        "idiot",
        "moron",
        "stupid",
        "dumb",
        "loser",
        "fool",
        "shut up",
        "hate you",
        "fuck you",
        "bastard",
        "trash",
        "useless",
        "mental",
        "mad fellow",
        "loosu",
        "punda",
        "thevdiya",
        "baadu",
        "kiruku"
    ]

    if any(word in text for word in toxic_words):
        return "Toxic"


    # --------------------------------------------------------
    # 3. QUESTION
    # --------------------------------------------------------

    question_words = [
        "why",
        "what",
        "when",
        "where",
        "who",
        "which",
        "how",
        "can you",
        "is this",
        "does this",
        "did he",
        "did she",
        "enna",
        "yen",
        "eppadi",
        "eppo",
        "enga",
        "engae",
        "yaaru",
        "epdi",
        "ennaku"
    ]

    # Strong question indicators
    if "?" in text:
        return "Question"

    if any(text.startswith(word + " ") for word in question_words):
        return "Question"


    # --------------------------------------------------------
    # 4. SUGGESTION
    # --------------------------------------------------------

    suggestion_patterns = [

        # English
        "should",
        "could",
        "please make",
        "please add",
        "please show",
        "please explain",
        "try to",
        "you can improve",
        "need to improve",
        "i suggest",
        "suggestion",
        "recommend",
        "would be better",
        "it would be better",
        "next time",

        # Tamil / Tanglish
        "vachirukalam",
        "vechirukalam",
        "vachirundha",
        "vechirundha",
        "irukkanum",
        "irukanum",
        "pannalam",
        "panlam",
        "pannanum",
        "pannanum",
        "maathanum",
        "mathanum",
        "serkanum",
        "serkanum",
        "kondu varalam",
        "next video",
        "adutha video",
        "innum better",
        "better ah",
        "improve pannunga",
        "improve pannanum"
    ]

    if any(pattern in text for pattern in suggestion_patterns):
        return "Suggestion"


    # --------------------------------------------------------
    # 5. NEGATIVE
    # --------------------------------------------------------

    negative_words = [
        "bad",
        "poor",
        "worst",
        "hate",
        "terrible",
        "awful",
        "boring",
        "disappointing",
        "disappointed",
        "waste",
        "waste of time",
        "not good",
        "not nice",
        "not useful",
        "useless",
        "worst movie",
        "worst video",
        "boring video",

        # Tanglish
        "mokka",
        "semma mokka",
        "sothappal",
        "nalla illa",
        "nalla varala",
        "pidikala",
        "pudikala",
        "mosam",
        "romba mosam",
        "sari illa",
        "wasteu",
        "waste ah"
    ]

    # Negation + positive word
    negative_phrases = [
        "not good",
        "not great",
        "not amazing",
        "not nice",
        "not helpful",
        "not perfect",
        "isn't good",
        "isnt good",
        "wasn't good",
        "wasnt good"
    ]

    if any(phrase in text for phrase in negative_phrases):
        return "Negative"

    if any(word in text for word in negative_words):
        return "Negative"


    # --------------------------------------------------------
    # 6. POSITIVE
    # --------------------------------------------------------

    positive_words = [
        "good",
        "great",
        "excellent",
        "amazing",
        "helpful",
        "awesome",
        "beautiful",
        "nice",
        "cool",
        "best",
        "wonderful",
        "perfect",
        "fantastic",
        "super",
        "brilliant",
        "excellent video",
        "great video",
        "good video",
        "very good",
        "really good",
        "well explained",

        # Tanglish
        "nalla irukku",
        "nalla iruku",
        "romba nalla",
        "super ah",
        "semma",
        "mass",
        "vera level",
        "kalakkal",
        "arumai",
        "sirappu",
        "pinnita",
        "vera level video"
    ]

    if any(word in text for word in positive_words):
        return "Positive"


    # --------------------------------------------------------
    # 7. NEUTRAL
    # --------------------------------------------------------

    return "Neutral"


# ============================================================
# CLASSIFY DATAFRAME
# ============================================================

def classify_comments(df):

    df = df.copy()

    df["Category"] = df["Comment"].apply(
        classify_comment
    )

    df.to_csv(
        "data/classified_comments.csv",
        index=False
    )

    return df
