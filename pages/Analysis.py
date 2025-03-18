import streamlit as st
import pandas as pd
import altair as alt
import pymssql

@st.cache_resource
def init_connection(server, user, password, database):
    """Initialize and return a pymssql connection."""
    return pymssql.connect(server, user, password, database)

# Note the leading underscore in _conn to avoid hashing errors
@st.cache_data
def run_query(_conn, query):
    """Execute a SQL query and return results in a DataFrame."""
    with _conn.cursor() as cursor:
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
        """
    )

    # Sidebar for DB credentials
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

    # Tabs for different analyses
    tab1, tab2 = st.tabs(["Wet vs Dry", "Younger vs Older"])

    # ---- TAB 1: Wet vs Dry ----
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

                    # Prepare data
                    df_wet["type"] = "Wet"
                    df_dry["type"] = "Dry"

                    df_wet.rename(columns={"count_wet": "Collisions"}, inplace=True)
                    df_dry.rename(columns={"count_dry": "Collisions"}, inplace=True)

                    combined = pd.concat([df_wet, df_dry], ignore_index=True)

                    # Altair grouped bar chart
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

    # ---- TAB 2: Younger vs Older ----
    with tab2:
        st.subheader("Comparing Younger vs Older Drivers
