from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import pandas as pd
import traffic_info
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import requests



app = Flask(__name__)
CORS(app)


# Lineapiの設定
LINE_CHANNEL_ACCESS_TOKEN = "ZXXqpHDOoRhrrao0uKH5OBQiQIE12URz/Vdha0ztjtyO05MtgPkFQUCRMfzSsC4pwUjVnG5YFkHKOx9O6g7cxu8XMBvVIk0sHaCqjaWMDkhDLAuA1R1XHLknMtae621D+Su7IqxKnqgFZlRo5m3FAAdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "e6cbc018be87e7f53e4f50c6cc71b217"
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


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


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


# LINEメッセージ受信時、渋滞情報と受け取った時に最新の情報を取得して返信できるようにする
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    if "渋滞情報" in user_message:
        traffic_info_text = get_traffic_info_text()
        reply_message(event.reply_token, traffic_info_text)
    else:
        reply_message(event.reply_token, "「渋滞情報」と送ると、最新の交通情報をお知らせします！")


# /trafficから最新をロードして交通情報を取得し、テキストに整形
def get_traffic_info_text():
    TRAFFIC_API_URL = "http://127.0.0.1:5555/traffic"
    response = requests.get(TRAFFIC_API_URL)
    if response.status_code == 200:
        data = response.json()
        if "data" in data:
            traffic_data = data["data"]
            message = "🚗 最新の渋滞情報 🚗\n"
            for item in traffic_data[:5]:  # 5件まで表示
                message += f"\n🛑 {item['区間']}\n📌 {item['規制内容']} - {item['原因']}\n"
            return message
        else:
            return "⚠ 渋滞情報を取得できませんでした。"
    else:
        return "⚠ 交通情報の API に接続できませんでした。"


# LINE に返信する関数
def reply_message(reply_token, message):
    line_bot_api.reply_message(reply_token, TextSendMessage(text=message))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=True)

