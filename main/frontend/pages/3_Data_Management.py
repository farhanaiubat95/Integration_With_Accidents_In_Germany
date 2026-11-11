import streamlit as st
import requests
import pandas as pd

st.title("🗂️ Data Management")

st.divider()

st.header("Data Sources")

st.write(
    """
    Displays all registered datasets
    used in the system.
    """
)

if st.button("Load Sources"):

    response = requests.get(
        "http://127.0.0.1:8000/metadata/sources"
    )

    data = response.json()

    st.metric(
        "Total Sources",
        data["total_sources"]
    )

    df = pd.DataFrame(
        data["results"]
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    st.subheader("Source Distribution")

    chart_data = (
        df["source_name"]
        .value_counts()
        .reset_index()
    )

    chart_data.columns = [
        "Source",
        "Count"
    ]

    st.bar_chart(
        chart_data.set_index("Source")
    )


# IMPORT RUNS

st.divider()

st.header("Import History")

st.write(
    """
    Displays all import operations
    executed in the database.
    """
)

if st.button("Load Import Runs"):

    response = requests.get(
        "http://127.0.0.1:8000/import-runs"
    )

    data = response.json()

    st.metric(
        "Total Import Runs",
        data["total_import_runs"]
    )

    df = pd.DataFrame(
        data["results"]
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    st.subheader(
        "Records Imported Per Table"
    )

    chart_df = (
        df.groupby("table_name")
        ["records_imported"]
        .sum()
        .reset_index()
    )

    st.bar_chart(
        chart_df.set_index(
            "table_name"
        )
    )

    st.success(
        "Import history loaded successfully."
    )