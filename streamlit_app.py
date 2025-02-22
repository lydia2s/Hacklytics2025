import streamlit as st
from PIL import Image
import openai

# Show title and description.
st.title("Housing Damage Assessment")
st.write(
    "Upload an image below from library or camera roll for personalized damage and cost assessing."
)

# Title
st.title("Image Uploader")

# File Uploader: Accepts images only
uploaded_file = st.file_uploader("📤 Upload an image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Open image using PIL
    image = Image.open(uploaded_file)
    
    # Display the image
    st.subheader("Uploaded Image:")
    st.image(image, caption="Your Image", use_container_width=True)

    # Optional: Show image details
    st.write(f"**Filename:** {uploaded_file.name}")
    st.write(f"**Format:** {image.format}")
    st.write(f"**Size:** {image.size}")

else:
    st.info("📌 Please upload an image to display.")

##get damage type, severity, and affected parts from image

# Set your OpenAI API key
openai.api_key = "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"

def get_damage_estimate(damage_type, severity, affected_parts):
    prompt = f"""
    You are an expert in repair cost estimation. Given the details below, provide an estimated cost range in USD with a breakdown of parts, labor, and additional costs.

    - Damage Type: {damage_type}
    - Severity: {severity}
    - Affected Parts: {', '.join(affected_parts)}
    - Location: {location}
    - Labor Cost Factor: {labor_cost_factor}

    Return a structured response like:
    Estimated Cost: $X - $Y
    Breakdown:
    - Parts: $A
    - Labor: $B
    - Additional Costs: $C (paint, finishing, etc.)
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["choices"][0]["message"]["content"]

# Collect user input
location = input("Where is the home geographically located (e.g., Los Angeles, CA): ")
spending = input("How willing are you to spend on repairing the damage (low, medium, high): ")

# Get and print the cost estimate
estimate = get_damage_estimate(damage_type, severity, affected_parts, location, labor_cost_factor)
print("\nEstimated Repair Cost:\n", estimate)
