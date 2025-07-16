import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import textstat

analyzer = SentimentIntensityAnalyzer()

def clean_text(text):
    """Basic cleaning: lowercase, remove extra spaces, strip punctuation."""
    text = text.lower()
    # Remove punctuation except sentence-ending punctuation to keep readability scoring accurate
    text = re.sub(r'[^\w\s.!?]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_sentiment_scores(text):
    """Return sentiment dictionary from VADER."""
    return analyzer.polarity_scores(text)

def get_readability_scores(text):
    """Return Flesch-Kincaid grade and reading ease scores."""
    return {
        'fk_grade': textstat.flesch_kincaid_grade(text),
        'reading_ease': textstat.flesch_reading_ease(text)
    }

def analyze_warning(text):
    """Full pipeline: clean text, get sentiment & readability."""
    cleaned = clean_text(text)
    sentiment = get_sentiment_scores(cleaned)
    readability = get_readability_scores(cleaned)

    return {
        'cleaned_text': cleaned,
        **sentiment,
        **readability
    }

def compute_spectrum_score(analysis):
    """
    Compute a composite score representing communication quality.

    Parameters:
    - analysis: dict with keys 'compound' (sentiment), 'fk_grade' (readability), etc.

    Returns:
    - float: score where higher means clearer/more effective communication.
    """

    # Example weights (tune these as you test)
    sentiment_weight = 0.4  # positive compound sentiment favors clarity
    readability_weight = 0.4  # lower grade level = easier to understand
    urgency_weight = 0.2  # you could score presence of urgent words separately

    # Normalize readability: lower FK grade means easier
    # Invert FK grade so low grade = high score
    max_grade = 16  # typical max school grade level for FK
    readability_score = max(0, (max_grade - analysis.get('fk_grade', max_grade))) / max_grade

    sentiment_score = max(0, analysis.get('compound', 0))  # VADER compound is between -1 and 1

    # For urgency: example dummy score — improve later by keyword detection
    urgency_score = 0.5  # placeholder constant

    composite_score = (sentiment_weight * sentiment_score +
                       readability_weight * readability_score +
                       urgency_weight * urgency_score)
    return composite_score
