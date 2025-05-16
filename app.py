import streamlit as st
import requests
import os
import base64
import json

st.set_page_config(page_title="Handbag AI Prototype", layout="centered")

st.title("👜 Handbag AI – Prototype V1")

# Sidebar
st.sidebar.header("Instructions")
st.sidebar.markdown("""
1. Upload 10–20 images of your handbag (same angle, lighting preferred).
2. Choose the image type: Hero Shot or Macro Detail.
3. Click **Train Model** to start training with Kohya-SS.
4. Once training finishes, enter a prompt to generate an image using ComfyUI.
""")

# Upload
st.subheader("📤 Upload Training Images")
image_type = st.selectbox("Select image type:", ["Hero", "Macro Detail"])
uploaded_images = st.file_uploader("Upload Images", accept_multiple_files=True, type=["jpg", "png"])

if uploaded_images:
    st.success(f"{len(uploaded_images)} image(s) uploaded as '{image_type}'.")

# Start training
if st.button("🚀 Train Model"):
    if not uploaded_images:
        st.warning("Please upload at least one image before training.")
        st.stop()

    st.info("Sending images to Runware for training...")

    # Prepare the payload according to Runware's new API spec
    tasks = [
        {"type": "auth", "token": st.secrets["runware"]["api_key"]},
        {
            "type": "train_kohya",
            "model_name": "test_handbag_lora",
            "image_type": image_type,
            "images": []
        }
    ]

    # Read images into memory and encode to base64 strings
    for img in uploaded_images:
        img_bytes = img.read()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        tasks[1]["images"].append({
            "filename": img.name,
            "content": img_base64,
            "content_type": img.type
        })

    try:
        response = requests.post(
            "https://api.runware.ai/v1",
            headers={"Content-Type": "application/json"},
            data=json.dumps(tasks),
            timeout=120
        )

        if response.status_code == 200:
            st.success("✅ Training started! Check back in a while to test generation.")
        else:
            try:
                error_msg = response.json().get("error", "No error message returned.")
            except Exception:
                error_msg = response.content.decode('utf-8')  # fallback

            st.error(f"❌ Training failed: {error_msg}")
            st.write(f"Status code: {response.status_code}")
            st.write(f"Raw response: {response.content.decode('utf-8')}")

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")


# Prompt-based generation
st.subheader("🎨 Generate Image (ComfyUI)")

prompt = st.text_input("Enter prompt (e.g., 'leather handbag in studio lighting')")

if st.button("🖼️ Generate Image"):
    st.info("Sending prompt to ComfyUI for generation...")

    gen_response = requests.post(
        "https://api.runware.ai/v1",
        headers={"Content-Type": "application/json"},
        data=json.dumps([
            {"type": "auth", "token": st.secrets["runware"]["api_key"]},
            {"type": "generate_comfyui", "model": "test_handbag_lora", "prompt": prompt}
        ]),
        timeout=120
    )

    if gen_response.status_code == 200:
        image_url = gen_response.json().get("image_url")
        if image_url:
            st.image(image_url, caption="Generated Image")
        else:
            st.error("No image URL returned from generation.")
    else:
        st.error("There was an error generating the image.")
        st.write(f"Status code: {gen_response.status_code}")
        st.write(f"Response content: {gen_response.content.decode('utf-8')}")
