import requests
import urllib.parse
import csv
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime
import os

# Config
TOKEN = "use your own token here from scrape.do"
MAX_PRODUCTS_PER_CATEGORY = 20
MAX_REVIEWS_PER_PRODUCT = 5

# Categories chosen for our use case
CATEGORY_KEYWORDS = [
    "smart locks",
    "security cameras",
    "smart plugs",
    "smart thermostats",
    "smart detectors",
    "smart home entertainment",
    "smart pet devices",
    "voice assistants",
    "smart kitchen",
    "robot vacuum",
    "smart garden",
    "smart wifi mesh",
]

AMAZON_SEARCH_BASE = "https://us.amazon.com/s?k={k}&rh=n%3A6563140011"

def build_category_url(keyword: str) -> str:
    k = urllib.parse.quote_plus(keyword.strip())
    return AMAZON_SEARCH_BASE.format(k=k)

# Dict{category name: URL}
CATEGORIES = {kw.title(): build_category_url(kw) for kw in CATEGORY_KEYWORDS}


# Functions for scraping
def get_soup(url):
    api_url = f"http://api.scrape.do?token={TOKEN}&url={urllib.parse.quote_plus(url)}&geoCode=us"
    try:
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_product_links(category_url, max_products):
    print(f"Fetching products from category...")
    soup = get_soup(category_url)
    if not soup:
        return []

    product_links = []
    products = soup.find_all("div", {"data-component-type": "s-search-result"})

    for product in products[:max_products]:
        link_elem = product.find("a", class_=re.compile(r"a-link-normal.*s-no-outline"))
        if not link_elem or not link_elem.get("href"):
            continue

        href = link_elem.get("href")
        full_url = f"https://us.amazon.com{href}" if href.startswith("/") else href

        asin_match = re.search(r"/dp/([A-Z0-9]{10})", full_url)
        if not asin_match:
            data_asin = product.get("data-asin")
            if data_asin and re.fullmatch(r"[A-Z0-9]{10}", data_asin):
                asin = data_asin
            else:
                continue
        else:
            asin = asin_match.group(1)

        product_url = f"https://us.amazon.com/dp/{asin}"
        if product_url not in product_links:
            product_links.append(product_url)

    return product_links

# Function for general data of products
def extract_product_info(product_url):
    soup = get_soup(product_url)
    if not soup:
        return None

    title_elem = soup.find("span", {"id": "productTitle"})
    title = title_elem.get_text(strip=True) if title_elem else "N/A"

    price_elem = soup.find("span", class_=re.compile(r"a-price-whole"))
    price = price_elem.get_text(strip=True) if price_elem else "N/A"

    rating_elem = soup.find("span", class_="a-icon-alt")
    rating = rating_elem.get_text(strip=True).split()[0] if rating_elem else "N/A"

    review_count_elem = soup.find("span", {"id": "acrCustomerReviewText"})
    review_count = review_count_elem.get_text(strip=True).split()[0] if review_count_elem else "0"

    return {
        "title": title,
        "price": price,
        "rating": rating,
        "review_count": review_count,
        "url": product_url
    }

# Function to exctract products' reviews 
def extract_reviews(product_url, max_reviews):
    soup = get_soup(product_url)
    if not soup:
        return []

    reviews = []
    review_elements = soup.find_all("li", {"data-hook": "review"})

    for review in review_elements[:max_reviews]:
        rating_elem = review.find("i", {"data-hook": "review-star-rating"}) or review.find("i", class_=re.compile(r"a-icon-star"))
        rating = rating_elem.find("span", class_="a-icon-alt").text.split()[0] if rating_elem else "N/A"

        date_elem = review.find("span", {"data-hook": "review-date"})
        date = re.sub(r"Reviewed in .* on ", "", date_elem.text) if date_elem else "N/A"

        title_elem = review.find("a", {"data-hook": "review-title"})
        review_title = title_elem.get_text(strip=True) if title_elem else "N/A"

        content_elem = review.find("span", {"data-hook": "review-body"})
        content = content_elem.get_text(strip=True) if content_elem else "N/A"

        reviews.append({
            "rating": rating,
            "date": date,
            "title": review_title,
            "content": content
        })

    return reviews

def main():
    all_data = []

    print(f"Starting scrape at {datetime.now()}")
    print(f"Max products per category: {MAX_PRODUCTS_PER_CATEGORY}")
    print(f"Max reviews per product: {MAX_REVIEWS_PER_PRODUCT}\n")

    for category_name, category_url in CATEGORIES.items():
        print(f"\n{'='*60}")
        print(f"Category: {category_name}")
        print(f"URL: {category_url}")
        print(f"{'='*60}")

        product_links = extract_product_links(category_url, MAX_PRODUCTS_PER_CATEGORY)
        print(f"Found {len(product_links)} products")

        for idx, product_url in enumerate(product_links, 1):
            print(f"\n[{idx}/{len(product_links)}] Processing product...")

            product_info = extract_product_info(product_url)
            if not product_info:
                print(" Could not extract product info")
                continue

            print(f" Product: {product_info['title'][:50]}...")
            print(f" Price: ${product_info['price']} | Rating: {product_info['rating']}")

            reviews = extract_reviews(product_url, MAX_REVIEWS_PER_PRODUCT)
            print(f" Found {len(reviews)} reviews")

            if reviews:
                for review in reviews:
                    all_data.append({
                        "category": category_name,
                        "product_title": product_info['title'],
                        "product_price": product_info['price'],
                        "product_rating": product_info['rating'],
                        "product_review_count": product_info['review_count'],
                        "product_url": product_info['url'],
                        "review_rating": review['rating'],
                        "review_date": review['date'],
                        "review_title": review['title'],
                        "review_content": review['content']
                    })
            else:
                all_data.append({
                    "category": category_name,
                    "product_title": product_info['title'],
                    "product_price": product_info['price'],
                    "product_rating": product_info['rating'],
                    "product_review_count": product_info['review_count'],
                    "product_url": product_info['url'],
                    "review_rating": "N/A",
                    "review_date": "N/A",
                    "review_title": "N/A",
                    "review_content": "N/A"
                })

            time.sleep(2)

    if all_data:
        output_dir = "data"
        os.makedirs(output_dir, exist_ok=True) 
        filename = os.path.join(output_dir, "raw-data.csv")

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=all_data[0].keys())
            writer.writeheader()
            writer.writerows(all_data)

        print(f"\n{'='*60}")
        print(f" Scraped {len(all_data)} total rows")
        print(f" Saved to: {filename}")
        print(f"{'='*60}")

    else:
        print("\n No data collected")

if __name__ == "__main__":
    main()