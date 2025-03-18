import streamlit as st

def main():
    st.title("Project Conclusion")

    st.markdown(
        """
        ## Key Takeaways
        - **Wet roads** see higher collision counts, especially in certain conditions
        - **High speed limits** correlate with more severe rear-end collisions
        - **Younger drivers** (under 25) appear overrepresented in collisions under certain CrashRate categories

        ## Recommendations
        1. **Adaptive Speed Limits**: Implement variable or adaptive limits during wet weather.
        2. **Targeted Driver Education**: Additional training/awareness for younger drivers.
        3. **Data-Driven Policy**: Use real-time traffic & weather data to warn drivers about potential hazards.

        ## Next Steps
        - Expand the analysis to more freeways or additional years of data
        - Investigate the impact of roadway geometry (curve radius, grade) on collisions
        - Explore real-time data integration (e.g., WSDOT traffic sensors)

        ---
        #### Thank You!
        We appreciate your interest and hope this app sheds light on new strategies
        for reducing rear-end collisions on Washington State freeways.
        """
    )

if __name__ == "__main__":
    main()
