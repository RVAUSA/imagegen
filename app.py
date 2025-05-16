import streamlit as st
import requests
import base64
import json

st.set_page_config(page_title="Runware Training", layout="centered")

st.title("👜 Fine-Tune Your Handbag Model")
st.write("Upload a few reference images to train a custom AI model using Runware.")

# Image type selector
image_type = st.selectbox("Select image type for training", ["Hero", "Detail", "Lifestyle"])

# Image uploader
uploaded_images = st.file_uploader(
    "Upload training images (JPG or PNG)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# Show thumbnails
if uploaded_images:
    st.subheader("Preview of Uploaded Images:")
    for img in uploaded_images:
        st.image(img, width=200)

# Train Model button
if st.button("🚀 Train Model"):
    if not uploaded_images:
        st.warning("Please upload at least one image before training.")
        st.stop()

    st.info("Sending images to Runware for training...")

    # Convert uploaded images to base64 strings
    base64_images = []
    for img in uploaded_images:
        img_bytes = img.read()
        encoded = base64.b64encode(img_bytes).decode("utf-8")
        base64_images.append({
            "filename": img.name,
            "data": encoded,
            "mime_type": img.type
        })

    # Build the task array as per Runware API
    tasks = [
        {"auth": {"apiKey": st.secrets["runware"]["api_key"]}},
        {
            "type": "train_kohya",
            "model_name": "test_handbag_lora",
            "image_type": image_type,
            "images": base64_images
        }
    ]

    try:
        response = requests.post(
            "https://api.runware.ai/v1",
            json=tasks,
            timeout=120
        )

        if response.status_code == 200:
            st.success("✅ Training started successfully!")
        else:
            try:
                error_details = response.json().get("errors", "Unknown error")
            except Exception:
                error_details = response.text

            st.error(f"❌ Training failed: {error_details}")
            st.write(f"Status code: {response.status_code}")
            st.write(f"Raw response: {response.content}")

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
