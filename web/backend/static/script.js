document.getElementById('searchBtn').addEventListener('click', getWeather)

async function getWeather() {
    const city = document.getElementById('cityInput').value

    const response = await fetch('/api/weather?city=' + city)
    const filtered = await response.json()

    const result = document.getElementById('result')

    if (filtered.status === 'error') {
        result.innerHTML = `<p>Error: ${filtered.message}</p>`
        return
    }

    result.innerHTML = `
    <div class='weather-city'>${filtered.city}</div>
    <div class='weather-temp'>${filtered.temperature}°C</div>
    <div class='weather-desc'>${filtered.description}</div>

    <div class="weather-extra">
        <div class="extra-item">
            <span class="extra-label">💧 Humidity</span>
            <span class="extra-value">${filtered.humidity}%</span>
        </div>
        <div class="extra-item">
            <span class="extra-label">🌬️ Wind</span>
            <span class="extra-value">${filtered.wind} m/s</span>
        </div>
    </div>

    <img class='weather-icon' src='https://openweathermap.org/img/wn/${filtered.icon}@2x.png'>
`

    result.classList.remove('fade-in')
    void result.offsetWidth
    result.classList.add('fade-in')
}
