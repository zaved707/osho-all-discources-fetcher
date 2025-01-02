import os
import requests

# List of audio series with their ranges (start and end)
audio_series = {
    #"Adhyatam Upanishad": (4, 17),
    #"Ami Jharat Bigsat Kanwal": (1, 14),
    #"Ajhun Chet Ganwar": (5, 14),
    #"Ari Main To Namke": (1, 2),
    #"Athato Bhakti Jigyasa": (3, 3),
    # "Anhad_Main_Bisram": (1, 10),
    "Apui_Gai_Herai": (3, 10),
    #"Apne_Mahin_Tatol": (1, 8),
    "Asambhav Kranti": (5, 10),
    "Agyat Ki Aur": (1, 7),
    "Amrit Dwar": (1, 6),
    "Amrit Ki Disha": (1, 8),
    "Amrit Varsha": (1, 5),
    "Anant Ki Pukar": (1, 12),
    "Antar Ki Khoj": (1, 10)
}

# Base URL pattern
base_url_template = "https://oshoworld.com/wp-content/uploads/2020/11/Hindi%20Audio/OSHO-{title}_{:02d}.mp3"

# Iterate over the audio series
for title, (start, end) in audio_series.items():
    # Create a folder for the current series
    folder_name = title.replace(" ", "_")
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Download each file in the range for the series
    for i in range(start, end + 1):
        # Construct the URL
        url = base_url_template.replace("{title}", title.replace(" ", "_")).format(i)
        # Construct the file name
        filename = f"{title}_{i:02d}.mp3"
        filepath = os.path.join(folder_name, filename)

        try:
            print(f"Downloading {filename} to {folder_name}...")
            # Send a GET request to the URL
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Check for HTTP request errors

            # Write the file in chunks to save memory
            with open(filepath, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            print(f"Download complete: {filepath}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while downloading {filename}: {e}")
