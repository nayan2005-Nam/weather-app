import requests
import customtkinter as ctk
import geocoder

API_KEY = "46f39b60cd5f7dc35fd549b7d4ec833f"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()

def get_location():
    location = geocoder.ip("me")
    return location.city if location and location.city else "Unknown"

def show_weather():
    city = entry.get()
    if not city:
        city = get_location()

    try:
        data = get_weather(city)
        if data["cod"] != 200:
            result_label.configure(text="Invalid City, try again!", text_color="red")
            return

        temp_c = data["main"]["temp"]
        temp_f = (temp_c * 9/5) + 32
        humidity = data["main"]["humidity"]
        condition = data["weather"][0]["description"].capitalize()

        if "clear" in condition.lower():
            icon = "☀️"
        elif "cloud" in condition.lower():
            icon = "☁️"
        elif "rain" in condition.lower():
            icon = "🌧️"
        else:
            icon = "🌡️"

        result_label.configure(
            text=f"{city} Weather:\n{condition} {icon}\nTemp: {temp_c}°C | {temp_f}°F\nHumidity: {humidity}%",
            text_color="white"
        )
    except Exception as e:
        result_label.configure(text=f"Error: {str(e)}", text_color="red")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("450x350")
app.title("CustomTkinter Weather App")

title = ctk.CTkLabel(app, text="🌍 Weather Forecast", font=("Helvetica", 22, "bold"))
title.pack(pady=15)

entry = ctk.CTkEntry(app, placeholder_text="Enter city name", width=280, font=("Helvetica", 14))
entry.pack(pady=10)

get_btn = ctk.CTkButton(app, text="Get Weather", command=show_weather, font=("Helvetica", 14))
get_btn.pack(pady=5)

result_label = ctk.CTkLabel(app, text="", font=("Helvetica", 15))
result_label.pack(pady=20)

app.mainloop()


