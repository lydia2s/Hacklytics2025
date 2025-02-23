import streamlit as st
from PIL import Image
import openai

# ---- Set Page Configuration ----
st.set_page_config(
    page_title="Housing Damage Assessment",
    page_icon="🔍",
    layout="wide"
)

# ---- Custom CSS for Full Dark Blue Background & White Text ----
st.markdown(
    """
    <style>
        /* Apply dark blue background to entire page */
        body, .stApp {
            background-color: #001F3F; /* Dark Blue */
            color: white; /* White text */
        }

        /* Style the sidebar with a slightly lighter blue */
        [data-testid="stVerticalBlock"] > div:first-child {
            background-color: #ECECEC; /* Slightly lighter blue for sidebar */
            padding: 20px;
            border-radius: 10px;
        }

        /* Center the title */
        .header-container {
            text-align: center;
            width: 100%;
            margin-top: 0px;
        }
        .header-container h1 {
            color: #ff4d00;
            font-size: 50px;
            margin: 0;
        }

        /* Style text globally */
        h1, h2, h3, h4, h5, h6, p, label, span {
            color: white !important;
        }

        /* Style buttons */
        .stButton>button {
            background-color: #004080; /* Darker Blue */
            color: white;
            border-radius: 5px;
        }
        .stButton>button:hover {
            background-color: #0055A4; /* Lighter Blue on Hover */
        }

        /* Style info/warning boxes */
        .stAlert {
            background-color: #003366 !important; 
            color: white !important;
        }

        /* Style input fields */
        .stTextInput>div>div>input,
        .stSelectbox>div>div>div {
            background-color: #003366 !important;
            color: white !important;
        }

    </style>

    <div class="header-container">
        <h1 style>RenoVision</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# ---- Layout: Sidebar (1) | Main Content (2) ----
col1, col2 = st.columns([1, 2], gap="medium")

with col1:
    # ---- Sidebar ----
    st.subheader("Navigation")
    mode = st.radio("Select Mode:", ["Image Analysis", "Chat Assistant"])
    st.info("Receive a personalized repair estimate based on your location and the current market.")

    # File Uploader (Only in Sidebar, Used for Image Analysis)
    uploaded_file = st.file_uploader("📤 Upload an image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])

with col2:
    # ---- Mode Switching ----
    if mode == "Image Analysis":
        st.header("🔍 Image Analysis")
        
        if uploaded_file:
            image = Image.open(uploaded_file)

            # Display the image (Larger)
            st.subheader("Uploaded Image:")
            st.image(image, caption="Your Image", use_container_width=True)

            # Show image details
            st.write(f"**Repair Type:** {uploaded_file.name}")  # Placeholder for AI output
            st.write(f"**Severity:** {image.format}")  # Placeholder for severity detection

            # ---- User Inputs (Only Show When Image is Uploaded) ----
            location = st.text_input("Home Location")
            spending = st.selectbox("Willingness to Spend:", ["Low", "Medium", "High"])

            if st.button("🔍 Get Repair Estimate"):
                with st.spinner("Analyzing the image and calculating costs..."):
                    estimate = f"Estimated cost range: $1000 - $2000\n- Parts: $500\n- Labor: $1200\n- Additional: $300"
                
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
        else:
            st.info("📤 Please upload an image to start the analysis.")

    elif mode == "Chat Assistant":
        st.header("💬 Chat Assistant")

        # Chat Input
        user_input = st.text_input("Ask me about home repairs, damage estimates, and renovation tips.")
        
        if st.button("Send"):
            with st.spinner("Analyzing..."):
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": user_input}]
                )
                assistant_reply = response["choices"][0]["message"]["content"]

            # Display Chat Response
            st.markdown(
                f"""
                <div style='background-color:#00a5e3; padding:15px; border-radius:10px; color:white;'>
                     <b>Assistant:</b>  
                    {assistant_reply}
                </div>
                """,
                unsafe_allow_html=True
            )
