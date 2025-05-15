import streamlit as st
import requests
import os

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
    st.info("Sending images to Runware for training...")

    # This is placeholder logic — you’ll need to connect to your actual Runware instance
    files = []
    for img in uploaded_images:
        files.append(("images", (img.name, img, img.type)))

    data = {"image_type": image_type, "model_name": "test_handbag_lora"}

    # Example placeholder endpoint
    response = requests.post("https://api.runware.ai/kohya/train", files=files, data=data, headers = {
    "X-API-Key": st.secrets["runware"]["api_key"]
}
)

    if response.status_code == 200:
        st.success("Training started! Check back in a while to test generation.")
    else:
        st.error("There was an error starting training. Check your API or image data.")

# Prompt-based generation
st.subheader("🎨 Generate Image (ComfyUI)")

prompt = st.text_input("Enter prompt (e.g., 'leather handbag in studio lighting')")

if st.button("🖼️ Generate Image"):
    st.info("Sending prompt to ComfyUI for generation...")

    # Placeholder generation logic
    gen_response = requests.post("https://api.runware.ai/comfyui/generate", json={
        "prompt": prompt,
        "model": "test_handbag_lora"
    }, headers={
        "Authorization": f"Bearer {os.getenv('RUNWARE_API_KEY', 'your-api-key-here')}"
    })

    if gen_response.status_code == 200:
        image_url = gen_response.json().get("image_url")
        st.image(image_url, caption="Generated Image")
    else:
        st.error("There was an error generating the image.")
