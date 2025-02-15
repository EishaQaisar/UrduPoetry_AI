import requests
from bs4 import BeautifulSoup
import csv
import time
import os

main_url = "https://www.urdusadpoetry.com/category/two-line-urdu-poetry/"


def extract_poetry(post_url, category_name, poetry_data, serial_number):
    try:
        print(f"🔍 Extracting: {post_url} from {category_name}")
        response = requests.get(post_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        poetry_container = soup.find("div", class_="entry-inner")

        if poetry_container:
            paragraphs = poetry_container.find_all("p")
            for para in paragraphs:
                poem_text = para.get_text(strip=True)
                if poem_text:
                    poetry_data.append([serial_number, category_name, poem_text])
                    serial_number += 1
    except Exception as e:
        print(f"❌ Error fetching post: {e}")

    return serial_number

def scrape_category(category_url, category_name):
    current_page = category_url
    poetry_data = []
    serial_number = 1

    while current_page:
        print(f"📂 Scraping Category: {category_name} - Page: {current_page}")

        try:
            response = requests.get(current_page)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

   
            post_links = soup.find_all("h2", class_="post-title entry-title")

            for post in post_links:
                post_url = post.find("a")["href"]
                serial_number = extract_poetry(post_url, category_name, poetry_data, serial_number)

                time.sleep(1)

            next_page_link = soup.find("a", string="Next")
            if next_page_link:
                current_page = next_page_link["href"]
            else:
                current_page = None

        except Exception as e:
            print(f"❌ Error fetching category page: {e}")
            break


    save_category_data(category_name, poetry_data)

def save_category_data(category_name, poetry_data):
    if not poetry_data:
        print(f"⚠️ No data found for {category_name}. Skipping file creation.")
        return

    output_dir = "urdu_poetry_categories"
    os.makedirs(output_dir, exist_ok=True)


    safe_category_name = category_name.replace(" ", "_").replace("/", "_")

    csv_filename = os.path.join(output_dir, f"{safe_category_name}.csv")
    with open(csv_filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Serial No.", "Category", "Poetry"])
        writer.writerows(poetry_data)

    print(f"✅ Data saved successfully to {csv_filename}")


def get_categories():
    try:
        response = requests.get(main_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        categories = []
        
        category_section = soup.find("h3", string="Poetry Categories")
        
        if category_section:
            category_list = category_section.find_next("ul")
            category_links = category_list.find_all("a")

            for link in category_links:
                category_name = link.get_text(strip=True)
                category_url = link["href"]
                categories.append((category_name, category_url))

        return categories
    except Exception as e:
        print(f"❌ Error fetching categories: {e}")
        return []


categories = get_categories()
for category_name, category_url in categories:
    scrape_category(category_url, category_name)

print("🎉 All categories scraped successfully!")
