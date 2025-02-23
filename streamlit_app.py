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
        /* Remove background for RenoVision */
        .header-container {
            text-align: center;
            width: 100%;
            margin-top: 0px;
            background: none !important;
            padding-bottom: 10px;
        }

        /* Style the RenoVision title */
        .renovision-title {
            font-size: 50px;
            margin: 0;
            background: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            border: none !important;
            color: white !important;
        }

        /* Style the separator */
        .separator {
            width: 80%;
            height: 2px;
            background-color: white;
            margin: 20px auto;
            border-radius: 2px;
        }
    </style>

    <div class="header-container">
        <h1 class="renovision-title">RenoVision</h1>
        <h6 title> Renovation with a New Vision. </h1 header>
        
    </div>
    """,

    unsafe_allow_html=True
)



# ---- Layout: Sidebar (1) | Main Content (2) ----
col1, col2 = st.columns([1, 2], gap="medium")

with col1:
    # ---- Sidebar ----
    mode = st.radio("Select Mode:", ["Image Analysis", "Chat Assistant"])
    st.info("Receive a personalized repair estimate based on your location and the current market.")

    # File Uploader (Only in Sidebar, Used for Image Analysis)
    uploaded_file = st.file_uploader("Upload an image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])

with col2:
    # ---- Mode Switching ----
    if mode == "Image Analysis":
        st.header("Image Analysis")
        
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

            if st.button("Get Repair Estimate"):
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
            st.info("Please upload an image to start the analysis.")

    elif mode == "Chat Assistant":
        st.header("Chat Assistant")

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
