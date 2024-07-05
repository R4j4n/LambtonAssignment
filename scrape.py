import requests
import pandas as pd
import sqlite3
from typing import Any
from tqdm.auto import tqdm
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed


class Scraper:

    def __init__(self, db_name="kijiji_real_estate_gta.db"):
        self.db_name = db_name
        self.create_db()

    def create_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS properties (
                url TEXT PRIMARY KEY,
                title TEXT,
                price TEXT,
                region TEXT,
                nearest_intersection TEXT,
                bedrooms TEXT,
                bathrooms TEXT,
                unit_type TEXT,
                parking_included TEXT,
                size_sqft TEXT,
                pets_friendly TEXT,
                address TEXT,
                description TEXT
            )
        """
        )
        conn.commit()
        conn.close()

    def get_description(self, link):
        try:
            response = requests.get(link)
            soup = BeautifulSoup(response.content, "html.parser")
            address_tag = soup.find("span", {"itemprop": "address"})
            address = address_tag.get_text(strip=True) if address_tag else "N/A"
            description = ""

            p_tags = soup.select("div > p")

            for p_tag in p_tags:
                description += p_tag.get_text(strip=True)

            return address, description

        except:
            return "N/A", "N/A"

    def get_property_detail(self, property_card):
        title_tag = property_card.find("a", {"data-testid": "listing-link"})
        title = title_tag.get_text(strip=True) if title_tag else "N/A"
        link = "https://kijiji.ca/" + title_tag["href"] if title_tag else "N/A"

        price_tag = property_card.find("p", {"data-testid": "listing-price"})
        price = price_tag.get_text(strip=True) if price_tag else "N/A"

        region_tag = property_card.find("p", {"data-testid": "listing-location"})
        region = region_tag.get_text(strip=True) if region_tag else "N/A"

        nearest_intersection_tag = property_card.find(
            "li", {"aria-label": "Nearest intersection"}
        )
        nearest_intersection = (
            nearest_intersection_tag.get_text(strip=True)
            if nearest_intersection_tag
            else "N/A"
        )

        bedrooms_tag = property_card.find("li", {"aria-label": "Bedrooms"})
        bedrooms = bedrooms_tag.get_text(strip=True) if bedrooms_tag else "N/A"

        bathrooms_tag = property_card.find("li", {"aria-label": "Bathrooms"})
        bathrooms = bathrooms_tag.get_text(strip=True) if bathrooms_tag else "N/A"

        unit_type_tag = property_card.find("li", {"aria-label": "Unit type"})
        unit_type = unit_type_tag.get_text(strip=True) if unit_type_tag else "N/A"

        parking_included_tag = property_card.find(
            "li", {"aria-label": "Parking included"}
        )
        parking_included = (
            parking_included_tag.get_text(strip=True) if parking_included_tag else "N/A"
        )

        size_tag = property_card.find("li", {"aria-label": "Size (sqft)"})
        size = size_tag.get_text(strip=True) if size_tag else "N/A"

        pets_friendly_tag = property_card.find("li", {"aria-label": "Pets friendly"})
        pets_friendly = (
            pets_friendly_tag.get_text(strip=True) if pets_friendly_tag else "N/A"
        )

        address, description = self.get_description(link)

        return {
            "url": link,
            "title": title,
            "price": price,
            "region": region,
            "nearest_intersection": nearest_intersection,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "unit_type": unit_type,
            "parking_included": parking_included,
            "size_sqft": size,
            "pets_friendly": pets_friendly,
            "address": address,
            "description": description,
        }

    def save_to_db(self, property_details):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO properties (
                url, title, price, region, nearest_intersection, bedrooms,
                bathrooms, unit_type, parking_included, size_sqft, pets_friendly,
                address, description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                property_details["url"],
                property_details["title"],
                property_details["price"],
                property_details["region"],
                property_details["nearest_intersection"],
                property_details["bedrooms"],
                property_details["bathrooms"],
                property_details["unit_type"],
                property_details["parking_included"],
                property_details["size_sqft"],
                property_details["pets_friendly"],
                property_details["address"],
                property_details["description"],
            ),
        )
        conn.commit()
        conn.close()

    def scrape_page(self, page):
        url = f"https://www.kijiji.ca/b-real-estate/gta-greater-toronto-area+/page-{page}/c34l1700272"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        property_listings = soup.find_all("section", {"data-testid": "listing-card"})
        for property_card in property_listings:
            property_details = self.get_property_detail(property_card)
            self.save_to_db(property_details)

    def __call__(self, num_pages=2) -> Any:
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.scrape_page, page)
                for page in range(1, num_pages + 1)
            ]
            for future in tqdm(as_completed(futures), total=num_pages):
                future.result()


if __name__ == "__main__":

    from multiprocessing import cpu_count

    n_cores = cpu_count()
    print(f"Number of Logical CPU cores: {n_cores}")
    print(f"Using all {n_cores} Logical CPU cores.")

    Scraper()(num_pages=1900)
