import datetime
import random
from time import sleep, strptime

import streamlit as st

from src.scrape_local_epc import EnergyCertificateScraper
from src.backend_functions import get_addresses, get_certificates, mwh_usage

MONTHS: list[str] = [datetime.datetime.strptime(f"2024-{i}-01", "%Y-%m-%d").strftime("%B") for i in range(1, 13)]

def generate_random_number(input: float) -> float:
    random.seed(42)
    return random.gauss(mu=1, sigma=0.25) * input

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
    address: str = st.selectbox(label="Select address", options=get_addresses(input_postcode))

    if address:

        month: int = MONTHS.index(
            st.selectbox(
                "Month",
                options=MONTHS,
            )
        )
        property_type: str = st.selectbox(
            label="Property type",
            options=["Detached", "Semi-detached", "Terrace", "Flat"],
        )
        area: int = st.number_input("Floor area (m^2)", min_value=0, help="Floor area in metres squared")
        has_heat_pump: bool = st.checkbox("Has heat pump")
        # has_battery
        has_solar: bool = st.checkbox("Has solar")
        # has_electric_hot_water
        # has_electric_radiator
        # is_mains_gas
        has_ev: bool = st.checkbox("Has electric vehicle")
        # has_lct
        urban_or_remote: bool = st.checkbox("Urban property?")

        scraper = EnergyCertificateScraper(address, input_postcode)
        scraper.parse_table()
        scraper.scrape_current_certificate()
        scraper.parse_current_certificate()

        scraper.get_previous_reports()
        scraper.collect_report_recommendation_history()

        epc, median_rating = get_certificates(address, input_postcode)
        st.text(f"Your EPC rating is {epc}, compared with an average of {median_rating} in your postcode.")
        
        expected_energy_usage: float = mwh_usage(
            epc=epc,
            user_inputs=[month, property_type, area, has_heat_pump, has_solar, has_ev, urban_or_remote]
        )
        observed_energy_usage: float = generate_random_number(mwh_usage(epc, [0, "Flat", 90, 1, 1, 0, 1]))

        st.text(f"The energy usage expected for your property per day, based on the attributes listed above, would be {expected_energy_usage:.2f}kWh. The actual usage observed is {observed_energy_usage:.2f}kWh.")


        st.text(f"This property has the potential to have an energy rating of {scraper.potential_energy_rating} and an environmental rating of {scraper.potential_environmental_impact_rating}.")
        st.dataframe(
            scraper.full_recommendations_history
        )

        show_ai_summarisation_tool: bool = st.checkbox("Show AI summarisation")
        if show_ai_summarisation_tool:
            sleep(2.5)
            st.text("The most recent report for this property recommends the improvement of insulation in the walls of the property. Previous reports suggested fitting double glazing, but these fixes have now been implemented. The report suggests that financial support may be available for fitting a heat pump. This has not yet been installed.")

        
