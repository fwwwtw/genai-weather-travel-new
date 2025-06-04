import streamlit as st  # 把Python程式變成網頁介面
import json
import google.generativeai as genai  # Google出的Gemini AI SDK，可以在Python裡直接呼叫Gemini
from weather_summary_plus import get_weather_summary_plus  # 我寫的天氣摘要功能，直接import進主程式用

# 設定 Google Gemini 金鑰
api_key = st.text_input("請輸入 Google Gemini API 金鑰：", type="password")
if api_key:
    genai.configure(api_key=api_key)

# 從 json 檔案自動抓可選地名
def get_all_stations():
    with open("response_1749029442984.json", encoding="utf-8") as f:
        data = json.load(f)
    stations = data["records"]["Station"]
    return [
        f"{s['StationName']}（{s['GeoInfo']['CountyName']} {s['GeoInfo']['TownName']}）"
        for s in stations
    ]

st.title("☁️ 全台即時天氣與 Gemini 旅遊建議")

station_list = get_all_stations()
selected_station = st.selectbox("請選擇測站", station_list)
#user_pref = st.selectbox("請選擇旅遊偏好：", ["輕鬆自然系🌿", "熱血戶外型🏃🏻‍♂️‍➡️", "文化深度派🏛️", 
#                                      "網美必備💅🏻", "躲太陽派😶‍🌫️", "家庭親子行👨🏻‍👩🏻‍👧🏻‍👦🏻"])  # 預設一些給選擇障礙的選
user_pref_default = st.selectbox(
    "請選擇旅遊偏好（可不選）",
    ["請選擇", "輕鬆自然系🌿", "熱血戶外型🏃🏻‍♂️‍➡️", "文化深度派🏛️","網美必備💅🏻", "躲太陽派😶‍🌫️", "家庭親子行👨🏻‍👩🏻‍👧🏻‍👦🏻"],   # 預設一些給選擇障礙的選
    index=0
)
user_pref_custom = st.text_input("或自行輸入偏好需求（可複選描述）")

# 實際丟給 AI 的偏好
user_pref = user_pref_custom if user_pref_custom.strip() else user_pref_default


if st.button("🔎查詢天氣與 AI 建議") and api_key:
    with st.spinner("查詢天氣與旅遊建議生成中..."):
        weather_info = get_weather_summary_plus(selected_station)
        if "找不到" in weather_info or "查無" in weather_info or "錯誤" in weather_info:
            st.error(weather_info)
        else:
            st.subheader("📑 天氣摘要：")
            st.write(weather_info)

            prompt = f"""
你是一位專業台灣旅遊顧問，請根據下方「天氣預報摘要」與「旅遊偏好」：
1. 提供 1 份 2 天 1 夜的旅遊行程建議（地點、活動、拍照打卡景點），盡量搭配天氣狀況安排最合適的活動。
2. 回答內容要有 emoji，風格要活潑一點，讓人想要馬上出門。
3. 不要直接複製天氣摘要，要根據天氣狀況給出專屬旅遊建議。
4. 以條列式清楚整理行程內容，結尾可以給貼心提醒，不要重複資料，請融合判斷給出貼心推薦。
（可以用 emoji，也能提醒注意事項）。
【天氣預報摘要】
{weather_info}
【旅遊偏好】
{user_pref}
"""

            try:
                model = genai.GenerativeModel("models/gemini-1.5-flash-001")
                resp = model.generate_content(prompt)
                ai_suggest = resp.text
                st.subheader("🤖 Gemini 旅遊建議：")
                st.write(ai_suggest)
            except Exception as e:
                st.error(f"Gemini 回應錯誤：{e}")

st.caption("※ 本系統支援全國所有即時觀測站！") 
