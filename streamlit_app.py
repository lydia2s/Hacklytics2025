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
uploaded_file = st.file_uploader("Upload an image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])

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

##get damage type, severity, and affected parts from image

# Set your OpenAI API key
from openai import OpenAI

client = OpenAI(api_key="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") 
openai.api_key = "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"

damage_type = "Crack"  # Placeholder; should be detected by AI in future
severity = "Moderate"
affected_parts = ["Wall", "Ceiling"]
labor_cost_factor = 1.2  # Placeholder value

def get_damage_estimate(damage_type, severity, affected_parts, location, labor_cost_factor):
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

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# Collect user input
location = st.text_input("Where is the home geographically located (e.g., Los Angeles, CA): ")
spending = st.selectbox("Willingness to spend:", ["Low", "Medium", "High"])

if st.button("Get Repair Estimate"):
        with st.spinner("🔄 Analyzing the image and calculating costs..."):
            estimate = get_damage_estimate(damage_type, severity, affected_parts, location, labor_cost_factor)
        st.subheader("Estimated Repair Cost:")
        st.write(estimate)


# Get and print the cost estimate
estimate = get_damage_estimate(damage_type, severity, affected_parts, location, labor_cost_factor)
print("\nEstimated Repair Cost:\n", estimate)
