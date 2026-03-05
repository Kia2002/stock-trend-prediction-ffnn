import pandas as pd


file_name = "Model_3_Results.xlsx"
sheet_name = "Final_Test_List"

df = pd.read_excel(file_name, sheet_name=sheet_name)

metric_columns = [
    "Test_Accuracy",
    "Precision_-1", "Recall_-1", "F1_-1",
    "Precision_1", "Recall_1", "F1_1"
]

def get_best_model(sub_df):
    return sub_df.sort_values("F1_-1", ascending=False).iloc[0]

def average_top3(sub_df):
    return sub_df[metric_columns].mean()


prediction_horizons = [
    "Total Ret 3 Mo (Daily)",
    "Total Ret 6 Mo (Daily)",
    "Total Ret 1 Yr (Daily)"
]

rows = []

for horizon in prediction_horizons:
    temp = df[df["Target"] == horizon]

    best = get_best_model(temp)
    avg3 = average_top3(temp)

    rows.append(["Best_" + horizon] + list(best[metric_columns]))
    rows.append(["Average_top3_" + horizon] + list(avg3))


overall_average = df[metric_columns].mean()
rows.append(["Average_all_9"] + list(overall_average))


final_df = pd.DataFrame(
    rows,
    columns=["Description"] + metric_columns
)


final_df.to_excel("Model_3_Comparison_Table.xlsx", index=False)

print("Done ✅")