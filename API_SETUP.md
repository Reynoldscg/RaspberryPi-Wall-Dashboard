# API Setup Guide

Complete step-by-step instructions for obtaining all required API credentials.

## Table of Contents
1. [Dropbox](#dropbox-setup)
2. [Google Calendar](#google-calendar-setup)
3. [Weatherbit.io](#weatherbit-setup)
4. [OpenWeatherMap](#openweathermap-setup)
5. [Solar (Optional)](#solar-setup-optional)

---

## Dropbox Setup

### Step 1: Create a Dropbox App

1. Go to [Dropbox App Console](https://www.dropbox.com/developers/apps)
2. Click **"Create app"**
3. Choose:
   - **API:** Scoped access
   - **Access:** Full Dropbox (or App folder if you prefer)
   - **Name:** "Family Dashboard" (or any name)
4. Click **"Create app"**

### Step 2: Configure Permissions

1. Go to the **Permissions** tab
2. Enable these permissions:
   - ✅ `files.metadata.read`
   - ✅ `files.content.read`
3. Click **"Submit"**

### Step 3: Get Your Credentials

1. Go to the **Settings** tab
2. Note your:
   - **App key** (e.g., `gwheha0z7klzsp0`)
   - **App secret** (e.g., `9tqyvghu77vnlfs`)

### Step 4: Generate Refresh Token

**Option A: Using curl (Recommended)**

```bash
# Replace with your App Key and App Secret
APP_KEY="your_app_key"
APP_SECRET="your_app_secret"

# Step 1: Get authorization code
# Open this URL in your browser:
echo "https://www.dropbox.com/oauth2/authorize?client_id=$APP_KEY&token_access_type=offline&response_type=code"

# Step 2: After authorizing, you'll get a code. Use it here:
AUTH_CODE="paste_your_auth_code_here"

# Step 3: Exchange for refresh token
curl https://api.dropbox.com/oauth2/token \
  -d code=$AUTH_CODE \
  -d grant_type=authorization_code \
  -u $APP_KEY:$APP_SECRET

# Copy the "refresh_token" from the response
```

**Option B: Using Dropbox OAuth Playground**
1. Go to [OAuth Guide](https://www.dropbox.com/developers/documentation/http/documentation#authorization)
2. Follow the OAuth 2.0 flow to get a refresh token

### Step 5: Upload Photos

1. Create folder structure in Dropbox: `/Photos/Dashboard Photos/`
2. Upload your family photos to this folder
3. Supported formats: JPG, PNG, GIF, HEIC, WebP

---

## Google Calendar Setup

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"Create Project"**
3. Name it "Family Dashboard" and click **"Create"**

### Step 2: Enable Calendar API

1. In the project, go to **"APIs & Services" → "Library"**
2. Search for **"Google Calendar API"**
3. Click on it and press **"Enable"**

### Step 3: Create OAuth Credentials

1. Go to **"APIs & Services" → "Credentials"**
2. Click **"Create Credentials" → "OAuth client ID"**
3. If prompted, configure OAuth consent screen:
   - User Type: **External**
   - App name: **"Family Dashboard"**
   - Add your email as a test user
4. Create OAuth client ID:
   - Application type: **Desktop app**
   - Name: "Dashboard Client"
5. Click **"Create"**
6. Save your:
   - **Client ID** (ends in `.apps.googleusercontent.com`)
   - **Client Secret** (starts with `GOCSPX-`)

### Step 4: Get Refresh Token

**Using Google OAuth Playground:**

1. Go to [OAuth 2.0 Playground](https://developers.google.com/oauthplayground/)
2. Click the gear icon (⚙️) in top right
3. Check **"Use your own OAuth credentials"**
4. Enter your **Client ID** and **Client Secret**
5. In "Step 1", select **"Calendar API v3"**
6. Select `https://www.googleapis.com/auth/calendar.readonly`
7. Click **"Authorize APIs"**
8. Sign in and grant permissions
9. Click **"Exchange authorization code for tokens"**
10. Copy the **refresh_token** (starts with `1//`)

### Step 5: Find Calendar IDs

1. Go to [Google Calendar](https://calendar.google.com/)
2. Click on calendar name → **"Settings and sharing"**
3. Scroll to **"Integrate calendar"**
4. Copy the **Calendar ID** (usually your email or a long ID)
5. Repeat for each calendar you want to display

---

## Weatherbit Setup

### Step 1: Sign Up

1. Go to [Weatherbit.io](https://www.weatherbit.io/api)
2. Click **"Sign Up"** (free tier available)
3. Confirm your email

### Step 2: Get API Key

1. Log in to your [Account Dashboard](https://www.weatherbit.io/account)
2. Your API key is displayed on the dashboard
3. Copy it (e.g., `b34906e086d840e3827ab0ab0e90a4b3`)

### Step 3: Get Your Coordinates

1. Go to [Google Maps](https://www.google.com/maps)
2. Right-click your location → Click on coordinates to copy
3. Format: First number is **Latitude**, second is **Longitude**
   - Example: `33.7701, -118.1937`

**Free Tier Limits:**
- 50 API calls per day
- 1 call per second

---

## OpenWeatherMap Setup

### Step 1: Sign Up

1. Go to [OpenWeatherMap](https://openweathermap.org/)
2. Click **"Sign Up"** (free tier available)
3. Confirm your email

### Step 2: Get API Key

1. Log in to your account
2. Go to [API Keys](https://home.openweathermap.org/api_keys)
3. Your default API key is already created
4. Copy it (e.g., `1234...`)

**Note:** New API keys take about 10-15 minutes to activate.

**Free Tier Limits:**
- 1,000 API calls per day
- 60 calls per minute

---

## Solar Setup (Optional)

For APsystems ECU-R-PRO solar inverter monitoring.

### Step 1: Find Your ECU Information

1. Find your ECU's IP address on your router (look for "ECU" device)
2. Open web browser and go to `http://[ECU-IP]`
3. Login to ECU web interface
4. Note:
   - **ECU ID** (12 characters, e.g., `216200094701`)
   - **Local IP** (e.g., `192.168.5.90`)

### Step 2: Configure Solar Server

Edit `solar_server.py`:

```python
ECU_IP = "192.168.5.90"      # Your ECU's IP
ECU_PORT = 8899              # Default port
ECU_ID = "216200094701"      # Your ECU ID
SERVER_PORT = 8080           # Local API server port
```

### Step 3: Test Connection

```bash
python3 solar_server.py
```

Expected output:
```
☀️  Solar API Server running on port 8080
   ECU: 192.168.5.90:8899
   Endpoint: http://localhost:8080/api/solar
```

Test the API:
```bash
curl http://localhost:8080/api/solar
```

Expected response:
```json
{
  "current_power_w": 2554,
  "today_kwh": 19.77,
  "lifetime_kwh": 34611.5,
  "inverter_count": 12,
  "timestamp": "2024-12-06T14:25:00.000000"
}
```

### Step 4: Enable in Dashboard

Edit `dashboard.html`:

```javascript
SOLAR_API_URL: 'http://localhost:8080/api/solar',
SOLAR_ENABLED: true,  // Change to true
```

---

## Testing Your Configuration

### Quick Test Script

Create a file `test_config.html` and open it in a browser:

```html
<!DOCTYPE html>
<html>
<head><title>API Test</title></head>
<body>
  <h1>API Configuration Test</h1>
  <div id="results"></div>
  <script>
    // Paste your CONFIG here and test each API
    async function testAPIs() {
      const results = [];
      
      // Test Weatherbit
      try {
        await fetch(`https://api.weatherbit.io/v2.0/current?lat=33.7701&lon=-118.1937&key=YOUR_KEY`);
        results.push('✅ Weatherbit: OK');
      } catch (e) {
        results.push('❌ Weatherbit: ' + e.message);
      }
      
      document.getElementById('results').innerHTML = results.join('<br>');
    }
    testAPIs();
  </script>
</body>
</html>
```

---

## Troubleshooting

### Dropbox
- **Error: Invalid refresh token** → Regenerate token with correct scopes
- **No photos showing** → Check folder path and file extensions

### Google Calendar
- **Error: Invalid credentials** → Verify Client ID and Secret
- **No events showing** → Check Calendar IDs and permissions

### Weather APIs
- **Error: 401 Unauthorized** → Check API keys
- **Error: 429 Too Many Requests** → You've exceeded rate limits

### Solar
- **Error: Connection refused** → Check ECU IP and that it's on same network
- **Error: Timeout** → Verify ECU port (8899) is accessible
- **No data** → Check ECU ID is correct

---

## Security Reminders

⚠️ **NEVER commit API keys to public repositories!**

- Keep `dashboard.html` private if it contains real credentials
- Use environment variables for production
- Rotate keys if accidentally exposed
- Use read-only permissions where possible

---

**Need help?** Open an issue on GitHub with details (but never include actual API keys!)
