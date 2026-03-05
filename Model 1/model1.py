import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import r2_score

folder_putanja = r'C:\Users\Aleksa\Documents\Predvidjanje\Model 1'
ulazni_fajl = os.path.join(folder_putanja, 'stocks - healthcare - fixed input.xlsx')
izlazni_fajl = os.path.join(folder_putanja, 'Model_1_Results.xlsx')

df = pd.read_excel(ulazni_fajl)
y_cols = df.columns[15:18]   
X_cols = df.columns[18:97]   

df_clean = df.copy()
for col in X_cols:
    df_clean[col] = df_clean[col].fillna(df_clean[col].mean())
for col in y_cols:
    df_clean[col] = df_clean[col].fillna(df_clean[col].mean())


architectures = {
    "1_sloj_10": (10,), "1_sloj_25": (25,), "1_sloj_50": (50,),
    "2_sloja_10x10": (10, 10), "2_sloja_25x25": (25, 25), "2_sloja_50x50": (50, 50),
    "3_sloja_10x10x10": (10, 10, 10), "3_sloja_25x25x25": (25, 25, 25), "3_sloja_50x50x50": (50, 50, 50),
    "5_slojeva_75x50x25x10x3": (75, 50, 25, 10, 3)
}

selection_list = []
top3_test_list = []

for target in y_cols:
    print(f"\n>>> ANALYSIS AND SELECTION FOR: {target} <<<")
    X = df_clean[X_cols]
    y = df_clean[target]

    X_train_temp, X_test, y_train_temp, y_test = train_test_split(
        X, y, test_size=0.15, random_state=42
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_temp, y_train_temp, test_size=0.176, random_state=42
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)

    temp_list_for_top3 = []

    for name, layers in architectures.items():
        model = MLPRegressor(
            hidden_layer_sizes=layers, 
            activation='relu', 
            solver='adam', 
            alpha=0.5, 
            max_iter=2000, 
            random_state=42,
            early_stopping=True, 
            n_iter_no_change=10
        )
        model.fit(X_train_scaled, y_train)

        t_r2 = r2_score(y_train, model.predict(X_train_scaled))
        v_r2 = r2_score(y_val, model.predict(X_val_scaled))
        
        gap = t_r2 - v_r2
        s_score = v_r2 - 0.5 * abs(gap)

        result_meta = {
            "Target": target,
            "Architecture": name,
            "Train R2": t_r2,
            "Val R2": v_r2,
            "Gap": gap,
            "Selection_Score": s_score
        }
        selection_list.append(result_meta)
        
        temp_list_for_top3.append({
            "model": model, 
            "name": name, 
            "score": s_score, 
            "val_r2": v_r2
        })

    top3_candidates = sorted(temp_list_for_top3, key=lambda x: x["score"], reverse=True)[:3]
    
    print(f"Testing Top 3 architectures for {target}...")
    for item in top3_candidates:
        winning_model = item["model"]
        test_preds = winning_model.predict(X_test_scaled)
        t_r2_final = r2_score(y_test, test_preds)
        
        top3_test_list.append({
            "Target": target,
            "Architecture": item["name"],
            "Val R2": item["val_r2"],
            "FINAL_TEST_R2": t_r2_final
        })

with pd.ExcelWriter(izlazni_fajl) as writer:
    pd.DataFrame(selection_list).to_excel(writer, sheet_name='All_Architectures_Selection', index=False)
    pd.DataFrame(top3_test_list).to_excel(writer, sheet_name='Top3_Final_Test', index=False)