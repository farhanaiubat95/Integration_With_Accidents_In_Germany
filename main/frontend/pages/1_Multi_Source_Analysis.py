import streamlit as st
import requests
import pandas as pd

st.title("📊 Multi Source Analysis")

# =====================================================
# Q6
# =====================================================

st.divider()

st.header(
    "Q6. Which 5 districts had the highest accident rate per 100,000 inhabitants using 2024 population data?"
)

st.write(
    """
    Uses accident data and population data to identify
    districts with the highest accident risk.
    """
)

if st.button("Analyze Q6"):

    response = requests.get(
        "http://127.0.0.1:8000/aggregates/accident-rate-per-100k"
    )

    data = response.json()

    df = pd.DataFrame(data["results"])

    highest = df.iloc[0]

    st.success(
        f"Analyzed {data['total_districts_analyzed']} districts."
    )

    st.metric(
        "Highest Accident Rate District",
        highest["district"]
    )

    st.markdown(
        f"""
        <div style="
            background:#2563eb;
            color:white;
            padding:15px;
            border-radius:10px;
            font-size:18px;
            font-weight:600;
        ">
            🚨 Highest accident rate recorded in
            <b>{highest['district']}</b><br><br>

            Accident Rate:
            {highest['accident_rate_per_100k']}
            per 100,000 inhabitants
        </div>
        """,
        unsafe_allow_html=True
    )

    st.code(
        "GET /aggregates/accident-rate-per-100k",
        language="text"
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    st.subheader("📈 Accident Rate per 100,000 Inhabitants")

    st.bar_chart(
        df.set_index("district")["accident_rate_per_100k"]
    )

    


# =====================================================
# Q7
# =====================================================

st.divider()

st.header(
    "Q7. Which districts had the highest accident density (accidents per square kilometer) in 2023?"
)

st.write(
    """
    Accident density shows how many accidents occurred
    per square kilometer.
    """
)

if st.button("Analyze Q7"):

    response = requests.get(
        "http://127.0.0.1:8000/aggregates/accident-density"
    )

    data = response.json()

    df = pd.DataFrame(data["results"])

    top_density = df.iloc[0]

    st.metric(
        "Highest Density District",
        top_density["district"]
    )

    st.markdown(
        f"""
        <div style="
            background:#dc2626;
            color:white;
            padding:15px;
            border-radius:10px;
            font-size:18px;
            font-weight:600;
        ">
            📍 Highest accident density district:
            <b>{top_density['district']}</b><br><br>

            Density:
            {top_density['accidents_per_km2']}
            accidents per km²
        </div>
        """,
        unsafe_allow_html=True
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    st.subheader("📊 Accidents per km²")

    st.bar_chart(
        df.set_index("district")["accidents_per_km2"]
    )

    st.code(
        "GET /aggregates/accident-density",
        language="text"
    )