import tkinter as tk
from tkinter import ttk, messagebox
from scanner import scan_wifi, get_connected_network, is_wifi_connected, get_current_network_info
from calculator import calculate_transmission
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Network Analyzer & Transmission Calculator")
        self.geometry("800x650")
        self.configure(bg="#0c0f3a")

        tabControl = ttk.Notebook(self)
        self.wifi_tab = ttk.Frame(tabControl)
        self.calc_tab = ttk.Frame(tabControl)

        tabControl.add(self.wifi_tab, text='Network Detection & Analysis')
        tabControl.add(self.calc_tab, text='Transmission Calculator')
        tabControl.pack(expand=1, fill="both")

        self.selected_network = None
        self.build_wifi_tab()
        self.build_calc_tab()

    def build_wifi_tab(self):
        detect_frame = ttk.Frame(self.wifi_tab)
        detect_frame.pack(pady=10, fill='x', padx=10)

        detect_btn = ttk.Button(detect_frame, text="🔍 Detect Network", command=self.detect_network)
        detect_btn.pack()

        self.detect_result = tk.Text(self.wifi_tab, height=10, bg="#11154e", fg="white")
        self.detect_result.pack(fill='x', padx=10, pady=5)

        self.scan_btn = ttk.Button(self.wifi_tab, text="📡 Scan Available Wi-Fi Networks", command=self.load_networks)
        self.scan_btn.pack(pady=5)
        self.scan_btn["state"] = "disabled"

        self.wifi_tree = ttk.Treeview(self.wifi_tab, columns=("ID", "SSID", "BSSID", "Signal", "Frequency"), show='headings')
        for col in ("ID", "SSID", "BSSID", "Signal", "Frequency"):
            self.wifi_tree.heading(col, text=col)
            self.wifi_tree.column(col, width=150)
        self.wifi_tree.pack(fill='both', expand=True, pady=10)
        self.wifi_tree.bind("<ButtonRelease-1>", self.on_select_network)

    def detect_network(self):
        self.detect_result.delete(1.0, tk.END)

        if is_wifi_connected():
            info = get_current_network_info()
            if info:
                self.detect_result.insert(tk.END, "📶 Connected via Wi-Fi\n")
                self.detect_result.insert(tk.END, f"- SSID: {info['SSID']}\n")
                self.detect_result.insert(tk.END, f"- BSSID: {info['BSSID']}\n")
                self.detect_result.insert(tk.END, f"- Frequency: {info['Frequency']} MHz\n")
                self.detect_result.insert(tk.END, f"- IP: {info['IP']}\n")
                speed = self.calculate_speed(-50)  # Approximation
                self.detect_result.insert(tk.END, f"- Estimated Speed: {speed} Mbps\n")
                self.scan_btn["state"] = "normal"
            else:
                self.detect_result.insert(tk.END, "⚠️ Wi-Fi connected but unable to get network info.\n")
                self.scan_btn["state"] = "disabled"
        else:
            ip = get_connected_network()
            self.detect_result.insert(tk.END, "🧷 Connected via Ethernet\n")
            self.detect_result.insert(tk.END, f"- IP Address: {ip}\n")
            self.scan_btn["state"] = "disabled"

    def load_networks(self):
        self.wifi_tree.delete(*self.wifi_tree.get_children())
        networks = scan_wifi()
        seen = set()
        for idx, net in enumerate(networks, 1):
            if net['BSSID'] not in seen:
                seen.add(net['BSSID'])
                self.wifi_tree.insert('', 'end', values=(idx, net['SSID'], net['BSSID'], net['Signal'], net['Frequency']))

    def on_select_network(self, event):
        item = self.wifi_tree.selection()
        if item:
            self.selected_network = self.wifi_tree.item(item, 'values')
            self.open_network_details()

    def open_network_details(self):
        if self.selected_network:
            serial_id, ssid, bssid, signal, freq = self.selected_network
            new_window = tk.Toplevel(self)
            new_window.title(f"Details of {ssid}")
            new_window.geometry("600x500")

            title_lbl = tk.Label(new_window, text=f"Network: {ssid}", font=("Arial", 16, "bold"), fg="blue")
            title_lbl.pack(pady=10)

            details = f"Network Serial ID: {serial_id}\n"
            details += f"SSID: {ssid}\n"
            details += f"BSSID: {bssid}\n"
            details += f"Signal Strength: {signal} dBm\n"
            details += f"Frequency: {freq} MHz\n"
            details += f"IP Address: {get_connected_network()}\n"

            details_lbl = tk.Label(new_window, text=details, font=("Arial", 12))
            details_lbl.pack(padx=20, pady=20)

            self.add_signal_chart(new_window, int(signal))
            self.add_speed_circle(new_window, int(signal))

            close_btn = ttk.Button(new_window, text="Close", command=new_window.destroy)
            close_btn.pack(pady=10)

    def add_signal_chart(self, window, signal):
        fig, ax = plt.subplots(figsize=(4, 1))
        ax.barh([0], [signal], color='green' if signal > -60 else 'red')
        ax.set_xlim(-100, 0)
        ax.set_yticks([])
        ax.set_title("Signal Strength")

        canvas = FigureCanvasTkAgg(fig, window)
        canvas.get_tk_widget().pack(padx=20, pady=10)
        canvas.draw()

    def add_speed_circle(self, window, signal):
        canvas = tk.Canvas(window, width=200, height=200, bg='white')
        canvas.pack(pady=10)

        radius = max(50, 100 - (abs(signal) + 40))
        center = 100

        canvas.create_oval(center - radius, center - radius, center + radius, center + radius, outline="blue", width=2)
        speed = self.calculate_speed(signal)
        canvas.create_text(center, center, text=f"Speed: {speed} Mbps", font=("Arial", 10))

    def calculate_speed(self, signal):
        if signal > -50:
            return 100
        elif signal > -60:
            return 50
        elif signal > -70:
            return 20
        else:
            return 5

    def build_calc_tab(self):
        frame = ttk.Frame(self.calc_tab)
        frame.pack(padx=10, pady=10, fill='x')

        ttk.Label(frame, text="Transmission Medium:").grid(row=0, column=0, sticky='w')
        self.medium = ttk.Combobox(frame, values=["Ethernet", "Optical Fiber", "Wi-Fi (HOME)", "Twisted Pair Cable", "Wi-Fi (INDUSTRIAL)"])
        self.medium.grid(row=0, column=1, sticky='ew')

        ttk.Label(frame, text="Signal Type (DC/AC) (Not For Wi-Fi):").grid(row=1, column=0, sticky='w')
        self.signal_type = ttk.Entry(frame)
        self.signal_type.grid(row=1, column=1, sticky='ew')

        ttk.Label(frame, text="Wave Type (Radio/Micro) (Only For Wi-Fi):").grid(row=2, column=0, sticky='w')
        self.wave_type = ttk.Entry(frame)
        self.wave_type.grid(row=2, column=1, sticky='ew')

        ttk.Label(frame, text="Distance (km):").grid(row=3, column=0, sticky='w')
        self.distance = ttk.Entry(frame)
        self.distance.grid(row=3, column=1, sticky='ew')

        frame.columnconfigure(1, weight=1)

        calc_btn = ttk.Button(frame, text="Calculate", command=self.perform_calc)
        calc_btn.grid(row=4, column=0, columnspan=2, pady=10)

        self.result_text = tk.Text(self.calc_tab, height=15, bg="#11154e", fg="white")
        self.result_text.pack(fill='both', padx=10, pady=5)

    def perform_calc(self):
        medium = self.medium.get()
        sig_type = self.signal_type.get()
        wave = self.wave_type.get()
        dist = self.distance.get()

        try:
            result = calculate_transmission(medium, sig_type, wave, dist)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == '__main__':
    app = App()
    app.mainloop()