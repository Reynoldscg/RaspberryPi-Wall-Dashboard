#!/usr/bin/env python3
"""
Solar API Server for APsystems ECU-R-PRO
Queries the ECU via local network and serves solar production data
"""

import socket
import json
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Optional
import time

# ============================================
# CONFIGURATION
# ============================================
ECU_IP = "192.168.5.90"
ECU_PORT = 8899
ECU_ID = "216200094701"
SERVER_PORT = 8080

# ============================================
# ECU QUERY
# ============================================
# Cache to avoid hammering ECU
cached_data = None
cache_time = None
CACHE_TTL = 30  # seconds

def query_ecu() -> Optional[dict]:
    """Query ECU and return solar production data"""
    global cached_data, cache_time

    # Return cached data if fresh
    if cached_data and cache_time and (time.time() - cache_time) < CACHE_TTL:
        return cached_data

    info_cmd = b'APS1100160001END'

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((ECU_IP, ECU_PORT))
        sock.sendall(info_cmd)
        data = sock.recv(4096)
        sock.close()

        if not data or len(data) < 50:
            return cached_data  # Return stale cache on failure

        # Parse based on discovered offsets:
        # Offset 27-30 (4 bytes BE): Lifetime energy in 100 Wh units (0.1 kWh)
        # Offset 33-34 (2 bytes BE): Current power in W
        # Offset 37-38 (2 bytes BE): Today's energy in 10 Wh units (0.01 kWh)
        # Offset 46-47 (2 bytes BE): Inverter count

        lifetime_raw = int.from_bytes(data[27:31], 'big')
        lifetime_kwh = round(lifetime_raw / 10.0, 1)

        current_power = int.from_bytes(data[33:35], 'big')

        today_raw = int.from_bytes(data[37:39], 'big')
        today_kwh = round(today_raw / 100.0, 2)

        inverter_count = int.from_bytes(data[46:48], 'big')

        cached_data = {
            "current_power_w": current_power,
            "today_kwh": today_kwh,
            "lifetime_kwh": lifetime_kwh,
            "inverter_count": inverter_count,
            "timestamp": datetime.now().isoformat()
        }
        cache_time = time.time()

        return cached_data

    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ECU query error: {e}")
        return cached_data  # Return stale cache on failure


# ============================================
# HTTP SERVER
# ============================================
class SolarHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Enable CORS for dashboard access
        if self.path == '/api/solar' or self.path == '/solar':
            data = query_ecu()

            if data:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(data).encode())
            else:
                self.send_response(503)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "ECU unavailable"}).encode())

        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')

        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        # Suppress default logging, add our own
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")


def run_server():
    server = HTTPServer(('0.0.0.0', SERVER_PORT), SolarHandler)
    print(f"☀️  Solar API Server running on port {SERVER_PORT}")
    print(f"   ECU: {ECU_IP}:{ECU_PORT}")
    print(f"   Endpoint: http://localhost:{SERVER_PORT}/api/solar")
    print()
    server.serve_forever()


if __name__ == "__main__":
    run_server()
