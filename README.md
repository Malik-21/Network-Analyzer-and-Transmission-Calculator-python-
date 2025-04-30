
# Network Analyzer & Transmission Calculator

## Introduction
The **Network Analyzer & Transmission Calculator** is a Python-based desktop application developed using Tkinter that provides two core functionalities:

1. **Wi-Fi Network Scanning & Analysis** – Detects available Wi-Fi networks, gathers network details (SSID, BSSID, Signal Strength, Frequency, IP), and visualizes signal strength and estimated internet speed.
2. **Transmission Loss Calculator** – Calculates attenuation, repeater/router requirement, and spacing based on different mediums (Ethernet, Optical Fiber, Twisted Pair Cable, Wi-Fi HOME & INDUSTRIAL).

---

## Features

### Functional Requirements
- Detect active Wi-Fi or Ethernet connection.
- Scan nearby Wi-Fi networks.
- Display SSID, BSSID, Signal Strength, Frequency, and IP.
- Graphical representation of signal strength and estimated speed.
- Input-based calculation for transmission loss, spacing, attenuation rate.

### Non-Functional Requirements
- Easy-to-use GUI interface.
- Cross-platform compatibility (Windows, Linux, macOS).
- Real-time scan with responsive design.

---

## Technologies Used
- **Programming Language**: Python
- **GUI Framework**: Tkinter
- **Network Library**: `pywifi`
- **Graphing/Plotting**: `matplotlib`
- **System/Network Access**: `socket`, `subprocess`, `platform`

---

## Required Libraries & Installation
To run the project, you need to install the following dependencies:

### Install All at Once
```bash
pip install pywifi matplotlib
```

### Or Install Separately
```bash
pip install pywifi        # For scanning and accessing Wi-Fi networks
pip install matplotlib    # For plotting signal graphs
```

These are the Python standard libraries used (no need to install separately):
- `tkinter` – GUI toolkit
- `socket` – Network interface access
- `subprocess` – Running system commands
- `platform` – OS detection
- `math` – Mathematical calculations
- `time` – Timing utilities
- `ttk` – Themed widgets (part of tkinter)
- `messagebox` – Popup dialogs (part of tkinter)

---

## Project Structure
```
network-analyzer-transmission-calculator/
├── main.py                   # Main GUI logic using tkinter
├── scanner.py                # Wi-Fi detection, scanning, info fetcher
├── calculator.py             # Transmission loss calculator logic
├── README.md                 # Project description
```

---

## How to Install & Run

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd network-analyzer-transmission-calculator
```

### Step 2: Install Dependencies
```bash
pip install pywifi matplotlib
```

### Step 3: Run the App
```bash
python main.py
```

---

## Creating an Executable (.exe) File

If you want to distribute the application as an `.exe` file for Windows users, you can create an executable using **PyInstaller**. Here's how:

1. **Install PyInstaller**
   First, install PyInstaller by running:
   ```bash
   pip install pyinstaller
   ```

2. **Generate the .exe File**
   In your project directory, run the following command:
   ```bash
   pyinstaller --onefile --windowed main.py
   ```

   - `--onefile` ensures everything is packaged into a single executable.
   - `--windowed` ensures the application runs without opening a terminal window (ideal for GUI applications).
   - After running this command, an `.exe` file will be created in the `dist` folder.

3. **Distribute the Executable**
   The `.exe` file will be in the `dist` folder, which you can now distribute to users who do not have Python installed.

---

# 🎯 Use Case
- Useful for engineers, students, and technicians to analyze Wi-Fi coverage.
- Helps calculate transmission loss for wired and wireless mediums.
- Can be extended to a full network management toolkit.

---

# 📃 Author & Credits
- Developed by: [Ayna Khan, Malik Muhammad Yahya, Muhammad Hamza]
- Date: April 2025
- Special Thanks: Open-source libraries and the Python community

---

# 🛠️ Future Improvements
- Add support for 5GHz vs 2.4GHz differentiation.
- Export results to CSV or PDF.
- Add real-time speed test integration.
- Dark mode and themes.

---

# 📝 License


