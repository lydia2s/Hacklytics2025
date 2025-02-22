import streamlit as st
from PIL import Image

# Show title and description.
st.title("Housing Damage Assessment")
st.write(
    "Upload an image below from library or camera roll for personalized damage and cost assessing."
)

# Title
st.title("Image Uploader")

# File Uploader: Accepts images only
uploaded_file = st.file_uploader("📤 Upload an image (JPG, PNG)", type=["jpg", "png"])

if uploaded_file:
    # Open image using PIL
    image = Image.open(uploaded_file)
    
    # Display the image
    st.subheader("Uploaded Image:")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Optional: Show image details
    st.write(f"**Filename:** {uploaded_file.name}")
    st.write(f"**Format:** {image.format}")
    st.write(f"**Size:** {image.size}")

else:
    st.info("📌 Please upload an image to display.")
