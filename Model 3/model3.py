import pandas as pd
import numpy as np
import os
from scipy.stats import norm

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, accuracy_score, f1_score


folder_putanja = r'C:\Users\Aleksa\Documents\Predvidjanje\Model 3'
ulazni_fajl = os.path.join(folder_putanja, 'stocks - healthcare - fixed input.xlsx')
izlazni_fajl = os.path.join(folder_putanja, 'Model_3_Results.xlsx')

df = pd.read_excel(ulazni_fajl)

y_cols = ['Total Ret 3 Mo (Daily)',
          'Total Ret 6 Mo (Daily)',
          'Total Ret 1 Yr (Daily)']

X_cols = df.columns[18:97]

df_clean = df.copy()
df_clean[y_cols] = df_clean[y_cols].fillna(df_clean[y_cols].mean())
df_clean[X_cols] = df_clean[X_cols].fillna(df_clean[X_cols].mean())


def max_min_normalized(series):
    s = series.sort_values()
    v_min, v_max = s.iloc[3], s.iloc[-4]
    return (series.clip(lower=v_min, upper=v_max) - v_min) / (v_max - v_min)

def cdf_normalized(series):
    mu, sigma = series.mean(), series.std()
    return pd.Series(norm.cdf(series, loc=mu, scale=sigma if sigma > 0 else 1),
                     index=series.index)


groups = {}
for col in X_cols:
    base = col.replace('_1Yr_Avg', '').replace('_Value', '').split('_')[0].split(' ')[0]
    groups.setdefault(base, []).append(col)

def aggregate_data(data):
    pond = pd.DataFrame(index=data.index)
    logi = pd.DataFrame(index=data.index)

    for base, cols in groups.items():
        if len(cols) >= 3:
            pond[base] = 0.5*data[cols[0]] + 0.25*data[cols[1]] + 0.25*data[cols[2]]
            logi[base] = data[cols[0]] * (data[cols[1]] + data[cols[2]] - data[cols[1]]*data[cols[2]])
        elif len(cols) == 2:
            pond[base] = 0.5*data[cols[0]] + 0.5*data[cols[1]]
            logi[base] = data[cols[0]] * data[cols[1]]
        else:
            pond[base] = data[cols[0]]
            logi[base] = data[cols[0]]

    return pond, logi

X_mm_pond, X_mm_logi = aggregate_data(df_clean[X_cols].apply(max_min_normalized))
X_cdf_pond, X_cdf_logi = aggregate_data(df_clean[X_cols].apply(cdf_normalized))

all_input_sets = {
    'MM_Ponderisano': X_mm_pond,
    'MM_Logicko': X_mm_logi,
    'CDF_Ponderisano': X_cdf_pond,
    'CDF_Logicko': X_cdf_logi
}


r = 10

def trend_label(x):
    if x > r:
        return 1
    elif x < -r:
        return -1
    return 0


architectures = {
    "1_sloj_10": (10,),
    "1_sloj_25": (25,),
    "1_sloj_50": (50,),
    "2_sloja_10x10": (10, 10),
    "2_sloja_25x25": (25, 25),
    "2_sloja_50x50": (50, 50),
    "3_sloja_10x10x10": (10, 10, 10),
    "3_sloja_25x25x25": (25, 25, 25),
    "3_sloja_50x50x50": (50, 50, 50),
    "5_slojeva_75x50x25x10x3": (75, 50, 25, 10, 3)
}

lista_za_sheet1 = []
privremena_za_selekciju = []

