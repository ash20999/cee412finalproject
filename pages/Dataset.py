import streamlit as st
import os
import base64
# from PIL import Image  # Only needed if using st.image

def main():
    st.title("Dataset & Data Management Plan")

    st.markdown(
        """
        ### Dataset Overview
        We used the HSIS dataset for major Washington State freeways (I-5, I-90, I-405, SR-520),
        containing details on:
        - **Accidents** (date, time, weather, location)
        - **Roadway features** (speed limits, AADT, surface conditions)
        - **Vehicles & Drivers** (type, age, impairment)
        
        **Size**: ~ several hundred thousand collision records across multiple years.
        
        ### Limitations
        1. Missing or erroneous records (unknown driver ages, incomplete weather data).
        2. Differences in data dictionaries between 2002 and 2013–2017, requiring standardization.
        3. Freeways might not be equally represented in each year (potential bias).
        """
    )

    # Example of embedding or displaying your E/R diagram
    st.subheader("E/R Diagram")

    pdf_path = os.path.join("data", "er_diagram.pdf")  # adjust if needed
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode("utf-8")
        pdf_display = f"""
        <iframe 
        src="data:application/pdf;base64,{base64_pdf}" 
        width="650" 
        height="900" 
        type="application/pdf"></iframe>
        """
        st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        st.warning("E/R Diagram PDF not found. Check the path or file name.")

    st.write(
        """
        **Entity Design**:
        - **Accident**: CASENO (PK), Date, Weather, Road_Condition, ...
        - **Road**: RoadID (PK), GPSX, GPSY, Surface_Type, AADT, ...
        - **Vehicle**: VEHICLE_ID (PK), ACCIDENT_ID (FK), Vehicle_Type, ...
        - **Driver**: LICENSENUMBER (PK), Age, Impaired, Sex, ...
        
        ### Data Storage & Management
        - Hosted on Microsoft SQL Server (for robust queries and concurrent access).
        - SQL scripts used to import raw HSIS data.
        - Backups performed bi-weekly to mitigate data loss.
        - Anomalies (e.g., duplicates) flagged and addressed prior to analysis.
        
        Our structure follows BCNF, ensuring minimal redundancy and efficient queries.
        """
    )

if __name__ == "__main__":
    main()
