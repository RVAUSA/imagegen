import streamlit as st

st.set_page_config(page_title="Handbag Model Trainer", layout="wide")

st.title("👜 Train Your First AI Model")

uploaded_files = st.file_uploader(
    "Upload 10–30 photos of your handbag",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} images uploaded successfully.")
    # In a real app, you'd now send these to Runware's backend API

    if st.button("Start Training"):
        st.info("⏳ Training in progress... (this would connect to Runware API)")
        # Placeholder — backend call goes here
        st.success("✅ Model trained successfully!")

prompt = st.text_input("Enter a prompt to generate new images")

if prompt:
    if st.button("Generate Images"):
        st.info("🧠 Generating images from model...")
        # Placeholder — real API call would go here
        st.image("https://placekitten.com/400/400", caption="Generated Image", width=300)
