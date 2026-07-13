from fastapi import APIRouter
from database import get_connection

router = APIRouter(
    prefix="/aggregates",
    tags=["Aggregates"]
)

STATE_MAP = {
        "sh": 1,
        "hh": 2,
        "ni": 3,
        "hb": 4,
        "nw": 5,
        "he": 6,
        "rp": 7,
        "bw": 8,
        "by": 9,
        "sl": 10,
        "be": 11,
        "bb": 12,
        "mv": 13,
        "sn": 14,
        "st": 15,
        "th": 16,

        "schleswig-holstein": 1,
        "hamburg": 2,
        "niedersachsen": 3,
        "bremen": 4,
        "nordrhein-westfalen": 5,
        "hessen": 6,
        "rheinland-pfalz": 7,
        "baden-württemberg": 8,
        "bayern": 9,
        "saarland": 10,
        "berlin": 11,
        "brandenburg": 12,
        "mecklenburg-vorpommern": 13,
        "sachsen": 14,
        "sachsen-anhalt": 15,
        "thüringen": 16,
}

# Q2
# How many accidents involving personal injury occurred in Sachsen in 2023?
@router.get("/personal-injury")
def personal_injury(state: str, year: int):

    state_id = STATE_MAP.get(state.lower().strip())

    if state_id is None:
        return {"error": "Invalid state"}

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT COUNT(*) AS total_accidents
        FROM accidents
        WHERE ULAND = %s
        AND UJAHR = %s
        AND UKATEGORIE IN (1,2,3)
    """, (state_id, year))

    data = cursor.fetchone()

    cursor.close()
    conn.close()

    return {
        "state": state,
        "year": year,
        "personal_injury_accidents": data["total_accidents"]
    }


# Q5 : How many accidents involving pedestrians occurred in Berlin in 2023?
@router.get("/pedestrian-accidents")
def pedestrian_accidents(
    state: str,
    year: int
):

    state_id = STATE_MAP.get(state.lower().strip())

    if state_id is None:
        return {
            "error": "Invalid state"
        }

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT COUNT(*) AS pedestrian_accidents
        FROM accidents
        WHERE ULAND = %s
        AND UJAHR = %s
        AND IstFuss = 1
    """, (state_id, year))

    data = cursor.fetchone()

    cursor.close()
    conn.close()

    return {
        "state": state,
        "year": year,
        "pedestrian_accidents": data["pedestrian_accidents"]
    }


# Q6
# Which 5 districts had the highest accident rate per 100,000 inhabitants using 2024 population data?

@router.get("/accident-rate-per-100k")
def accident_rate_per_100k():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Total districts analyzed

    cursor.execute("""
        SELECT COUNT(DISTINCT r.region_id) AS total_districts
        FROM regions r
        JOIN population p
            ON r.region_id = p.region_id
        WHERE r.level = 'district'
        AND p.population > 0
    """)

    total_districts = cursor.fetchone()["total_districts"]

    # Main query

    cursor.execute("""
        SELECT
            r.name AS district,

            p.population,

            COUNT(a.accident_id) AS total_accidents,

            ROUND(
                (COUNT(a.accident_id) * 100000.0) / p.population,
                2
            ) AS accident_rate_per_100k

        FROM accidents a

        JOIN population p
            ON a.region_id = p.region_id

        JOIN regions r
            ON a.region_id = r.region_id

        WHERE r.level = 'district'
        AND p.population > 0

        GROUP BY
            r.region_id,
            r.name,
            p.population

        ORDER BY accident_rate_per_100k DESC

        LIMIT 5
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "question": "Which districts had the highest accident rate per 100,000 inhabitants using 2024 population data?",
        "total_districts_analyzed": total_districts,
        "returned_results": len(data),
        "results": data
    }


# Q7 : Which districts had the highest accident density (accidents per square kilometer) in 2023?
@router.get("/accident-density")
def accident_density(limit: int = 10):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            r.name AS district,
            r.area_km2,

            COUNT(a.accident_id) AS total_accidents,

            ROUND(
                COUNT(a.accident_id) / r.area_km2,
                2
            ) AS accidents_per_km2

        FROM accidents a

        JOIN regions r
            ON a.region_id = r.region_id

        WHERE r.level = 'district'
        AND r.area_km2 > 0
        AND a.UJAHR = 2023

        GROUP BY
            r.region_id,
            r.name,
            r.area_km2

        ORDER BY accidents_per_km2 DESC

        LIMIT %s
    """, (limit,))

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "question": "Which districts had the highest accident density (accidents per square kilometer) in 2023?",
        "year": 2023,
        "total_results": len(data),
        "results": data
    }


# Q8 : Which five districts recorded the highest number of fatal accidents in 2024?
@router.get("/top-fatal-accidents")
def top_fatal_accidents(limit: int = 5):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            r.name AS district,
            COUNT(*) AS fatal_accidents

        FROM accidents a

        JOIN regions r
            ON a.region_id = r.region_id

        WHERE r.level = 'district'
        AND a.UJAHR = 2024
        AND a.UKATEGORIE = 1

        GROUP BY
            r.region_id,
            r.name

        ORDER BY fatal_accidents DESC

        LIMIT %s
    """, (limit,))

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "question": "Which districts recorded the highest number of fatal accidents in 2024?",
        "year": 2024,
        "returned_results": len(data),
        "results": data
    }


# Q9
# How many bicycle accidents occurred in Dresden in 2024?
@router.get("/bicycle-accidents")
def bicycle_accidents(
    location: str,
    year: int
):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            COUNT(*) AS bicycle_accidents
        FROM accidents a

        JOIN regions r
            ON a.region_id = r.region_id

        WHERE r.name LIKE CONCAT('%', %s, '%')
        AND a.UJAHR = %s
        AND a.IstRad = 1
    """, (location, year))

    data = cursor.fetchone()

    cursor.close()
    conn.close()

    return {
        "location": location,
        "year": year,
        "bicycle_accidents": data["bicycle_accidents"]
    }

# Q10
# "Which districts in Sachsen recorded the lowest number of accidents in 2023?"
@router.get("/lowest-accidents")
def lowest_accidents(
    year: int = 2023,
    limit: int = 5
):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            r.name AS district,
            COUNT(a.accident_id) AS total_accidents

        FROM accidents a

        JOIN regions r
            ON a.region_id = r.region_id

        WHERE r.level = 'district'
        AND r.ags LIKE '14%%'
        AND a.UJAHR = %s

        GROUP BY
            r.region_id,
            r.name

        ORDER BY total_accidents ASC

        LIMIT %s
    """, (year, limit))

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "question": f"Which districts in Sachsen recorded the lowest number of accidents in {year}?",
        "year": year,
        "total_results": len(data),
        "results": data
    }