import streamlit as st
import pandas as pd
from aspect_inferance import predict_aspects
from sentiment_inferance import predict_sentiment

st.set_page_config(
    page_title="Aspect Sentiment Analyzer",
    page_icon="💬",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

.hero {
    padding: 35px;
    border-radius: 22px;
    background: linear-gradient(135deg, #1f2937, #111827);
    border: 1px solid #374151;
    margin-bottom: 25px;
}

.hero h1 {
    color: #ffffff;
    font-size: 42px;
    margin-bottom: 8px;
}

.hero p {
    color: #9ca3af;
    font-size: 18px;
}

.card {
    padding: 22px;
    border-radius: 18px;
    background-color: #111827;
    border: 1px solid #374151;
    margin-bottom: 16px;
}

.aspect-title {
    font-size: 22px;
    font-weight: 700;
    color: #ffffff;
}

.badge {
    padding: 6px 14px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 14px;
}

.positive {
    background-color: rgba(34, 197, 94, 0.15);
    color: #22c55e;
    border: 1px solid #22c55e;
}

.negative {
    background-color: rgba(239, 68, 68, 0.15);
    color: #ef4444;
    border: 1px solid #ef4444;
}

.neutral {
    background-color: rgba(234, 179, 8, 0.15);
    color: #eab308;
    border: 1px solid #eab308;
}

.confidence {
    color: #9ca3af;
    font-size: 15px;
    margin-top: 8px;
}
</style>
""", unsafe_allow_html=True)


def get_badge_class(sentiment):
    sentiment = sentiment.lower()

    if sentiment == "positive":
        return "positive"
    elif sentiment == "negative":
        return "negative"
    else:
        return "neutral"


st.markdown("""
<div class="hero">
    <h1>Aspect-Based Sentiment Analyzer</h1>
    <p>Analyze customer reviews, extract key aspects, and detect sentiment for each aspect.</p>
</div>
""", unsafe_allow_html=True)


with st.container():
    text = st.text_area(
        "Customer Review",
        placeholder="Type or paste a customer review here...",
        height=180
    )

    analyze_btn = st.button("Analyze Review", use_container_width=True)


if analyze_btn:
    if not text.strip():
        st.warning("Please enter a review before analyzing.")
    else:
        with st.spinner("Analyzing review..."):
            aspects = predict_aspects(text)

            results = []

            for aspect in aspects:
                sentiment_output = predict_sentiment(text, aspect)

                label = sentiment_output["label"]
                confidence = sentiment_output["confidence"]
                probs = sentiment_output["probs"]

                results.append({
                    "Aspect": aspect,
                    "Sentiment": label,
                    "Confidence": confidence,
                    "Negative": probs["negative"],
                    "Neutral": probs["neutral"],
                    "Positive": probs["positive"]
                })

        df = pd.DataFrame(results)

        st.markdown("## Analysis Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric("Detected Aspects", len(df))
        col2.metric("Positive", len(df[df["Sentiment"] == "positive"]))
        col3.metric("Negative", len(df[df["Sentiment"] == "negative"]))

        st.markdown("## Aspect Results")

        for item in results:
            sentiment = item["Sentiment"]
            badge_class = get_badge_class(sentiment)

            st.markdown(f"""
            <div class="card">
                <div class="aspect-title">{item["Aspect"].title()}</div>
                <br>
                <span class="badge {badge_class}">
                    {sentiment.upper()}
                </span>
                <div class="confidence">
                    Confidence: {item["Confidence"]:.2%}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("## Detailed Results")

        st.dataframe(
            df.style.format({
                "Confidence": "{:.2%}",
                "Negative": "{:.2%}",
                "Neutral": "{:.2%}",
                "Positive": "{:.2%}"
            }),
            use_container_width=True
        )

        st.markdown("## Sentiment Distribution")

        sentiment_counts = df["Sentiment"].value_counts()
        st.bar_chart(sentiment_counts)