for set_name, X_data in all_input_sets.items():
    for target_name in y_cols:

        y_raw = df_clean[target_name]

        X_temp, X_test, y_temp, y_test_raw = train_test_split(
            X_data, y_raw, test_size=0.15, random_state=42
        )

        test_index = X_test.index

        X_train, X_val, y_train_raw, y_val_raw = train_test_split(
            X_temp, y_temp, test_size=0.1765, random_state=42
        )

        y_train = y_train_raw.apply(trend_label)
        y_val   = y_val_raw.apply(trend_label)
        y_test  = y_test_raw.apply(trend_label)

        train_mask = y_train != 0
        val_mask   = y_val != 0
        test_mask  = y_test != 0

        X_train, y_train = X_train[train_mask], y_train[train_mask]
        X_val, y_val     = X_val[val_mask], y_val[val_mask]
        X_test, y_test   = X_test[test_mask], y_test[test_mask]
        test_index       = test_index[test_mask]

        if len(np.unique(y_train)) < 2:
            continue

        scaler = StandardScaler()
        X_train_s = scaler.fit_transform(X_train)
        X_val_s   = scaler.transform(X_val)
        X_test_s  = scaler.transform(X_test)

        for arch_name, layers in architectures.items():

            clf = MLPClassifier(hidden_layer_sizes=layers, max_iter=2000,
                                early_stopping=True, random_state=42,
                                alpha=0.005)

            counts = y_train.value_counts()
            if -1 in counts and 1 in counts:
                tezina_neg = (counts[1] / counts[-1]) * 1.5
            else:
                tezina_neg = 1

            sample_weights = y_train.map({1: 1.0, -1: tezina_neg})

            clf.fit(X_train_s, y_train, sample_weight=sample_weights)

            y_tr_pred = clf.predict(X_train_s)
            y_v_pred  = clf.predict(X_val_s)

            rep_v = classification_report(y_val, y_v_pred, output_dict=True, zero_division=0)

            prec_pos = rep_v.get("1", {}).get("precision", 0)
            prec_neg = rep_v.get("-1", {}).get("precision", 0)

            f1_tr = f1_score(y_train, y_tr_pred, pos_label=1)
            f1_v  = f1_score(y_val, y_v_pred, pos_label=1)

            gap = abs(f1_tr - f1_v)
            s_score = 0.5 * (prec_pos * prec_neg) - gap

            meta = {
                "Combination": set_name,
                "Target": target_name,
                "Architecture": arch_name,
                "Precision_1": prec_pos,
                "Precision_-1": prec_neg,
                "Gap": gap,
                "Selection_Score": s_score
            }

            lista_za_sheet1.append(meta)

            privremena_za_selekciju.append({
                "model": clf,
                "meta": meta,
                "scaler": scaler,
                "X_test": X_test_s,
                "y_test": y_test,
                "test_index": test_index
            })


df_pre = pd.DataFrame(lista_za_sheet1)
lista_finalni_test = []

for target_name in y_cols:

    top_indices = (
        df_pre[df_pre["Target"] == target_name]
        .sort_values("Selection_Score", ascending=False)
        .head(3)
        .index
    )

    for idx in top_indices:

        t = privremena_za_selekciju[idx]

        y_pred = t["model"].predict(t["X_test"])
        rep = classification_report(t["y_test"], y_pred, output_dict=True, zero_division=0)

        lista_finalni_test.append({
            "Target": t["meta"]["Target"],
            "Combination": t["meta"]["Combination"],
            "Architecture": t["meta"]["Architecture"],
            "Test_Accuracy": accuracy_score(t["y_test"], y_pred),
            "Precision_-1": rep.get("-1", {}).get("precision", 0),
            "Recall_-1": rep.get("-1", {}).get("recall", 0),
            "F1_-1": rep.get("-1", {}).get("f1-score", 0),
            "Precision_1": rep.get("1", {}).get("precision", 0),
            "Recall_1": rep.get("1", {}).get("recall", 0),
            "F1_1": rep.get("1", {}).get("f1-score", 0),
        })


selected_networks_1yr = [
    {"Combination": "CDF_Ponderisano", "Architecture": "1_sloj_25", "Sheet": "Rank_1Yr_First"},
    {"Combination": "MM_Ponderisano", "Architecture": "1_sloj_25", "Sheet": "Rank_1Yr_Second"}
    
]

ranking_dict = {}

for t in privremena_za_selekciju:

    if t["meta"]["Target"] != 'Total Ret 1 Yr (Daily)':
        continue

    for cfg in selected_networks_1yr:

        if t["meta"]["Combination"] == cfg["Combination"] and t["meta"]["Architecture"] == cfg["Architecture"]:

            model = t["model"]

            test_index = t["test_index"]
            names = df_clean.loc[test_index, "Name"]
            y_true = t["y_test"]
            X_test = t["X_test"]

            proba = model.predict_proba(X_test)

            idx_map = {cls: i for i, cls in enumerate(model.classes_)}
            invest_score = np.array([
                proba[i, idx_map[y]] for i, y in enumerate(y_true)
            ])

            res_df = pd.DataFrame({
                "Company": names.values,
                "Trend_Class": y_true.values,
                "Investment_Score": invest_score
            })

            ranking_dict[cfg["Sheet"]] = {
                "Positive_Trend": res_df[res_df["Trend_Class"] == 1].sort_values("Investment_Score", ascending=False),
                "Negative_Trend": res_df[res_df["Trend_Class"] == -1].sort_values("Investment_Score", ascending=False)
            }


with pd.ExcelWriter(izlazni_fajl) as writer:

    df_pre.to_excel(writer, sheet_name="All_Combinations", index=False)
    pd.DataFrame(lista_finalni_test).to_excel(writer, sheet_name="Final_Test_List", index=False)

    for sheet_name, df_dict in ranking_dict.items():
        df_dict["Positive_Trend"].to_excel(writer, sheet_name=f"{sheet_name}_Pos", index=False)
        df_dict["Negative_Trend"].to_excel(writer, sheet_name=f"{sheet_name}_Neg", index=False)