from customtkinter import *
import requests
import geocoder

API_KEY = "46f39b60cd5f7dc35fd549b7d4ec833f"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
def get_weather(city):
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url=url)
    return response.json()

def get_lacation():
    location = geocoder.ip("me")
    return location.city if location and location.city else "unknown"


def show_weather():
    city = entry.get()
    if not city:
        city = get_lacation()

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


set_appearance_mode("dark")
set_default_color_theme("blue")
window = CTk()
window.title("Weather Forcast")
window.geometry("400x400")

label = CTkLabel(window,text="weather foeecast",font=("Helvetica",22))
label.pack()

entry = CTkEntry(window,placeholder_text="Enter city",font=("Helvetica",14),width=280)
entry.pack()

btn = CTkButton(window,text="Get Weather",font=("Helvetica",14),command=show_weather)
btn.pack()

result_label = CTkLabel(window,text="",font=("Helvetica",14))
result_label.pack()

window.mainloop()