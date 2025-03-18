import streamlit as st

def main():
    st.title("Introduction & Motivation")

    st.write(
        """
        ### Background
        Rear-end collisions are among the most frequent types of highway accidents, 
        often influenced by factors such as road surface conditions, driver behavior, 
        vehicle characteristics, and traffic volumes.
        
        Over the past decade, Washington State freeways have seen a variety of weather patterns 
        and traffic demands, making them ideal for exploring how factors like:
        
        - **Road surface (wet vs. dry)**,
        - **Speed limits**, and
        - **Driver age groups**
        
        affect collision frequency and severity.
        
        ### Why This Matters
        By identifying key predictors of rear-end collisions, we can:
        
        - Inform roadway design improvements (e.g., variable speed limits, better signage).
        - Develop targeted driver education (especially for younger motorists).
        - Optimize traffic control measures (ramp metering, dynamic message signs, etc.).
        
        **Our goal** is to present these findings in an accessible way, 
        allowing stakeholders to easily explore the data and glean insights 
        for policy and design decisions.
        """
    )

    st.info(
        """
        **Tip**: Use the sidebar to navigate to the Dataset & Data Management page, 
        where you can see how we structured and stored the data, 
        or jump straight to the Analysis page for interactive visualizations.
        """
    )

if __name__ == "__main__":
    main()
