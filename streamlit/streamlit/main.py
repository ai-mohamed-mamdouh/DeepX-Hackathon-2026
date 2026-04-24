import streamlit as st
import pandas as pd
import json
from datetime import datetime
from streamlit_local_storage import LocalStorage

# Your existing functions
def send_to_model(text):
    # This is your mock function - replace with actual model call
    return {
        "aspects": ["delivery", "service"],
        "aspect_sentiments": {
            "delivery": "positive",
            "service": "negative"
        }
    }

def prepare_json(review_id, text):
    aspects_and_sentiments = send_to_model(text)
    return {
        "review_id": review_id,
        "aspects": aspects_and_sentiments["aspects"],
        "aspect_sentiments": aspects_and_sentiments["aspect_sentiments"]
    }

# Set page configuration
st.set_page_config(
    page_title="Aspect-Based Sentiment Analysis",
    page_icon="🎯",
    layout="wide"
)

# Initialize LocalStorage
ls = LocalStorage()

# Custom CSS for beautiful design
st.markdown("""
    <style>
    /* Main container styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        margin-top: 0.5rem;
        font-size: 1.1rem;
    }
    
    /* Card styling */
    .result-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        transition: transform 0.2s;
    }
    
    .result-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    /* Sentiment badges */
    .sentiment-positive {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        color: white;
        font-weight: bold;
        display: inline-block;
        font-size: 0.85rem;
    }
    
    .sentiment-negative {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        color: white;
        font-weight: bold;
        display: inline-block;
        font-size: 0.85rem;
    }
    
    .sentiment-neutral {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        color: white;
        font-weight: bold;
        display: inline-block;
        font-size: 0.85rem;
    }
    
    /* Aspect item styling */
    .aspect-item {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 0.8rem;
        margin: 0.5rem 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .aspect-name {
        font-weight: 600;
        color: #333;
        font-size: 1rem;
    }
    
    /* Input area styling - FULL WIDTH */
    .input-container {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 2rem;
        margin-bottom: 2rem;
        width: 100%;
    }
    
    /* Stats styling */
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        color: white;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* History item */
    .history-item {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid #e0e0e0;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .history-item:hover {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        background: linear-gradient(to right, #667eea, #764ba2);
        height: 2px;
    }
    
    /* Make text area full width */
    .stTextArea > div {
        width: 100% !important;
    }
    
    /* Ensure full width for main content */
    .main .block-container {
        max-width: 100% !important;
        padding: 1rem 2rem !important;
    }
    
    /* Remove the second column for history section */
    .reportview-container .main .block-container {
        max-width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Load history from local storage on startup
def load_history_from_storage():
    stored_history = ls.getItem("sentiment_history")
    if stored_history is not None:
        # Convert string back to list of dictionaries
        try:
            history_data = json.loads(stored_history) if isinstance(stored_history, str) else stored_history
            # Convert timestamp strings back to datetime objects
            for item in history_data:
                if 'timestamp' in item and isinstance(item['timestamp'], str):
                    item['timestamp'] = datetime.fromisoformat(item['timestamp'])
            return history_data
        except:
            return []
    return []

# Save history to local storage
def save_history_to_storage(history):
    # Convert datetime objects to strings for JSON serialization
    history_serializable = []
    for item in history:
        item_copy = item.copy()
        if 'timestamp' in item_copy:
            item_copy['timestamp'] = item_copy['timestamp'].isoformat()
        history_serializable.append(item_copy)
    ls.setItem("sentiment_history", json.dumps(history_serializable))

# Initialize session state for history
if 'history' not in st.session_state:
    st.session_state.history = load_history_from_storage()
if 'review_count' not in st.session_state:
    st.session_state.review_count = len(st.session_state.history)

# Header
st.markdown("""
    <div class="main-header">
        <h1>🎯 Aspect-Based Sentiment Analysis</h1>
        <p>Analyze customer reviews and extract aspect-specific sentiments</p>
    </div>
""", unsafe_allow_html=True)

# Remove columns - use full width layout
st.markdown("### 📝 Enter Your Review")

# Create tabs for better organization
tab1, tab2 = st.tabs(["📝 New Review", "📊 Review History"])

with tab1:
    # Text input area - full width
    user_input = st.text_area(
        "Write your review here:",
        height=150,
        placeholder="e.g., The delivery was incredibly fast, but the customer service was disappointing...",
        key="review_input",
        help="Enter your customer review text here for aspect-based sentiment analysis"
    )
    
    # Analyze button - centered with full width option
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        analyze_button = st.button("🔍 Analyze Sentiment", use_container_width=True)
    
    # Analysis logic
    if analyze_button and user_input:
        with st.spinner("Analyzing sentiment..."):
            # Simulate processing delay (remove in production)
            import time
            time.sleep(1)
            
            # Call your model
            review_id = f"review_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            result = prepare_json(review_id, user_input)
            
            # Save to history
            st.session_state.history.append({
                'timestamp': datetime.now(),
                'review_text': user_input,
                'result': result
            })
            st.session_state.review_count += 1
            
            # Save to local storage
            save_history_to_storage(st.session_state.history)
            
            # Display results
            st.markdown("---")
            st.markdown("### ✨ Analysis Results")
            
            # Create two columns for results display
            res_col1, res_col2 = st.columns([1, 1])
            
            with res_col1:
                st.markdown(f"""
                    <div class="result-card">
                        <h4 style="color: black;">📋 Review Text</h4>
                        <p style="color: #666;">{user_input}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with res_col2:
                # Display aspects and sentiments
                for aspect in result['aspects']:
                    sentiment = result['aspect_sentiments'][aspect]
                    sentiment_class = f"sentiment-{sentiment}"
                    
                    st.markdown(f"""
                        <div class="aspect-item">
                            <span class="aspect-name">📌 {aspect.capitalize()}</span>
                            <span class="{sentiment_class}">{sentiment.upper()} ✨</span>
                        </div>
                    """, unsafe_allow_html=True)
            
            # Overall sentiment summary
            sentiments = list(result['aspect_sentiments'].values())
            positive_count = sentiments.count('positive')
            negative_count = sentiments.count('negative')
            neutral_count = sentiments.count('neutral')
            
            if positive_count > negative_count and positive_count > neutral_count:
                overall = "🟢 Mostly Positive"
            elif negative_count > positive_count and negative_count > neutral_count:
                overall = "🔴 Mostly Negative"
            elif neutral_count > positive_count and neutral_count > negative_count:
                overall = "⚪ Mostly Neutral"
            else:
                overall = "🟡 Balanced"
            
            st.markdown(f"""
                <div class="result-card">
                    <h4 style="color: black;">📊 Overall Assessment</h4>
                    <p style="color: black; font-size: 1.2rem;"><strong>{overall}</strong></p>
                    <p style="color: black;">✅ Positive: {positive_count} | ❌ Negative: {negative_count} | ⚪ Neutral: {neutral_count}</p>
                </div>
            """, unsafe_allow_html=True)
    
    elif analyze_button and not user_input:
        st.warning("⚠️ Please enter some text to analyze!")

with tab2:
    # Display history in a more compact way
    if st.session_state.history:
        st.markdown(f"### 📜 Review History ({len(st.session_state.history)} reviews)")
        
        # # Add clear history button
        # if st.button("🗑️ Clear All History", use_container_width=True):
        #     st.session_state.history = []
        #     st.session_state.review_count = 0
        #     save_history_to_storage(st.session_state.history)
        #     st.rerun()
        
        # Display history items
        for idx, review in enumerate(reversed(st.session_state.history)):
            with st.expander(f"Review from {review['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"):
                st.markdown(f"**Review Text:** {review['review_text'][:200]}")
                st.markdown("**Aspects Found:**")
                for aspect in review['result']['aspects']:
                    sentiment = review['result']['aspect_sentiments'][aspect]
                    st.markdown(f"- {aspect.capitalize()}: {sentiment.upper()}")
    else:
        st.info("No reviews analyzed yet. Go to the 'New Review' tab to get started!")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🎯 Aspect-Based Sentiment Analysis Tool | Powered by Streamlit</p>
    </div>
""", unsafe_allow_html=True)