import streamlit as st

def load_css():
    css = """
    <style>
        /* General Styles */
        body {
            background-color: #f7f7f7;
            color: #333;
        }
        
        /* Title Styling */
        .title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #007bff;
            margin-bottom: 20px;
        }
        
        /* Sidebar Styling */
        .css-1lcbmhc {
            background-color: #2c3e50 !important;
            color: white !important;
        }

        /* Buttons */
        .stButton>button {
            background-color: #007bff;
            color: white;
            border-radius: 8px;
            font-size: 16px;
            padding: 10px;
            width: 100%;
            border: none;
        }

        .stButton>button:hover {
            background-color: #0056b3;
        }

        /* Text Inputs */
        .stTextInput>div>div>input {
            border-radius: 5px;
            border: 1px solid #007bff;
            padding: 10px;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
