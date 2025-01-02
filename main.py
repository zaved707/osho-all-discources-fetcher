import os
import requests
from tqdm import tqdm
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

for title, (start, end) in audio_series.items():
    folder_name = title
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    for i in range(start, end + 1):
        # Construct the URL
        url = base_url_template.replace("{title}", title.replace(" ", "_")).format(i)
        # Construct the file name
        filename = f"{title}_{i:02d}.mp3"
        incomplete_filename = f"incomplete_{filename}"
        incomplete_filepath = os.path.join(folder_name, incomplete_filename)
        final_filepath = os.path.join(folder_name, filename)

        # Check if file is already completed
        if os.path.exists(final_filepath):
            print(f"Skipping {filename}, already downloaded.")
            continue

        # Download with a progress bar
        print(f"Downloading {filename} from {url}")
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))

        with open(incomplete_filepath, "wb") as file:
            with tqdm(
                total=total_size,
                unit='B',
                unit_scale=True,
                desc=filename,
                ascii=True
            ) as pbar:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
                    pbar.update(len(chunk))

        # Rename the file to remove "incomplete_" prefix
        os.rename(incomplete_filepath, final_filepath)
        print(f"Saved {filename} to {final_filepath}")