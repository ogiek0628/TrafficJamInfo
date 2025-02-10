import pandas as pd

# Yahoo!交通情報URL
YAHOO_URL = "https://roadway.yahoo.co.jp/traffic/area/11/road/1091018/list?p=0.17298644687684828,0.4515545670543588&z=13&scale=4&moved=1&bbox=0.09573904550256884,0.3394596879047356,0.2502335338095918,0.5636494462053179"


# <table> を取得し、表を確認、整合する
tables = pd.read_html(YAHOO_URL)
processed_tables = []
for i, table in enumerate(tables):
    print(f"\n===== Table {i} =====")
    print(table.head())

    # 規制区間の前後が分かれている場合は統合し使わない列は削除
    if "規制区間.1" in table.columns:
        table["規制区間"] = table["規制区間"] + " → " + table["規制区間.1"]
        table = table.drop(columns=["規制区間.1"])

    # カラム名を統一し、合わない場合も考慮する
    if len(table.columns) == 3:
        table.columns = ["区間", "規制内容", "原因"]
    elif len(table.columns) == 2:
        table.columns = ["区間", "詳細"]
    else:
        table.columns = [f"カラム{i}" for i in range(len(table.columns))]

    processed_tables.append(table)

# 全データを統合して出力
df_final = pd.concat(processed_tables, ignore_index=True)
print("\n===== 統合後のデータ =====")
print(df_final)

# とりあえずCSVに保存
df_final.to_csv("traffic_info_combined.csv", index=False, encoding="utf-8-sig")
print("\nCSV ファイル 'save traffic_info_combined.csv'")
