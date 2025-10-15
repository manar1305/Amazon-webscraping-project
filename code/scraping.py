import requests
import urllib.parse
import csv
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime

# Config
TOKEN = "75250c6ad9364162a86488532b07de015ee64cbc94c"
MAX_PRODUCTS_PER_CATEGORY = 20  
MAX_REVIEWS_PER_PRODUCT = 5 

# Smart Home Categories
CATEGORIES = {
    "Smart Home Lighting": "https://us.amazon.com/gp/browse.html?node=21217035011",
    "Smart Locks and Entry": "https://us.amazon.com/s?k=smart+locks&rh=n%3A6563140011",
    "Security Cameras": "https://us.amazon.com/s?k=security+cameras&rh=n%3A6563140011",
    "Smart Plugs and Outlets": "https://us.amazon.com/s?k=smart+plugs&rh=n%3A6563140011",
    "Smart Thermostats": "https://us.amazon.com/s?k=smart+thermostats&rh=n%3A6563140011",
    "Smart Detectors": "https://us.amazon.com/s?k=smart+detectors&rh=n%3A6563140011",
    "Smart Home Entertainment": "https://us.amazon.com/s?k=smart+home+entertainment&rh=n%3A6563140011",
    "Smart Pet Devices": "https://us.amazon.com/s?k=smart+pet+devices&rh=n%3A6563140011",
    "Voice Assistants": "https://us.amazon.com/s?k=voice+assistants&rh=n%3A6563140011",
    "Smart Kitchen": "https://us.amazon.com/s?k=smart+kitchen&rh=n%3A6563140011",
    "Robot Vacuums": "https://us.amazon.com/s?k=robot+vacuum&rh=n%3A6563140011",
    "Smart Garden": "https://us.amazon.com/s?k=smart+garden&rh=n%3A6563140011",
    "Smart WiFi": "https://us.amazon.com/s?k=smart+wifi+mesh&rh=n%3A6563140011"
}

def get_soup(url):
    api_url = f"http://api.scrape.do?token={TOKEN}&url={urllib.parse.quote_plus(url)}&geoCode=us"
    try:
        response = requests.get(api_url, timeout=30)
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
        if link_elem and link_elem.get("href"):
            href = link_elem.get("href")
            if href.startswith("/"):
                full_url = f"https://us.amazon.com{href}"
            else:
                full_url = href
            
            # Extract ASIN from URL
            asin_match = re.search(r'/dp/([A-Z0-9]{10})', full_url)
            if asin_match:
                asin = asin_match.group(1)
                # Create clean product URL
                product_url = f"https://us.amazon.com/dp/{asin}"
                if product_url not in product_links:
                    product_links.append(product_url)
    
    return product_links

def extract_product_info(product_url):
    soup = get_soup(product_url)
    if not soup:
        return None
    
    # Extract product title
    title_elem = soup.find("span", {"id": "productTitle"})
    title = title_elem.get_text(strip=True) if title_elem else "N/A"
    
    # Extract price
    price_elem = soup.find("span", class_=re.compile(r"a-price-whole"))
    price = price_elem.get_text(strip=True) if price_elem else "N/A"
    
    # Extract rating
    rating_elem = soup.find("span", class_="a-icon-alt")
    rating = rating_elem.get_text(strip=True).split()[0] if rating_elem else "N/A"
    
    # Extract number of reviews
    review_count_elem = soup.find("span", {"id": "acrCustomerReviewText"})
    review_count = review_count_elem.get_text(strip=True).split()[0] if review_count_elem else "0"
    
    return {
        "title": title,
        "price": price,
        "rating": rating,
        "review_count": review_count,
        "url": product_url
    }

def extract_reviews(product_url, max_reviews):
    soup = get_soup(product_url)
    if not soup:
        return []
    
    reviews = []

    review_elements = soup.find_all("li", {"data-hook": "review"})
    
    for review in review_elements[:max_reviews]:
        # Extract rating 
        rating_elem = review.find("i", {"data-hook": "review-star-rating"}) or review.find("i", class_=re.compile(r"a-icon-star"))
        rating = rating_elem.find("span", class_="a-icon-alt").text.split()[0] if rating_elem else "N/A"
        
        # Extract date
        date_elem = review.find("span", {"data-hook": "review-date"})
        date = re.sub(r"Reviewed in .* on ", "", date_elem.text) if date_elem else "N/A"
        
        # Extract review title
        title_elem = review.find("a", {"data-hook": "review-title"})
        review_title = title_elem.get_text(strip=True) if title_elem else "N/A"
        
        # Extract content 
        content_elem = review.find("span", {"data-hook": "review-body"})
        content = content_elem.get_text(strip=True) if content_elem else "N/A"
        
        # Extract helpful votes 
        helpful_elem = review.find("span", {"data-hook": "helpful-vote-statement"})
        helpful = re.findall(r'\d+', helpful_elem.text)[0] if helpful_elem and re.findall(r'\d+', helpful_elem.text) else "0"
        
        reviews.append({
            "rating": rating,
            "date": date,
            "title": review_title,
            "content": content,
            "helpful": helpful
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
        print(f"{'='*60}")
        
        # Get product links
        product_links = extract_product_links(category_url, MAX_PRODUCTS_PER_CATEGORY)
        print(f"Found {len(product_links)} products")
        
        # Process each product
        for idx, product_url in enumerate(product_links, 1):
            print(f"\n[{idx}/{len(product_links)}] Processing product...")
            
            # Get product info
            product_info = extract_product_info(product_url)
            if not product_info:
                print(" Could not extract product info")
                continue
            
            print(f" Product: {product_info['title'][:50]}...")
            print(f" Price: ${product_info['price']} | Rating: {product_info['rating']}")
            
            # Get reviews
            reviews = extract_reviews(product_url, MAX_REVIEWS_PER_PRODUCT)
            print(f" Found {len(reviews)} reviews")
            
            # Combine data
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
                        "review_content": review['content'],
                        "review_helpful": review['helpful']
                    })
            else:
                # Add product without reviews
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
                    "review_content": "N/A",
                    "review_helpful": "0"
                })
            
            time.sleep(2)
    
    # Save to a csv file
    if all_data:
        filename = f"smart_home_products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
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