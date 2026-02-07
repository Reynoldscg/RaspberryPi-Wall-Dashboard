# 🏠 Raspberry Pi Family Dashboard

A beautiful, self-hosted digital wall display for Raspberry Pi featuring clock, weather, calendar, photo slideshow, and optional solar production monitoring.

![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi%203/4-red) ![OS](https://img.shields.io/badge/OS-Raspberry%20Pi%20OS-green) ![License](https://img.shields.io/badge/License-MIT-blue)

## ✨ Features

- **⏰ Real-time Clock** - 12-hour format with automatic updates
- **🌤️ Weather Widget** - Current conditions, AQI, and wind via Weatherbit.io & OpenWeatherMap
- **📅 Multi-Calendar** - Multiple Google Calendars with color-coded events
- **📸 Photo Slideshow** - Rotating photos from Dropbox with smooth transitions
- **☀️ Solar Monitoring** (Optional) - APsystems ECU-R-PRO solar production data
- **🖥️ Kiosk Mode** - Full-screen, maintenance-free operation
- **🔄 Auto-Recovery** - Survives power outages and reboots

## 📸 Screenshot

The dashboard features an elegant gradient blue design with:
- Left column: Clock, Weather, Solar (optional), Photo slideshow
- Right column: Full month calendar view with event details

## 🛠️ Hardware Requirements

- **Raspberry Pi 3 Model B** (or newer, tested on Pi 3B and Pi 4)
- **32GB+ microSD card** (Class 10 recommended)
- **5V 2.5A+ power supply** (micro-USB for Pi 3, USB-C for Pi 4)
- **HDMI display** (monitor or TV)
- **Internet connection** (WiFi or Ethernet)

## 📋 API Requirements

You'll need free API keys from:

1. **[Weatherbit.io](https://www.weatherbit.io/api)** - Weather data (free tier: 50 calls/day)
2. **[OpenWeatherMap](https://openweathermap.org/api)** - Air Quality Index (free tier)
3. **[Dropbox](https://www.dropbox.com/developers/apps)** - Photo hosting
4. **[Google Calendar API](https://console.cloud.google.com/)** - Calendar integration

### Optional (for Solar):
5. **APsystems ECU-R-PRO** - Local network access to solar inverter

## 🚀 Quick Start

### 1. Prepare Your Raspberry Pi

Flash Raspberry Pi OS (Lite or Desktop) to your microSD card:

```bash
# Download Raspberry Pi Imager: https://www.raspberrypi.com/software/
# Choose: Raspberry Pi OS (64-bit) or Raspberry Pi OS Lite (64-bit)
# Configure WiFi and SSH during imaging
```

### 2. SSH into Your Pi

```bash
ssh pi@raspberrypi.local
# Or use your Pi's IP address
```

### 3. Clone This Repository

```bash
cd ~
git clone https://github.com/yourusername/raspberry-pi-dashboard.git
cd raspberry-pi-dashboard
```

### 4. Configure Your Dashboard

Edit `dashboard.html` and update the `CONFIG` section with your API credentials:

```javascript
const CONFIG = {
  // Dropbox Configuration
  DROPBOX_APP_KEY: 'your_app_key_here',
  DROPBOX_APP_SECRET: 'your_app_secret_here',
  DROPBOX_REFRESH_TOKEN: 'your_refresh_token_here',
  DROPBOX_FOLDER_PATH: '/Photos/Dashboard Photos',

  // Google Calendar Configuration
  GOOGLE_CLIENT_ID: 'your_client_id.apps.googleusercontent.com',
  GOOGLE_CLIENT_SECRET: 'GOCSPX-your_client_secret',
  GOOGLE_REFRESH_TOKEN: 'your_refresh_token_here',
  CALENDAR_IDS: [
    'your_calendar@gmail.com',
  ],

  // Calendar Colors (customize per calendar)
  CALENDAR_COLORS: {
    'your_calendar@gmail.com': { bg: '#6AC5FE', text: '#FFFFFF' },
  },

  // Weather Configuration
  WEATHERBIT_API_KEY: 'your_weatherbit_api_key',
  LATITUDE: '33.7701',  // Your location
  LONGITUDE: '-118.1937',
  OPENWEATHER_API_KEY: 'your_openweather_api_key',

  // Solar Configuration (optional)
  SOLAR_API_URL: 'http://localhost:8080/api/solar',
  SOLAR_ENABLED: false,  // Set to true to enable solar
};
```

### 5. Run the Dashboard

#### Option A: Simple Browser (Development/Testing)

```bash
# Install a lightweight browser if needed
sudo apt update
sudo apt install -y chromium-browser

# Open the dashboard
chromium-browser --kiosk --noerrdialogs --disable-infobars \
  --disable-session-crashed-bubble file:///home/pi/raspberry-pi-dashboard/dashboard.html
```

#### Option B: Auto-Start on Boot (Production)

Create an autostart script:

```bash
mkdir -p ~/.config/autostart
nano ~/.config/autostart/dashboard.desktop
```

Add:

```ini
[Desktop Entry]
Type=Application
Name=Dashboard
Exec=chromium-browser --kiosk --noerrdialogs --disable-infobars --disable-session-crashed-bubble file:///home/pi/raspberry-pi-dashboard/dashboard.html
```

Reboot to test:

```bash
sudo reboot
```

## ☀️ Solar Monitoring Setup (Optional)

If you have an APsystems ECU-R-PRO solar inverter:

### 1. Configure Solar Server

Edit `solar_server.py` and update the configuration:

```python
ECU_IP = "192.168.x.x"  # Your ECU's IP address
ECU_PORT = 8899
ECU_ID = "your_ecu_id"
SERVER_PORT = 8080
```

### 2. Test the Solar Server

```bash
python3 solar_server.py
```

You should see:
```
☀️  Solar API Server running on port 8080
   ECU: 192.168.x.x:8899
   Endpoint: http://localhost:8080/api/solar
```

Test it:
```bash
curl http://localhost:8080/api/solar
```

### 3. Install as System Service

```bash
sudo nano /etc/systemd/system/solar-server.service
```

Add:

```ini
[Unit]
Description=Solar API Server for Dashboard
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/raspberry-pi-dashboard
ExecStart=/usr/bin/python3 /home/pi/raspberry-pi-dashboard/solar_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable solar-server.service
sudo systemctl start solar-server.service
sudo systemctl status solar-server.service
```

### 4. Enable Solar in Dashboard

Edit `dashboard.html` and set:

```javascript
SOLAR_ENABLED: true,
```

## 🔧 API Setup Guides

### Dropbox Setup

1. Go to [Dropbox App Console](https://www.dropbox.com/developers/apps)
2. Click "Create App"
3. Choose "Scoped access" and "Full Dropbox"
4. Name your app (e.g., "Family Dashboard")
5. Under "Permissions", enable:
   - `files.metadata.read`
   - `files.content.read`
6. Generate a refresh token using the [Dropbox OAuth Guide](https://www.dropbox.com/developers/documentation/http/documentation#authorization)

### Google Calendar Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable "Google Calendar API"
4. Create OAuth 2.0 credentials (Desktop application)
5. Use [OAuth Playground](https://developers.google.com/oauthplayground/) to get refresh token:
   - Select "Calendar API v3"
   - Authorize and exchange for refresh token

### Weather API Setup

**Weatherbit.io:**
1. Sign up at [Weatherbit.io](https://www.weatherbit.io/api)
2. Copy your API key from the dashboard

**OpenWeatherMap:**
1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Copy your API key (wait 10 minutes for activation)

## 📁 Project Structure

```
raspberry-pi-dashboard/
├── dashboard.html          # Main dashboard file
├── solar_server.py         # Optional solar monitoring server
├── config.example.js       # Example configuration
├── README.md               # This file
└── LICENSE                 # MIT License
```

## 🎨 Customization

### Change Colors

Edit the CSS in `dashboard.html`:

```css
body {
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
}
```

### Add More Calendars

In the CONFIG section:

```javascript
CALENDAR_IDS: [
  'calendar1@gmail.com',
  'calendar2@gmail.com',
  'calendar3@group.calendar.google.com',
],

CALENDAR_COLORS: {
  'calendar1@gmail.com': { bg: '#6AC5FE', text: '#FFFFFF' },
  'calendar2@gmail.com': { bg: '#F88379', text: '#FFFFFF' },
  'calendar3@group.calendar.google.com': { bg: '#98FBCB', text: '#000000' },
},
```

### Adjust Refresh Intervals

```javascript
PHOTO_INTERVAL: 30000,      // 30 seconds
WEATHER_REFRESH: 1800000,   // 30 minutes
SOLAR_REFRESH: 60000,       // 1 minute
```

## 🐛 Troubleshooting

### Dashboard won't load
- Check browser console (F12) for errors
- Verify all API keys are correct
- Check network connectivity

### Photos not showing
- Verify Dropbox folder path is correct
- Check Dropbox permissions
- Ensure photos folder has images

### Weather not loading
- Verify API keys are active
- Check latitude/longitude coordinates
- Ensure you haven't exceeded API rate limits

### Solar not working
- Verify ECU IP address is correct
- Check that solar_server.py is running
- Ensure SOLAR_ENABLED is set to true in dashboard.html

### Calendar events not showing
- Check Google Calendar API is enabled
- Verify refresh token is valid
- Ensure calendar IDs are correct

## 🔒 Security Notes

- **Never commit API keys to public repositories**
- Store credentials in environment variables for production
- Use read-only API permissions where possible
- Keep your Raspberry Pi OS updated: `sudo apt update && sudo apt upgrade`

## 📝 License

MIT License - feel free to use and modify for personal or commercial projects.

## 🙏 Acknowledgments

- Weather data from Weatherbit.io and OpenWeatherMap
- Calendar integration via Google Calendar API
- Photo hosting via Dropbox API
- Solar monitoring for APsystems ECU-R-PRO inverters

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

**Made with ❤️ for families who want a beautiful, informative dashboard in their home**
