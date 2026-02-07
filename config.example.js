// ============================================
// Dashboard Configuration Template
// Copy these values into the CONFIG section of dashboard.html
// ============================================

const CONFIG = {
  // ==========================================
  // DROPBOX CONFIGURATION
  // ==========================================
  // Create app at: https://www.dropbox.com/developers/apps
  // 1. Create App → Scoped access → Full Dropbox
  // 2. Enable permissions: files.metadata.read, files.content.read
  // 3. Generate refresh token via OAuth flow
  
  DROPBOX_APP_KEY: 'your_app_key_here',
  DROPBOX_APP_SECRET: 'your_app_secret_here',
  DROPBOX_REFRESH_TOKEN: 'your_refresh_token_here',
  DROPBOX_FOLDER_PATH: '/Photos/Dashboard Photos',

  // ==========================================
  // GOOGLE CALENDAR CONFIGURATION
  // ==========================================
  // Setup at: https://console.cloud.google.com/
  // 1. Create project → Enable Calendar API
  // 2. Create OAuth 2.0 credentials (Desktop app)
  // 3. Use OAuth Playground to get refresh token
  
  GOOGLE_CLIENT_ID: 'your_client_id.apps.googleusercontent.com',
  GOOGLE_CLIENT_SECRET: 'GOCSPX-your_client_secret',
  GOOGLE_REFRESH_TOKEN: 'your_refresh_token_here',
  
  // Add your calendar IDs (find in calendar settings)
  CALENDAR_IDS: [
    'your_personal@gmail.com',
    'family_calendar@group.calendar.google.com',
    'work_calendar@gmail.com',
  ],

  // Customize colors for each calendar
  CALENDAR_COLORS: {
    'your_personal@gmail.com': { bg: '#6AC5FE', text: '#FFFFFF' },      // Blue
    'family_calendar@group.calendar.google.com': { bg: '#B660CD', text: '#FFFFFF' },  // Purple
    'work_calendar@gmail.com': { bg: '#F88379', text: '#FFFFFF' },       // Red
  },

  // ==========================================
  // WEATHER CONFIGURATION
  // ==========================================
  // Weatherbit.io: https://www.weatherbit.io/api (free: 50 calls/day)
  // OpenWeatherMap: https://openweathermap.org/api (free tier)
  
  WEATHERBIT_API_KEY: 'your_weatherbit_api_key',
  OPENWEATHER_API_KEY: 'your_openweather_api_key',
  
  // Your location (get from Google Maps)
  LATITUDE: '33.7701',
  LONGITUDE: '-118.1937',

  // ==========================================
  // SOLAR CONFIGURATION (OPTIONAL)
  // ==========================================
  // For APsystems ECU-R-PRO solar monitoring
  // Requires solar_server.py running on local network
  
  SOLAR_API_URL: 'http://localhost:8080/api/solar',
  SOLAR_ENABLED: false,  // Set to true to enable

  // ==========================================
  // DISPLAY SETTINGS
  // ==========================================
  PHOTO_INTERVAL: 30000,      // 30 seconds per photo
  WEATHER_REFRESH: 1800000,   // 30 minutes
  SOLAR_REFRESH: 60000,       // 1 minute
};

// ==========================================
// SOLAR SERVER CONFIGURATION (solar_server.py)
// ==========================================
/*
ECU_IP = "192.168.x.x"      # Your ECU's local IP
ECU_PORT = 8899             # Default APsystems port
ECU_ID = "your_ecu_id"      # Find on ECU web interface
SERVER_PORT = 8080          # Local API server port
*/
