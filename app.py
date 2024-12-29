from flask import Flask, request, jsonify, render_template
import requests
import csv

app = Flask(__name__)

# 获取城市对应的 district_id
def get_district_id(city_name):
    with open('weather_district_id.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['city'] == city_name or row['district'] == city_name:
                return row['district_id']
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    try:
        city = request.json.get('city')
        if not city:
            return jsonify({'error': 'City is required'}), 400

        district_id = get_district_id(city)
        if not district_id:
            return jsonify({'error': 'Invalid city name'}), 400

        api_key = 'piMinoeoApCx3LSZDgqYsVLgPm8nHm8J'
        weather_url = f'https://api.map.baidu.com/weather/v1/?district_id={district_id}&data_type=all&ak={api_key}'
        weather_response = requests.get(weather_url)
        
        
        if weather_response.status_code != 200:
            return jsonify({'error': 'Failed to fetch weather data'}), weather_response.status_code
        else:
            print(weather_response.text)
    
        weather_data = weather_response.json()
        if weather_data.get('status') != 0:
            return jsonify({'error': weather_data.get('message', 'Unknown error')}), 400
        
        # 提取并格式化需要的数据
        now = weather_data['result']['now']
        formatted_data = {
            'temperature': now['temp'],
            'weather': now['text'],
            'dayOrNight': 'day' if '06:00' <= now['uptime'][8:13] <= '18:00' else 'night',
            'weatherIcon': f"/static/images/{now['text']}.png"  # 根据天气状况选择对应的图标
        }
        
        return jsonify({'result': formatted_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)