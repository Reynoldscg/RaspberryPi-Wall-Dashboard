#!/bin/bash
# ============================================
# Raspberry Pi Dashboard - Installation Script
# ============================================

set -e

echo "================================================"
echo "  Raspberry Pi Dashboard - Installation"
echo "================================================"
echo ""

# Check if running on Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/cpuinfo; then
    echo "⚠️  Warning: This doesn't appear to be a Raspberry Pi"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Update system
echo "📦 Updating system packages..."
sudo apt update

# Install dependencies
echo "📦 Installing dependencies..."
sudo apt install -y chromium-browser python3 python3-pip

# Check if desktop environment exists
if ! command -v startx &> /dev/null; then
    echo "⚠️  No desktop environment detected"
    echo "Installing minimal X server for kiosk mode..."
    sudo apt install -y xserver-xorg xinit
fi

# Set up dashboard directory
DASHBOARD_DIR="$HOME/raspberry-pi-dashboard"
cd "$DASHBOARD_DIR"

echo ""
echo "✅ Dependencies installed successfully!"
echo ""

# Check configuration
echo "📝 Checking configuration..."
if grep -q "your_app_key_here" dashboard.html; then
    echo ""
    echo "⚠️  WARNING: Dashboard is not configured!"
    echo ""
    echo "Please edit dashboard.html and add your API credentials:"
    echo "  nano $DASHBOARD_DIR/dashboard.html"
    echo ""
    echo "See config.example.js for guidance."
    echo ""
fi

# Solar setup (optional)
echo ""
read -p "Do you want to set up solar monitoring? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Setting up solar server..."
    
    # Check if solar_server.py is configured
    if grep -q "192.168.5.90" solar_server.py; then
        echo "⚠️  Please configure solar_server.py with your ECU IP address:"
        echo "  nano $DASHBOARD_DIR/solar_server.py"
        echo ""
    fi
    
    # Install solar server service
    read -p "Install solar server as system service? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo cp solar-server.service /etc/systemd/system/
        sudo systemctl daemon-reload
        sudo systemctl enable solar-server.service
        echo "✅ Solar server service installed"
        echo "Start with: sudo systemctl start solar-server.service"
    fi
fi

# Auto-start setup
echo ""
read -p "Do you want the dashboard to start automatically on boot? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    mkdir -p ~/.config/autostart
    cat > ~/.config/autostart/dashboard.desktop <<EOF
[Desktop Entry]
Type=Application
Name=Dashboard
Exec=chromium-browser --kiosk --noerrdialogs --disable-infobars --disable-session-crashed-bubble file://$DASHBOARD_DIR/dashboard.html
EOF
    echo "✅ Auto-start configured"
fi

# Screen power management
echo ""
read -p "Do you want to disable screen blanking? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Disable screen blanking
    if [ -f ~/.config/autostart/disable-screensaver.desktop ]; then
        rm ~/.config/autostart/disable-screensaver.desktop
    fi
    
    mkdir -p ~/.config/autostart
    cat > ~/.config/autostart/disable-screensaver.desktop <<EOF
[Desktop Entry]
Type=Application
Name=Disable Screensaver
Exec=bash -c "xset s off; xset -dpms; xset s noblank"
EOF
    echo "✅ Screen blanking disabled"
fi

echo ""
echo "================================================"
echo "  Installation Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "  1. Configure your API keys in dashboard.html"
echo "  2. Test: chromium-browser --kiosk file://$DASHBOARD_DIR/dashboard.html"
echo "  3. Reboot to start automatically"
echo ""
echo "For help, see: $DASHBOARD_DIR/README.md"
echo ""
