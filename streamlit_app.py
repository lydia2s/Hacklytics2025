import streamlit as st
from PIL import Image
import openai

# ---- Set Page Configuration ----
st.set_page_config(
    page_title="Housing Damage Assessment",
    page_icon="🔍",
    layout="wide"
)

# ---- Layout: Sidebar (1) | Main Content (2) ----
col1, col2 = st.columns([1, 2], gap="medium")

with col1:
    # ---- Sidebar (Fixed Width) ----
    st.title("RenoVision")
    st.image("images/logo.png")
    mode = st.radio("Select Mode:", ["Image Analysis", "Chat Assistant"])
    st.info("Receive a personalized repair estimate based on your location and the current market.")

    # File Uploader (Only in Sidebar)
    uploaded_file = st.file_uploader("📤 Upload an image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])

with col2:
    # ---- Main Section ----

    # Enlarged Image Upload Section
    if uploaded_file:
        image = Image.open(uploaded_file)
        
        # Display the image (Larger)
        st.subheader("Uploaded Image:")
        st.image(image, caption="Your Image", use_container_width=True)

        # Show image details
        st.write(f"**Repair Type:** {uploaded_file.name}")  # Replace with AI-generated type
        st.write(f"**Severity:** {image.format}")  # Replace with AI-generated severity

    else:
        st.info("Please upload an image to start analysis.")

# ---- OpenAI API Client ----
OPEN_AI_KEY = st.secrets["AI_KEY"]
openai.api_key = OPEN_AI_KEY  # Correctly setting the API key

# Placeholder values (Replace with AI detection in future)
damage_type = "Crack"
severity = "Moderate"
affected_parts = ["Wall", "Ceiling"]
labor_cost_factor = 1.2

def get_damage_estimate(damage_type, severity, affected_parts, location, labor_cost_factor):
    """Sends details to OpenAI to estimate repair costs."""
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

# ---- User Inputs ----
location = st.text_input("Home Location")
spending = st.selectbox("Willingness to Spend:", ["Low", "Medium", "High"])

if st.button("Get Repair Estimate"):
    with st.spinner("Analyzing the image and calculating costs..."):
        estimate = get_damage_estimate(damage_type, severity, affected_parts, location, labor_cost_factor)
    
    # Chat-style response
    st.markdown(
        f"""
        <div style='background-color:#00a5e3; padding:15px; border-radius:10px; color:white;'>
            <b>Estimated Repair Cost:</b>  
            {estimate}
        </div>
        """,
        unsafe_allow_html=True
    )
