import pandas as pd
import re

input_file = r"g:\Integration_With_Accidents_In_Germany\dataset folder\AGS Region\GV100AD_31052026.csv"

regions = []

current_state = None

with open(input_file, "r", encoding="latin1", errors="ignore") as f:

    for line in f:

        line = line.strip()

        if not line:
            continue

        parts = re.split(r"\s{2,}|\t+", line)

        # ------------------------
        # STATE RECORD
        # ------------------------
        if line.startswith("102"):

            if len(parts) >= 2:
                current_state = parts[1].strip()

            continue

        # ------------------------
        # DISTRICT RECORD
        # ------------------------
        if line.startswith("402"):

            if len(parts) < 3:
                continue

            code_part = parts[0]

            district_code = code_part[-4:]

            district_name = parts[1].strip()

            district_type = ""

            district_seat = ""

            for p in parts[2:]:

                p = p.strip()

                if p.isdigit():

                    if p in ["41", "43", "44"]:
                        district_type = p

                else:

                    district_seat = p

            regions.append({
                "district_code": district_code,
                "district_name": district_name,
                "district_seat": district_seat,
                "district_type": district_type,
                "state": current_state
            })

df = pd.DataFrame(regions)

df = df.drop_duplicates(subset=["district_code"])

df = df[df["district_type"].isin(["41", "43", "44"])]

df = df.sort_values("district_code")

output_file = r"g:\Integration_With_Accidents_In_Germany\dataset folder\AGS Region\regions_final.csv"

df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print(df.head(20))
print("Rows:", len(df))
print("Saved:", output_file)