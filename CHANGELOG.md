# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2024-12-18

### Added
- Initial release of Raspberry Pi Family Dashboard
- Real-time clock display (12-hour format)
- Weather widget with current conditions and AQI
- Multi-calendar Google Calendar integration
- Dropbox photo slideshow with smooth transitions
- Optional APsystems ECU-R-PRO solar monitoring
- Kiosk mode for full-screen display
- Auto-start on boot configuration
- Installation script for easy setup
- Comprehensive API setup documentation

### Features
- **Clock**: Automatic 12-hour time display
- **Weather**: 
  - Weatherbit.io integration for current weather
  - OpenWeatherMap for Air Quality Index
  - Dynamic sunrise/sunset display
  - Wind speed and temperature
- **Calendar**: 
  - Multiple calendar support
  - Color-coded events
  - Month view with event details
  - Today highlight
- **Photos**: 
  - Dropbox integration with refresh tokens
  - Automatic photo rotation
  - Smooth fade transitions
  - Supports JPG, PNG, GIF, HEIC, WebP
- **Solar** (Optional):
  - Real-time power production
  - Today's energy generation
  - Lifetime energy stats
  - Inverter status monitoring

### Technical
- Single-file HTML dashboard (no build process)
- Python 3 solar API server
- Systemd service integration
- CORS-enabled API endpoints
- Responsive viewport sizing
- Automatic token refresh for all APIs

### Documentation
- Comprehensive README.md
- Detailed API_SETUP.md guide
- Configuration examples
- Installation script
- Troubleshooting guide

## Future Enhancements

Potential features for future releases:
- [ ] Dark mode / theme customization
- [ ] Multiple photo folders/albums
- [ ] News feed integration
- [ ] Spotify now playing
- [ ] Smart home device integration
- [ ] Custom widgets framework
- [ ] Mobile-responsive layout
- [ ] Voice control integration
- [ ] Multi-monitor support
- [ ] Dashboard statistics/analytics
