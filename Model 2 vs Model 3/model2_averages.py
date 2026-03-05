import pandas as pd

file_name = "Model_2_Results.xlsx"
sheet_name = "Final_Test"

df = pd.read_excel(file_name, sheet_name=sheet_name)

metric_cols = [
    "Test_Accuracy",
    "Precision_(-1)", "Recall_(-1)", "F1_(-1)",
    "Precision_(1)", "Recall_(1)", "F1_(1)"
]

def best_model(subdf):
    return subdf.sort_values("F1_(-1)", ascending=False).iloc[0]

def avg_top3(subdf):
    return subdf[metric_cols].mean()

prediction_horizons = [
    "Total Ret 3 Mo (Daily)",
    "Total Ret 6 Mo (Daily)",
    "Total Ret 1 Yr (Daily)"
]

rows = []

for horizon in prediction_horizons:
    temp = df[df["Target"] == horizon]

    best = best_model(temp)
    avg3 = avg_top3(temp)

    rows.append(["Best_" + horizon] + list(best[metric_cols]))
    rows.append(["Average_top3_" + horizon] + list(avg3))

overall_avg = df[metric_cols].mean()
rows.append(["Average_all_9"] + list(overall_avg))

final_df = pd.DataFrame(
    rows,
    columns=["Description"] + metric_cols
)

final_df.to_excel("Model_2_Comparison_Table.xlsx", index=False)

print("Done ✅")