import tkinter as tk
import requests
import pymongo
import datetime

# Set up MongoDB client and database
client = pymongo.MongoClient("mongodb+srv://srikanthcgl:Nani1234@srikanthcluster.p2gipht.mongodb.net/test")
db = client["Weather_Data"]
collection = db["locations"]

# OpenWeatherMap API endpoint URL
OWM_URL = "https://api.openweathermap.org/"

class WeatherApp:
    def __init__(self, master):
        self.master = master
        master.title("Weather App")

        # Create label and entry for location names
        self.locations_label = tk.Label(master, text="Enter up to 5 location names (separated by commas):")
        self.locations_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.locations_entry = tk.Entry(master)
        self.locations_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Create button to fetch weather data
        self.fetch_button = tk.Button(master, text="Fetch weather data", command=self.fetch_weather_data)
        self.fetch_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Create label to display status
        self.status_label = tk.Label(master, text="")
        self.status_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    # Function to fetch weather data for multiple locations
    def fetch_weather_data(self):
        # Clear status label
        self.status_label.config(text="")

        # Get API key and location names from entries
        api_key = "e182533dd91357d387142a1675b24a1c"
        location_names = self.locations_entry.get().split(",")

        # Validate inputs
        if not api_key:
            self.status_label.config(text="Please enter an API key")
            return
        if not location_names:
            self.status_label.config(text="Please enter at least one location name")
            return
        if len(location_names) > 5:
            self.status_label.config(text="Please enter no more than 5 location names")
            return

        # Loop through each location and fetch weather data
        for location_name in location_names:
            # Make API request for current weather data
            params = {
                "q": location_name.strip(),
                "appid": api_key,
                "units": "metric",
            }
            response = requests.get(OWM_URL + "data/2.5/weather", params=params)
            data = response.json()

            # get current time
            now = datetime.datetime.now()

            # Extract relevant weather data
            if response.status_code == 200:
                temperature = data["main"]["temp"]
                clouds = data["clouds"]["all"]
                description = data["weather"][0]["description"]
                weather_main = data["weather"][0]["main"]
                condition = ""
                time = now.strftime("%Y-%m-%d %H:%M:%S")

                # Determine weather condition based on temperature
                if temperature >= 30:
                    condition = "sunny"
                elif temperature >= 10 and temperature < 28:
                    condition = "cloudy"
                else:
                    condition = "rainy"

                # Insert data into MongoDB
                weather_data = {
                    "location_name": location_name.strip(),
                    "latitude": data["coord"]["lat"],
                    "longitude": data["coord"]["lon"],
                    "temperature": temperature,
                    "clouds": clouds,
                    "description": description,
                    "weather_main": weather_main,
                    "condition":condition,
                    "time":time,
                }
                collection.insert_one(weather_data)

                # Update status label
                self.status_label.config(text="Weather data fetched and uploaded to MongoDB")

#Create and run the GUI
root = tk.Tk()
app = WeatherApp(root)
root.mainloop()

