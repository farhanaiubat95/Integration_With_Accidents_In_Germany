import streamlit as st
import requests
import pandas as pd

st.title("🔍 Custom Explorer")

# =====================================================
# Q8
# =====================================================

st.divider()

st.header(
    "Q8. Which five districts recorded the highest number of fatal accidents in 2024?"
)

if st.button("Analyze Q8"):

    response = requests.get(
        "http://127.0.0.1:8000/aggregates/top-fatal-accidents"
    )

    data = response.json()

    df = pd.DataFrame(data["results"])

    winner = df.iloc[0]

    st.markdown(
        f"""
        <div style="
            background:#b91c1c;
            color:white;
            padding:18px;
            border-radius:12px;
            font-size:20px;
            font-weight:600;
        ">
            🏆 Highest Fatal Accident District<br><br>
            {winner['district']}<br>
            Fatal Accidents: {winner['fatal_accidents']}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.code(
        "GET /aggregates/top-fatal-accidents",
        language="text"
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    st.bar_chart(
        df.set_index("district")["fatal_accidents"]
    )

    


# =====================================================
# Q9
# =====================================================

st.divider()

st.header(
    "Q9. How many bicycle accidents occurred in Dresden in 2024?"
)

if st.button("Analyze Q9"):

    response = requests.get(
        "http://127.0.0.1:8000/aggregates/bicycle-accidents",
        params={
            "location": "Dresden",
            "year": 2024
        }
    )

    data = response.json()

    st.metric(
        label="🚴 Bicycle Accidents",
        value=f"{data['bicycle_accidents']:,}"
    )

    st.markdown(
        f"""
        <div style="
            background:#0f766e;
            color:white;
            padding:20px;
            border-radius:12px;
            font-size:20px;
            font-weight:600;
            text-align:center;
        ">
            🚴 Dresden recorded<br>
            <span style="font-size:34px;">
            {data['bicycle_accidents']:,}
            </span><br>
            bicycle accidents in 2024
        </div>
        """,
        unsafe_allow_html=True
    )
    st.code(
        "GET /aggregates/bicycle-accidents?location=Dresden&year=2024",
        language="text"
    )

    

    


# =====================================================
# Q10
# =====================================================

st.divider()

st.header(
    "Q10. Which districts in Sachsen recorded the lowest number of accidents in 2023?"
)

if st.button("Analyze Q10"):

    response = requests.get(
        "http://127.0.0.1:8000/aggregates/lowest-accidents"
    )

    data = response.json()

    df = pd.DataFrame(data["results"])

    lowest = df.iloc[0]

    st.markdown(
        f"""
        <div style="
            background:#7c3aed;
            color:white;
            padding:18px;
            border-radius:12px;
            font-size:18px;
            font-weight:600;
        ">
            📉 Lowest Accident District in Sachsen (2023)<br><br>
            {lowest['district']}<br>
            Total Accidents: {lowest['total_accidents']}
        </div>
        """,
        unsafe_allow_html=True
    )


    st.code(
        "GET /aggregates/lowest-accidents",
        language="text"
    )

    
    st.dataframe(
        df,
        use_container_width=True
    )

    st.subheader("Lowest Accident Districts")

    st.bar_chart(
        df.set_index("district")["total_accidents"]
    )

    st.code(
        "GET /aggregates/lowest-accidents",
        language="text"
    )