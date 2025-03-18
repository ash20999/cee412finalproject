import streamlit as st
import pandas as pd
import altair as alt
import pymssql

@st.cache_resource
def init_connection(server, user, password, database):
    """Initialize and return a pymssql connection."""
    return pymssql.connect(server, user, password, database)

@st.cache_data
def run_query(conn, query):
    """Execute a SQL query and return results in a DataFrame."""
    with conn.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
    df = pd.DataFrame(data, columns=columns)
    return df

def main():
    st.title("Data Analysis & Interpretation")
    st.markdown(
        """
        In this section, we connect to our database and visualize key findings:

        1. **Wet vs Dry Road Collisions** (grouped by road surface code).
        2. **Younger vs Older Drivers** (grouped by crash rate or ACCTYPE).
        3. (Optional) Additional queries or advanced analytics (e.g., logistic regression, time-series).
        """
    )

    with st.sidebar:
        st.subheader("Database Credentials")
        server = st.text_input("Server address:", value="128.95.29.66")
        user = st.text_input("Username:", value="WI25_ash209")
        password = st.text_input("Password:", type="password", value="Aarshpatel0101")
        database = st.text_input("Database:", value="WI25_T10")

        if st.button("Connect to DB"):
            try:
                st.session_state["conn"] = init_connection(server, user, password, database)
                st.success("Connected successfully!")
            except Exception as e:
                st.error(f"Connection failed: {e}")

    # Use tabs to organize different analyses
    tab1, tab2, tab3 = st.tabs(["Wet vs Dry", "Younger vs Older", "Advanced Analysis"])

    with tab1:
        st.subheader("Comparing WetRoad vs DryRoad Tables")
        st.write("Grouped by `rdsurf` to see how collisions differ.")

        if "conn" not in st.session_state:
            st.warning("Please connect to the database first (check the sidebar).")
        else:
            conn = st.session_state["conn"]
            if st.button("Load Wet vs Dry Data"):
                try:
                    df_wet = run_query(conn, "SELECT rdsurf, COUNT(*) AS count_wet FROM WetRoad GROUP BY rdsurf")
                    df_dry = run_query(conn, "SELECT rdsurf, COUNT(*) AS count_dry FROM DryRoad GROUP BY rdsurf")

                    # Merge data for Altair chart
                    df_wet["type"] = "Wet"
                    df_dry["type"] = "Dry"

                    df_wet.rename(columns={"count_wet": "Collisions"}, inplace=True)
                    df_dry.rename(columns={"count_dry": "Collisions"}, inplace=True)

                    combined = pd.concat([df_wet, df_dry], ignore_index=True)

                    # Build an Altair bar chart
                    chart = (
                        alt.Chart(combined)
                        .mark_bar()
                        .encode(
                            x=alt.X("rdsurf:N", title="Road Surface Code"),
                            y=alt.Y("Collisions:Q", title="Number of Collisions"),
                            color=alt.Color("type:N", legend=alt.Legend(title="Surface Type")),
                            column=alt.Column("type:N", header=alt.Header(labelOrient="bottom"))
                        )
                        .properties(width=300)
                    )
                    st.altair_chart(chart, use_container_width=True)

                except Exception as ex:
                    st.error(f"Error loading data: {ex}")

    with tab2:
        st.subheader("Comparing Younger vs Older Drivers")
        st.write("Grouped by `CrashRate` or `ACCTYPE` to see distribution across driver age groups.")

        if "conn" not in st.session_state:
            st.warning("Please connect to the database in the sidebar.")
        else:
            conn = st.session_state["conn"]
            if st.button("Load Younger vs Older Data"):
                try:
                    query_y = "SELECT CrashRate, COUNT(*) AS collisions_y FROM AndYounger GROUP BY CrashRate"
                    query_o = "SELECT CrashRate, COUNT(*) AS collisions_o FROM AndOlder GROUP BY CrashRate"
                    df_younger = run_query(conn, query_y)
                    df_older = run_query(conn, query_o)

                    df_younger["Group"] = "Younger"
                    df_older["Group"] = "Older"

                    df_younger.rename(columns={"collisions_y": "Collisions"}, inplace=True)
                    df_older.rename(columns={"collisions_o": "Collisions"}, inplace=True)

                    combined_age = pd.concat([df_younger, df_older], ignore_index=True)

                    # Create an Altair grouped bar chart by CrashRate
                    chart_age = (
                        alt.Chart(combined_age)
                        .mark_bar()
                        .encode(
                            x=alt.X("CrashRate:N", title="Crash Rate Category"),
                            y=alt.Y("Collisions:Q", title="Number of Collisions"),
                            color=alt.Color("Group:N", legend=alt.Legend(title="Driver Group")),
                            column=alt.Column("Group:N", header=alt.Header(labelOrient="bottom"))
                        )
                        .properties(width=300)
                    )
                    st.altair_chart(chart_age, use_container_width=True)

                except Exception as ex:
                    st.error(f"Query error: {ex}")

    with tab3:
        st.subheader("Advanced Analysis (Optional)")
        st.write(
            """
            In a real project, this tab might include:
            - Statistical tests (e.g., chi-square or logistic regression)
            - Time-series analysis of collisions over years
            - Geospatial mapping of collisions (using `st.map` or `pydeck`)
            """
        )
        st.info("Future features can be demonstrated here!")

if __name__ == "__main__":
    main()
