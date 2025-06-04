import json
from collections import defaultdict  # 升級版字典，方便資料歸類 寫程式不用一直檢查key有沒有存在
from datetime import datetime, timedelta, timezone  # 時間處理工具包，現在時間、格式化日期字串/ 現在+-7天 / 指定時區

def get_weather_summary_plus(station_full_name):
    # 直接讀氣象署載下來的 .json
    with open("response_1749029442984.json", encoding="utf-8") as f:
        data = json.load(f)
    stations = data["records"]["Station"]

    #locations = data["records"]["Locations"][0]["Location"]
    #location_data = next((loc for loc in locations if loc["LocationName"] == location), None)
    #if not location_data:
    #    return f"找不到{location}的資料"
    
    # station_full_name 例如 "基隆（基隆市 仁愛區）"
    # 解析天氣資料
    result = []
    for s in stations:
        full_name = f"{s['StationName']}（{s['GeoInfo']['CountyName']} {s['GeoInfo']['TownName']}）"
        if full_name == station_full_name:
            e = s["WeatherElement"]
            obs_time = s["ObsTime"]["DateTime"]
            out = (
                f"{full_name}\n  觀測時間：{obs_time}"
                f"\n  天氣現象：{e.get('Weather', 'N/A')}"
                f"\n  溫度：{e.get('AirTemperature', 'N/A')}°C"
                f"\n  濕度：{e.get('RelativeHumidity', 'N/A')}%"
                f"\n  風速：{e.get('WindSpeed', 'N/A')} m/s"
                f"\n  降雨量：{e.get('Now', {}).get('Precipitation', 'N/A')} mm"
            )
            result.append(out)
    if not result:
        return f"找不到{station_full_name}的即時天氣資料"
    return "\n".join(result)

if __name__ == "__main__":
    # 可以直接試著印出某個全名（對應選單用）
    print(get_weather_summary_plus("基隆（基隆市 仁愛區）"))
