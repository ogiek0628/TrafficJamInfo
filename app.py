from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import traffic_info

app = Flask(__name__)
CORS(app)

# 交通情報のデータを読み込む
CSV_FILE = "traffic_info_combined.csv"


# /の場合は文字列を返す
@app.route("/")
def home():
    return "交通情報 API（Yahoo!交通情報スクレイピング）"

# /trafficの場合はcsvをjsonにして返す
@app.route("/traffic", methods=["GET"])
def get_traffic_info():
    traffic_info.get_csv()
    try:
        df = pd.read_csv(CSV_FILE)  
        traffic_data = df.to_dict(orient="records")
        return jsonify({"status": "success", "data": traffic_data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=True)
