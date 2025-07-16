# Severe Weather Risk Messaging Analyzer 🌪️

A Python-based tool for analyzing and visualizing the clarity, urgency, and effectiveness of severe weather warning messages across multiple sources — including the National Weather Service (NWS), broadcast media, and mobile apps.

This project is designed to help researchers, emergency managers, and communicators understand how different messaging styles impact public perception and response during dangerous weather events.

---

##  Features

- NLP-powered analysis of warning text using spaCy and NLTK
- Sentiment scoring (VADER) and readability metrics (Flesch-Kincaid)
- Visualizations using Plotly + Streamlit UI
- Communication "Spectrum Score" to rate message effectiveness
- Upload your own warnings or paste custom text for instant feedback

---

## Tech Stack

- **Language**: Python 3.11+
- **Libraries**: 
  - `streamlit` for UI
  - `spaCy` for text cleaning and tokenization
  - `nltk` for sentiment + readability
  - `plotly` for charts
  - `pandas` for data manipulation
  - `wordcloud` for visual flair

---

## Installation

1. Clone the repo:

```bash
git clone https://github.com/yourusername/risk-messaging-analyzer.git
cd risk-messaging-analyzer

Create and activate virtual environment:

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Download NLTK datasets (only once):

bash
Copy
Edit
python -m nltk.downloader vader_lexicon punkt
Download the spaCy language model:

bash
Copy
Edit
python -m spacy download en_core_web_sm
▶️ Run the App
bash
Copy
Edit
streamlit run app/main.py


📂 Sample Datasets
Included in /data:

sample_warnings.csv: Collection of warning messages from:

NWS (official text)

Broadcast media (TV transcripts or quotes)

Mobile apps (push alerts)

Each row includes:

source (e.g., "NWS", "Broadcast", "App")

text (full warning message)

Want to contribute? Add your own examples!

🧠 Communication Spectrum Score
Each warning is scored on a composite scale combining:

✅ Readability: How easy is it to understand?

⚠️ Urgency: Does it trigger action?

😐 Sentiment: Does it feel neutral, alarming, or confusing?

The goal is not to shame sources but to visualize variation and suggest improvements in crisis communication.

👩‍💻 Contributing
Have data, feedback, or suggestions for metrics? PRs and issues are welcome!

📜 License
MIT License. Attribution encouraged for educational and research use.

🔗 Acknowledgments
National Weather Service

SpaCy & NLTK teams

Research inspired by risk communication literature