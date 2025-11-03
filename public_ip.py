# !/usr/bin/env python3
# Script to fetch and display the public IP address and location information 

import requests

def get_public_ip_and_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        response.raise_for_status()
        data = response.json()

        ip = data.get("ip", "N/A")
        city = data.get("city", "N/A")
        region = data.get("region", "N/A")
        country = data.get("country", "N/A")
        loc = data.get("loc", "N/A")
        org = data.get("org", "N/A")

        print(f"Public IP: {ip}")
        print(f"Location: {city}, {region}, {country}")
        print(f"Coordinates: {loc}")
        print(f"Organization: {org}")

    except requests.RequestException as e:
        print(f"Error fetching IP info: {e}")

if __name__ == "__main__":
    get_public_ip_and_location()
