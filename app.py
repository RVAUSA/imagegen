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

    # Encode images to base64
    images_b64 = []
    for img in uploaded_images:
        img_bytes = img.read()
        img_b64 = base64.b64encode(img_bytes).decode("utf-8")
        images_b64.append(img_b64)

    # Prepare the payload
    tasks = [
        {"auth": {"apiKey": st.secrets["runware"]["api_key"]}},
        {
            "type": "train_kohya",
            "model_name": "test_handbag_lora",
            "image_type": image_type,
            "images": images_b64
        }
    ]

    # Debug output
    st.write("✅ API key loaded")
    st.write("📦 Payload being sent:")
    st.json(tasks[1])

    try:
        response = requests.post(
            "https://api.runware.ai/v1",
            headers={"Content-Type": "application/json"},
            data=json.dumps(tasks),
            timeout=120
        )

        if response.status_code == 200:
            st.success("✅ Training started! Check back later to test generation.")
        else:
            try:
                error_msg = response.json().get("errors", response.text)
            except Exception:
                error_msg = response.text

            st.error(f"❌ Training failed: {error_msg}")
            st.write(f"Status code: {response.status_code}")
            st.write(f"Raw response: {response.content}")

    except Exception as e:
        st.error(f"Unexpected error: {e}")
