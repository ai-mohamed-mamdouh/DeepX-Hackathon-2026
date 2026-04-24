import streamlit as st

# Example inference function
def run_inference(text):
    # TODO: implement your model here
    return {"label": "example_label", "score": 0.99}

st.set_page_config(page_title="Text Classifier", page_icon="📄")

st.title("📄 Text Classifier")

text = st.text_area("Enter text", height=180)

if st.button("Predict"):
    if text.strip():
        with st.spinner("Processing..."):
            output = run_inference(text)

        st.success("Prediction completed")

        if isinstance(output, dict):
            st.write("**Label:**", output.get("label"))
            st.write("**Score:**", output.get("score"))
        else:
            st.write(output)
    else:
        st.error("Please enter some text first.")