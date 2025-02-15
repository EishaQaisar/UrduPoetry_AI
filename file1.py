import requests
from bs4 import BeautifulSoup
import csv

base_url = "https://hamariweb.com/mobiles/poetry_sms_messages14/page-{}"

num_pages = 5  

poetry_data = []

serial_number = 1

for page in range(1, num_pages + 1):
    url = base_url.format(page)
    print(f"Scraping page {page}...")
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    poetry_list = soup.find_all("div", class_="quote_text")

    for poetry in poetry_list:
        poem_text = poetry.get_text(strip=True, separator=" ")
        poetry_data.append([serial_number, poem_text])
        serial_number += 1

csv_filename = "roman_urdu_poetry.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Serial No.", "Poetry"])
    writer.writerows(poetry_data)  

print(f"✅ Data saved successfully to {csv_filename}")
