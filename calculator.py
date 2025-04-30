def calculate_transmission(medium, signal_type, wave_type, distance_km):
    distance = float(distance_km)
    result = ""

    if medium in ["Ethernet", "Twisted Pair Cable"]:
        max_seg = 2
        repeaters = max(1, int(distance // max_seg) + 1)
        spacing = distance / repeaters
        attenuation = 0.2 if signal_type == "DC" else 0.7
        result += f"{medium} ({signal_type}):\n"

    elif medium == "Optical Fiber":
        max_seg = 40
        repeaters = max(1, int(distance // max_seg) + 1)
        spacing = distance / repeaters
        attenuation = 0.35
        result += f"{medium}:\n"

    elif medium == "Wi-Fi (HOME)":
        max_seg = 0.1 if wave_type == "Radio Wave" else 0.05
        repeaters = max(1, int(distance // max_seg) + 1)
        spacing = distance / repeaters
        attenuation = 10 if wave_type == "Radio Wave" else 20
        result += f"{medium} ({wave_type}):\n"

    elif medium == "Wi-Fi (INDUSTRIAL)":
        max_seg = 2  # Now, repeater needed after every 2 km
        repeaters = max(1, int(distance // max_seg))
        spacing = distance / (repeaters + 1)
        attenuation = 10 if wave_type == "Radio Wave" else 20
        result += f"{medium} ({wave_type}):\n"

    else:
        return "⚠️ Error: Unknown transmission medium selected. Please choose a valid one."

    result += f"- Total Distance: {distance:.2f} km\n"
    result += f"- Repeaters/Routers Needed: {repeaters - 1}\n"
    result += f"- Distance between Routers: {spacing:.2f} km\n"
    result += f"- Attenuation Rate: {attenuation:.2f} dB/km\n"
    return result