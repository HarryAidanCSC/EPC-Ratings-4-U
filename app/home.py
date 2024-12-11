import os

import streamlit as st

header_css = """
    <style>
        .header {
            color: white;
            background-color: black;
            padding: 0px;
            display: flex;
            align-items: center;
            height: 160px; /* Fixed height for the header */
            text-align: center;
        }
        .header img {
            margin-left: 10px;
            margin-right: 100px;  /* Adjust spacing between image and text */
        }
        .header p {
            margin: 0;
            font-size: 80px; /* Adjust font size as needed */
            line-height: 1.0; /* Adjust line height to match image height */
            font-weight: bold; /* Make text bold */
            font-family: Arial, Helvetica, sans-serif; /* Set font family */
            text-align: center;
            padding: 20px;
        }
        .blue-underline {
            background-color: #1d70b8; /* Blue color for the underline */
            height: 8px; /* Height of the underline */
            width: 85%; /* Set the width of the underline */
            margin: 0 auto; /* Center the underline horizontally */
        }
        .normal-line {
            background-color: #dddddd; /* Neutral color for the line */
            height: 2px; /* Thin line */
            width: 85%; /* Set the width of the line */
            margin: 10px auto 0; /* Add top margin to push the line down */
        }
    </style>
"""

st.markdown(header_css, unsafe_allow_html=True)

# Create a header section
header = st.container()
with header:
    # Using HTML to layout image and text
    st.markdown(
        f"""
        <div class="header">
            <p>EPC Ratings 4 U</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown(
        "<p text-align: justify; text-justify: inter-word;>"
        "This is a tool to to evaluate EPC certificates, reports, and ratings. "
        "</p>",
        unsafe_allow_html=True,
    )

input_postcode = st.text_input(label="Postcode", placeholder="Enter your postcode", max_chars=8, help="Enter your postcode")

st.text(input_postcode)

if input_postcode:
    st.selectbox(label="Select address", options=["1b Heriot Road, Hendon, London, NW4 2EG", "1c Heriot Road, Hendon, London, NW4 2EG"])