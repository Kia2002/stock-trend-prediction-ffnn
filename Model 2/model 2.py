import pandas as pd
import numpy as np
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, accuracy_score, f1_score


folder_putanja = r'C:\Users\Aleksa\Documents\Predvidjanje\Model 2'
ulazni_fajl = os.path.join(folder_putanja, 'stocks - healthcare - fixed input.xlsx')
izlazni_fajl = os.path.join(folder_putanja, 'Model_2_Results.xlsx')


df = pd.read_excel(ulazni_fajl)

y_cols = df.columns[15:18]
X_cols = df.columns[18:97]

df_clean = df.copy()

df_clean[y_cols] = df_clean[y_cols].fillna(df_clean[y_cols].mean())
df_clean[X_cols] = df_clean[X_cols].fillna(df_clean[X_cols].mean())


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

list_for_sheet1 = []
temp_for_selection = []

print("Starting training and selection of binary models...")


for target_name in y_cols:

    series = df_clean[target_name]
    X = df_clean[X_cols]

    try:
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, series, test_size=0.15, random_state=42
        )
    except:
        continue

    X_train, X_val, y_train_raw, y_val_raw = train_test_split(
        X_temp, y_temp, test_size=0.1765, random_state=42
    )

   
    r = 10

    def trend_label(x):
        if x > r:
            return 1
        elif x < -r:
            return -1
        else:
            return 0

    y_train = y_train_raw.apply(trend_label)
    y_val   = y_val_raw.apply(trend_label)
    y_test  = y_test.apply(trend_label)

    
    train_mask = y_train != 0
    val_mask   = y_val != 0
    test_mask  = y_test != 0

    X_train = X_train[train_mask]
    y_train = y_train[train_mask]

    X_val = X_val[val_mask]
    y_val = y_val[val_mask]

    X_test = X_test[test_mask]
    y_test = y_test[test_mask]

    print("-" * 30)
    print(f"Target: {target_name}")
    print("Class balance in training set:")
    print(y_train.value_counts())
    print("-" * 30)

    if len(np.unique(y_train)) < 2:
        continue

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_val_s = scaler.transform(X_val)
    X_test_s = scaler.transform(X_test)

    for name, layers in architectures.items():

        clf = MLPClassifier(
            hidden_layer_sizes=layers,
            max_iter=2000,
            alpha=0.001,
            random_state=42,
            solver='adam',
            early_stopping=True,
            n_iter_no_change=10,
            validation_fraction=0.2
        )

        counts = y_train.value_counts()
        negative_weight = (counts[1] / counts[-1]) * 1.5
        sample_weights = y_train.map({1: 1.0, -1: negative_weight})

        clf.fit(X_train_s, y_train, sample_weight=sample_weights)

        y_tr_pred = clf.predict(X_train_s)
        y_v_pred = clf.predict(X_val_s)

        rep_v = classification_report(y_val, y_v_pred, output_dict=True, zero_division=0)

        prec_pos = rep_v.get("1", {}).get("precision", 0)
        prec_neg = rep_v.get("-1", {}).get("precision", 0)

        f1_tr = f1_score(y_train, y_tr_pred, average='binary', pos_label=1)
        f1_v = f1_score(y_val, y_v_pred, average='binary', pos_label=1)
        gap = abs(f1_tr - f1_v)

        s_score = (prec_pos * prec_neg) - gap

        meta = {
            "Target": target_name,
            "Architecture": name,
            "Precision_(1)": prec_pos,
            "Precision_(-1)": prec_neg,
            "Gap": gap,
            "Selection_Score": s_score
        }

        list_for_sheet1.append(meta)

        temp_for_selection.append({
            "model": clf,
            "meta": meta,
            "scaler": scaler,
            "X_test": X_test_s,
            "y_test": y_test
        })



final_test_list = []
df_pre = pd.DataFrame(list_for_sheet1)

for target_name in y_cols:

    top_indices = (
        df_pre[df_pre["Target"] == target_name]
        .sort_values("Selection_Score", ascending=False)
        .head(3)
        .index
    )

    for idx in top_indices:

        t = temp_for_selection[idx]
        y_pred = t["model"].predict(t["X_test"])
        rep = classification_report(t["y_test"], y_pred, output_dict=True, zero_division=0)

        final_test_list.append({
            "Target": t["meta"]["Target"],
            "Architecture": t["meta"]["Architecture"],
            "Test_Accuracy": accuracy_score(t["y_test"], y_pred),
            "Precision_(-1)": rep.get("-1", {}).get("precision", 0),
            "Recall_(-1)": rep.get("-1", {}).get("recall", 0),
            "F1_(-1)": rep.get("-1", {}).get("f1-score", 0),
            "Precision_(1)": rep.get("1", {}).get("precision", 0),
            "Recall_(1)": rep.get("1", {}).get("recall", 0),
            "F1_(1)": rep.get("1", {}).get("f1-score", 0),
        })



with pd.ExcelWriter(izlazni_fajl) as writer:

    df_pre.to_excel(writer, sheet_name="Model_Selection", index=False)
    pd.DataFrame(final_test_list).to_excel(writer, sheet_name="Final_Test", index=False)