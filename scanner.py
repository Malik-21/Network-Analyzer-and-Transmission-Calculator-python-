import pywifi
from pywifi import const
import socket
import subprocess
import platform

def scan_wifi():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    iface.scan()
    import time
    time.sleep(3)  # Allow some time for scanning

    results = iface.scan_results()

    networks = []
    for network in results:
        networks.append({
            'SSID': network.ssid,
            'BSSID': network.bssid,
            'Signal': network.signal,
            'Frequency': network.freq
        })

    return networks

def is_wifi_connected():
    try:
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]
        return iface.status() == const.IFACE_CONNECTED
    except Exception:
        return False

def get_connected_network():
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return ip
    except Exception:
        return "Unknown"

def get_current_network_info():
    try:
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]
        if iface.status() != const.IFACE_CONNECTED:
            return None

        # Attempt to get BSSID and SSID from known profiles
        connected_profile = None
        for profile in iface.network_profiles():
            if profile.ssid:
                connected_profile = profile
                break

        ssid = connected_profile.ssid if connected_profile else "Unknown"
        bssid = connected_profile.bssid if connected_profile and connected_profile.bssid else "Unknown"
        freq = "Unknown"

        # Try to get frequency via OS-specific commands
        system = platform.system()
        if system == "Windows":
            try:
                output = subprocess.check_output("netsh wlan show interfaces", shell=True).decode()
                for line in output.splitlines():
                    if "Channel" in line:
                        channel = int(line.split(":")[1].strip())
                        freq = 2407 + channel * 5  # Approximate formula
                        break
            except:
                pass
        elif system == "Linux":
            try:
                output = subprocess.check_output(["iwgetid", "-f"]).decode().strip()
                freq = output if output else "Unknown"
            except:
                pass
        elif system == "Darwin":  # macOS
            try:
                output = subprocess.check_output(
                    ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"]
                ).decode()
                for line in output.splitlines():
                    if "agrCtlRSSI" in line:
                        break
                    if "channel" in line.lower():
                        freq = line.split(":")[1].strip()
                        break
            except:
                pass

        return {
            'SSID': ssid,
            'BSSID': bssid,
            'Frequency': freq,
            'IP': get_connected_network()
        }
    except Exception as e:
        print("Error getting current network info:", e)
        return None