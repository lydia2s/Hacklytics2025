import streamlit as st
from PIL import Image
import openai

# ---- Set Page Configuration ----
st.set_page_config(
    page_title="Housing Damage Assessment",
    page_icon="👓",
    layout="wide"
)

# ---- Custom CSS for Header & Styling Fixes ----
st.markdown(
    """
    <style>
        /* Apply light gray background to entire page */
        body, .stApp {
            background-color: #CCCCCC; /* Light Gray */
            color: black;
        }

        /* Separate White Header Section */
        .header-container {
            text-align: center;
            width: 100%;
            background-color: white; /* White Background */
            padding: 15px;
            border-radius: 10px;
        }

        /* RenoVision & Section Headers */
        .header-title {
            font-size: 50px;
            color: #001F3F !important; /* Dark Blue */
            font-weight: bold;
            margin: 10px 0;
        }

        /* Subtitle */
        .header-subtitle {
            font-size: 18px;
            color: #E2725B !important; /* Orange */
            font-weight: bold;
            margin-top: 5px;
        }

        /* Change text inside inputs to black */
        label, span, p {
            color: black !important;
        }

        /* Style input boxes (text input & select box) */
        .stTextInput>div>div>input,
        .stSelectbox>div>div>div {
            background-color: #EEEEEE !important; /* Light Gray */
            color: black !important;
            border-radius: 5px;
        }

        /* Style buttons */
        .stButton>button {
            background-color: #EEEEEE !important;
            color: black !important;
            border-radius: 5px;
        }
        .stButton>button:hover {
            background-color: #D3D3D3 !important;
        }

        /* Custom Info Box Styling */
        .custom-info-box {
            background-color: #EEEEEE;
            color: #5A5A5A; /* Matches File Uploader Text */
            padding: 15px;
            border-radius: 5px;
            text-align: center;
        }

        /* Style file uploader */
        .stFileUploader>div>div {
            color: #5A5A5A !important;
            background-color: #EEEEEE !important;
            border-radius: 5px;
        }
    </style>

    <div class="header-container">
        <h1 class="header-title">RenoVision</h1>
        <h6 class="header-subtitle">Renovation with a New Vision.</h6>
    </div>
    """,
    unsafe_allow_html=True
)

# ---- Layout: Sidebar (1) | Main Content (2) ----
col1, col2 = st.columns([1, 2], gap="medium")

with col1:
    # ---- Add Space Before "Select Mode" ----
    st.markdown("<br>", unsafe_allow_html=True)  # Adds spacing
    
    # ---- Sidebar ----
    mode = st.radio("Select Mode:", ["Image Analysis", "Chat Assistant"])

    # **Show image upload & repair description only in "Image Analysis" mode**
    if mode == "Image Analysis":
        # **Spacing before info box**
        st.markdown("<br>", unsafe_allow_html=True)

        # Custom Info Box (Replaces `st.info()`)
        st.markdown(
            "<div class='custom-info-box'>Receive a personalized repair estimate based on your location and the current market.</div>",
            unsafe_allow_html=True
        )

        # **Spacing before file upload**
        st.markdown("<br>", unsafe_allow_html=True)

        # File Uploader (Only in Image Analysis Mode)
        uploaded_file = st.file_uploader("Upload an image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])
    else:
        uploaded_file = None  # Ensures no file is processed if not in Image Analysis mode

with col2:
    # ---- Mode Switching ----
    if mode == "Image Analysis":
        # **Image Analysis Header with Same Styling as "RenoVision"**
        st.markdown("<h1 class='header-title'>Image Analysis</h1>", unsafe_allow_html=True)
        
        if uploaded_file:
            image = Image.open(uploaded_file)

            # Display the image (Larger)
            st.image(image, caption="Your Image", use_column_width=True)

            # Show image details
            st.write(f"**Repair Type:** {uploaded_file.name}")  # Placeholder for AI output
            st.write(f"**Severity:** {image.format}")  # Placeholder for severity detection

            # ---- User Inputs (Only Show When Image is Uploaded) ----
            location = st.text_input("Home Location (City)")

            if st.button("Get Repair Estimate"):
                with st.spinner("Analyzing the image and calculating costs..."):
                    estimate = f"Estimated cost range: $1000 - $2000\n- Parts: $500\n- Labor: $1200\n- Additional: $300"
                
                # Chat-style response
                st.markdown(
                    f"""
                    <div style='background-color:#EEEEEE; padding:15px; border-radius:10px; color:#5A5A5A;'>
                        <b>Estimated Repair Cost:</b>  
                        {estimate}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            # Custom Info Box for "Please upload an image to start the analysis."
            st.markdown(
                "<div class='custom-info-box'> Please upload an image to start the analysis.</div>",
                unsafe_allow_html=True
            )

    elif mode == "Chat Assistant":
        # **Chat Assistant Header with Same Styling as "RenoVision"**
        st.markdown("<h1 class='header-title'>Chat Assistant</h1>", unsafe_allow_html=True)

        # **Chat Input using "Enter" instead of Button**
        chat_input = st.text_input(
            "Ask me about home repairs, damage estimates, and renovation tips.",
            key="chat_input"
        )

        if chat_input:
            with st.spinner("Analyzing..."):
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": chat_input}]
                )
                assistant_reply = response["choices"][0]["message"]["content"]

            # Display Chat Response
            st.markdown(
                f"""
                <div style='background-color:#EEEEEE; padding:15px; border-radius:10px; color:#5A5A5A;'>
                     <b>Assistant:</b>  
                    {assistant_reply}
                </div>
                """,
                unsafe_allow_html=True
            )

            # **Clear input after submission**
            st.session_state["chat_input"] = ""
