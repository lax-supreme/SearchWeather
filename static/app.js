// 处理提交按钮点击事件
document.getElementById('submit-btn').addEventListener('click', function() {
    const city = document.getElementById('city-input').value;
    console.log('City:', city); // 添加日志
    fetch('/weather', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ city: city })
    })
    .then(response => {
        console.log('Response:', response); // 添加日志
        return response.json();
    })
    .then(data => {
        console.log('Data:', data); // 添加日志
        if (data.error) {
            alert(data.error);
            return;
        }
        const weather = data.result;
        // 更新天气信息到页面
        document.getElementById('temperature').innerText = `温度: ${weather.temperature} °C`;
        document.getElementById('weather-condition').innerText = `天气: ${weather.weather}`;
        document.getElementById('day-night-image').src = `/static/images/${weather.dayOrNight}.png`;
        document.getElementById('weather-icon').src = `/static/images/weather.png`;
        localStorage.setItem('city', city);
    })
    .catch(error => {
        console.error('Error fetching weather data:', error);
        alert('无法获取天气信息，请稍后再试。');
    });
});

// 页面加载时检查 localStorage 中是否有城市名称
window.onload = function() {
    const city = localStorage.getItem('city');
    if (city) {
        document.getElementById('city-input').value = city;
        document.getElementById('submit-btn').click();
    }
};