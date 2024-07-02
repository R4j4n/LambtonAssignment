import requests
import pandas as pd
from typing import Any
from tqdm.auto import tqdm
from bs4 import BeautifulSoup


class Scraper:

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
            "title": title,
            "price": price,
            "region": region,
            "nearest intersection": nearest_intersection,
            "link": link,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "unit type": unit_type,
            "parking included": parking_included,
            "size (sqft)": size,
            "pets_friendly": pets_friendly,
            "address": address,
            "description": description,
        }

    def __call__(self) -> Any:
        properties = []

        for page in tqdm(range(1, 2)):
            url = f"https://www.kijiji.ca/b-real-estate/gta-greater-toronto-area+/page-{page}/c34l1700272"
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")

            property_listings = soup.find_all(
                "section", {"data-testid": "listing-card"}
            )

            for property_card in property_listings:
                property_details = self.get_property_detail(property_card)
                properties.append(property_details)

        df = pd.DataFrame(properties)
        df.to_csv("kijiji_real_estate_gta.csv", index=False)


if __name__ == "__main__":
    Scraper()()
