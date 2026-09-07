import streamlit as st
import requests

st.title("📋 Mandatory Questions")

# Q1
st.subheader("Q1. What is the earliest accident year in the complete dataset?")

if st.button("Get Answer", key="q1"):

    response = requests.get(
        "http://127.0.0.1:8000/accidents/earliest-year"
    )

    data = response.json()

    st.metric(
        label="Earliest Accident Year",
        value=data["earliest_year"]
    )

    st.markdown(
    f"""
    <div style="
        background-color:#2563eb;
        padding:15px;
        border-radius:10px;
        color:white;
        font-size:18px;
        font-weight:600;
    ">
        📅 The accident dataset starts in {data['earliest_year']}
    </div>
    """,
    unsafe_allow_html=True
)

    st.code(
        "GET /accidents/earliest-year",
        language="text"
    )


# Q2
st.divider()

st.subheader(
    "Q2. How many accidents involving personal injury occurred in Sachsen in 2023?"
)

if st.button("Get Answer", key="q2"):

    response = requests.get(
        "http://127.0.0.1:8000/aggregates/personal-injury",
        params={
            "state": "sachsen",
            "year": 2023
        }
    )

    data = response.json()

    st.metric(
        label="Personal Injury Accidents",
        value=f"{data['personal_injury_accidents']:,}"
    )

    st.markdown(
    f"""
    <div style="
        background-color:#16a34a;
        padding:15px;
        border-radius:10px;
        color:white;
        font-size:18px;
        font-weight:600;
    ">
        🚑 In Sachsen, {data['personal_injury_accidents']:,} personal injury accidents occurred in 2023.
    </div>
    """,
    unsafe_allow_html=True
)

    st.code(
        "GET /aggregates/personal-injury?state=sachsen&year=2023",
        language="text"
    )


# Q3 + Q4 divider
st.divider()

col1, col2 = st.columns(2)

# Q3
with col1:

    st.markdown("#### Q3. Nordrhein-Westfalen")

    if st.button("Check NRW", key="q3"):

        response = requests.get(
            "http://127.0.0.1:8000/data-availability/",
            params={
                "state": "nordrhein-westfalen"
            }
        )

        data = response.json()

        st.metric(
            "First Available Year",
            data["first_year"]
        )

        st.markdown(
            f"""
            <div style="
                background-color:#7c3aed;
                padding:12px;
                border-radius:10px;
                color:white;
                font-weight:600;
            ">
                📂 NRW data available from {data['first_year']}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.code(
            "GET /data-availability/?state=nordrhein-westfalen",
            language="text"
        )


# Q4
with col2:

    st.markdown("#### Q4. Mecklenburg-Vorpommern")

    if st.button("Check MV", key="q4"):

        response = requests.get(
            "http://127.0.0.1:8000/data-availability/",
            params={
                "state": "mecklenburg-vorpommern"
            }
        )

        data = response.json()

        st.metric(
            "First Available Year",
            data["first_year"]
        )

        st.markdown(
            f"""
            <div style="
                background-color:#ea580c;
                padding:12px;
                border-radius:10px;
                color:white;
                font-weight:600;
            ">
                📂 Mecklenburg-Vorpommern data available from {data['first_year']}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.code(
            "GET /data-availability/?state=mecklenburg-vorpommern",
            language="text"
        )


# Q5
st.divider()

st.subheader(
    "Q5. How many accidents involving pedestrians occurred in Berlin in 2023?"
)

if st.button(
    "Get Q5 Answer",
    key="q5"
):

    response = requests.get(
        "http://127.0.0.1:8000/aggregates/pedestrian-accidents",
        params={
            "state": "berlin",
            "year": 2023
        }
    )

    data = response.json()

    st.metric(
        label="Pedestrian Accidents",
        value=f"{data['pedestrian_accidents']:,}"
    )

    st.markdown(
        f"""
        <div style="
            background-color:#008080;
            padding:15px;
            border-radius:10px;
            color:white;
            font-size:18px;
            font-weight:600;
        ">
            🚶 In Berlin, {data['pedestrian_accidents']:,} pedestrian-related accidents occurred during 2023.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.code(
        "GET /aggregates/pedestrian-accidents?state=berlin&year=2023",
        language="text"
    )