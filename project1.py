import tkinter as tk  # GUI library
from tkinter import messagebox  # For showing pop-up messages
from geopy.geocoders import Nominatim  # For getting city coordinates
from timezonefinder import TimezoneFinder  # For finding the city's timezone
from datetime import datetime  # For handling time
import requests  # For making API requests
import pytz  # For timezone management
import os  # For environment variable handling

# Create the main application window
root = tk.Tk()
root.title("Weather App")  # Set window title
root.geometry("900x500+300+200")  # Set window size
root.resizable(False, False)  # Prevent resizing

# API Key (Use environment variable for security)
API_KEY = "9eb5d61c4f7fdef5aa5cadc89a8971bc"  # Replace with your API key
if not API_KEY:
    messagebox.showerror("Error", "API key not found. Please set the OPENWEATHER_API_KEY environment variable.")
    exit()  # Stop execution if API key is missing

# Function to fetch weather data
def get_weather():
    city = textfield.get()  # Get user input from text field
    geolocator = Nominatim(user_agent="myweatherapp")  # Initialize geolocator

    try:
        # Get the city's geographical location (latitude & longitude)
        location = geolocator.geocode(city)
        if location is None:
            messagebox.showerror("Error", "City not found!")
            return

        # Find the timezone for the location
        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
        home = pytz.timezone(result)  # Convert to timezone format
        local_time = datetime.now(home)  # Get current time in that timezone
        current_time = local_time.strftime("%I:%M %p")  # Format time
        clock_label.config(text=current_time)  # Update time on UI
        current_weather_label.config(text="CURRENT WEATHER")  # Update weather title

        # API request to fetch weather details
        api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(api)  # Send request to API
        response.raise_for_status()  # Check for request errors
        json_data = response.json()  # Convert response to JSON format

        # Ensure the response contains expected data
        if "weather" not in json_data or "main" not in json_data:
            messagebox.showerror("Error", "Invalid response from weather API")
            return

        # Extract required weather data
        condition = json_data['weather'][0]['main']  # Main weather condition (e.g., Cloudy)
        description = json_data['weather'][0]['description']  # Detailed weather description
        temp = int(json_data['main']['temp'])  # Temperature in Celsius
        pressure = json_data['main']['pressure']  # Atmospheric pressure in hPa
        humidity = json_data['main']['humidity']  # Humidity percentage
        wind = json_data['wind']['speed']  # Wind speed in m/s

        # Update the UI with the weather data
        temperature_label.config(text=f"{temp}°C")
        condition_label.config(text=f"{condition} | FEELS LIKE {temp}°C")
        wind_label.config(text=f"{wind} m/s")
        humidity_label.config(text=f"{humidity}%")
        description_label.config(text=description.capitalize())
        pressure_label.config(text=f"{pressure} hPa")

    # Handle network errors (e.g., no internet, bad response)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Network error: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# UI Setup - Search Box
Search_image = tk.PhotoImage(file="search.png")  # Load search box image
myimage = tk.Label(image=Search_image)  # Display search box
myimage.place(x=20, y=20)

# Input field for city name
textfield = tk.Entry(root, justify="center", width=17, font=("poppins", 25, "bold"), bg="#404040", border=0, fg="white")
textfield.place(x=50, y=40)
textfield.focus()  # Auto-focus on input field

# Search button
Search_icon = tk.PhotoImage(file="search_icon.png")  # Load search icon image
myimage_icon = tk.Button(image=Search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=get_weather)
myimage_icon.place(x=400, y=34)  # Position search button

# Logo
Logo_image = tk.PhotoImage(file="logo.png")  # Load logo image
Logo = tk.Label(image=Logo_image)  # Display logo
Logo.place(x=150, y=100)

# Bottom box frame
Frame_image = tk.PhotoImage(file="box.png")  # Load bottom frame image
frame_myimage = tk.Label(image=Frame_image)
frame_myimage.pack(padx=5, pady=5, side=tk.BOTTOM)  # Position frame

# Labels for current time and weather status
current_weather_label = tk.Label(root, font=("arial", 15, "bold"))
current_weather_label.place(x=30, y=100)
clock_label = tk.Label(root, font=("Helvetica", 20))
clock_label.place(x=30, y=130)

# Function to create bottom weather info labels
def create_bottom_label(text, x):
    label = tk.Label(root, text=text, font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
    label.place(x=x, y=400)  # Set position
    data_label = tk.Label(root, text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
    data_label.place(x=x, y=430)  # Set position
    return data_label

# Create weather data labels (Wind, Humidity, Description, Pressure)
wind_label = create_bottom_label("WIND", 120)
humidity_label = create_bottom_label("HUMIDITY", 250)
description_label = create_bottom_label("DESCRIPTION", 430)
pressure_label = create_bottom_label("PRESSURE", 650)

# Label for temperature and condition
temperature_label = tk.Label(font=("arial", 70, "bold"), fg="#ee666d")
temperature_label.place(x=400, y=150)
condition_label = tk.Label(font=("arial", 15, "bold"))
condition_label.place(x=400, y=250)

# Run the application
root.mainloop()
