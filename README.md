# Weather App (Flask + OpenWeatherMap)

Simple Weather App with a clean modern UI. Features:
- Search weather city-wise (by city name)
- Displays current weather + 5-day forecast
- Recent searches saved in browser (localStorage)
- Responsive modern UI using Bootstrap
- Backend proxy implemented in Flask to keep API key secure

## Setup

1. Clone or download the project.
2. Get a free API key from OpenWeatherMap: https://openweathermap.org/api
   - Sign up and copy your API key.
3. Set environment variable `OWM_API_KEY` to your key.
   - Linux / macOS: `export OWM_API_KEY=your_api_key`
   - Windows PowerShell: `setx OWM_API_KEY "your_api_key"` (then restart terminal)
   - Or place the key directly in `app.py` (not recommended).

4. (Optional) Create a Python virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate   # Linux / macOS
venv\\Scripts\\activate    # Windows
```

5. Install requirements:
```bash
pip install -r requirements.txt
```

6. Run the app:
```bash
export OWM_API_KEY=your_api_key   # or set in system
python app.py
```

7. Open http://127.0.0.1:5000 in your browser.

## Files
- `app.py` - Flask backend (proxies requests to OpenWeatherMap)
- `templates/index.html` - Frontend HTML
- `static/css/style.css` - Styles
- `static/js/main.js` - Frontend JS (axios used)
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Notes
- The app uses OpenWeatherMap One Call API for current + daily forecast.
- If you want to deploy, keep your API key secret (use environment variables).
- Feel free to extend the UI, add icons, caching, or user preferences.
