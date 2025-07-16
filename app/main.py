import streamlit as st
import pandas as pd
import plotly.express as px
from text_analysis import analyze_warning

st.title("Severe Weather Risk Messaging Analyzer")

@st.cache_data
def load_data():
    return pd.read_csv("data/sample_warnings.csv", parse_dates=["date"])

data = load_data()

st.sidebar.header("Filters")
sources = data['source'].unique().tolist()
selected_sources = st.sidebar.multiselect("Select sources", options=sources, default=sources)

dates = data['date'].dt.date.unique()
selected_dates = st.sidebar.multiselect("Select dates", options=dates, default=dates)

filtered_data = data[
    (data['source'].isin(selected_sources)) &
    (data['date'].dt.date.isin(selected_dates))
].copy()

# Run analysis pipeline on each warning text
analysis_results = filtered_data['text'].apply(analyze_warning)
analysis_df = pd.json_normalize(analysis_results)
filtered_data = pd.concat([filtered_data.reset_index(drop=True), analysis_df], axis=1)

st.write(f"### Filtered Data with Analysis ({len(filtered_data)} rows)")
st.dataframe(filtered_data)

# Sorting option
sort_option = st.sidebar.selectbox("Sort by", options=['date', 'compound', 'fk_grade'], index=0)
filtered_data = filtered_data.sort_values(by=sort_option, ascending=(sort_option != 'date'))

# Visualization
fig_sentiment = px.box(filtered_data, x='source', y='compound',
                       title="Sentiment Compound Score Distribution by Source",
                       points="all")
st.plotly_chart(fig_sentiment, use_container_width=True)

fig_readability = px.box(filtered_data, x='source', y='fk_grade',
                         title="Readability (Flesch-Kincaid Grade) Distribution by Source",
                         points="all")
st.plotly_chart(fig_readability, use_container_width=True)




import datetime

st.sidebar.header("Filters")

# Date range filter
min_date = data['date'].min().date()
max_date = data['date'].max().date()
date_range = st.sidebar.date_input("Select date range", [min_date, max_date], min_value=min_date, max_value=max_date)

# Convert date range selection to filter data
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = min_date
    end_date = max_date

# Filter data by date range
filtered_data = filtered_data[
    (filtered_data['date'].dt.date >= start_date) &
    (filtered_data['date'].dt.date <= end_date)
]

# Sentiment compound score slider
compound_min, compound_max = float(filtered_data['compound'].min()), float(filtered_data['compound'].max())
compound_range = st.sidebar.slider("Sentiment Compound Score Range", compound_min, compound_max, (compound_min, compound_max))

filtered_data = filtered_data[
    (filtered_data['compound'] >= compound_range[0]) &
    (filtered_data['compound'] <= compound_range[1])
]

# Readability (Flesch-Kincaid Grade) slider
fk_min, fk_max = float(filtered_data['fk_grade'].min()), float(filtered_data['fk_grade'].max())
fk_range = st.sidebar.slider("Readability Grade Level Range", fk_min, fk_max, (fk_min, fk_max))

filtered_data = filtered_data[
    (filtered_data['fk_grade'] >= fk_range[0]) &
    (filtered_data['fk_grade'] <= fk_range[1])
]



fig_time = px.line(filtered_data, x='date', y='compound', color='source',
                   title="Sentiment Compound Score Over Time by Source",
                   markers=True)
st.plotly_chart(fig_time, use_container_width=True)


from wordcloud import WordCloud
import matplotlib.pyplot as plt

def plot_wordcloud(text, title):
    wordcloud = WordCloud(width=600, height=400, background_color='white').generate(text)
    plt.figure(figsize=(8,5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    st.pyplot(plt)

# Example usage:
# plot_wordcloud("some example text", "Example Word Cloud")
from text_analysis import compute_spectrum_score

filtered_data['spectrum_score'] = filtered_data.apply(lambda row: compute_spectrum_score(row), axis=1)

st.write("### Communication Spectrum Scores")
st.dataframe(filtered_data[['text', 'source', 'spectrum_score']].sort_values(by='spectrum_score', ascending=False))

fig_spectrum = px.box(filtered_data, x='source', y='spectrum_score',
                      title="Risk Communication Spectrum Scores by Source",
                      points="all")
st.plotly_chart(fig_spectrum, use_container_width=True)

st.header("Analyze Your Own Warning Message")

user_text = st.text_area("Paste or type a warning message here:")

if user_text:
    user_analysis = analyze_warning(user_text)
    user_spectrum_score = compute_spectrum_score(user_analysis)

    st.subheader("Analysis Results:")
    st.write(f"**Cleaned Text:** {user_analysis['cleaned_text']}")
    st.write(f"**Sentiment Scores:** {user_analysis['compound']:.3f} (compound), positive: {user_analysis['pos']:.3f}, neutral: {user_analysis['neu']:.3f}, negative: {user_analysis['neg']:.3f}")
    st.write(f"**Readability:** Flesch-Kincaid Grade = {user_analysis['fk_grade']:.2f}, Reading Ease = {user_analysis['reading_ease']:.2f}")
    st.write(f"**Communication Spectrum Score:** {user_spectrum_score:.3f}")
if st.button("Analyze Warning"):
    if user_text.strip():
        user_analysis = analyze_warning(user_text)
        user_spectrum_score = compute_spectrum_score(user_analysis)
        # (same display code as above)
    else:
        st.warning("Please enter a warning message to analyze.")
