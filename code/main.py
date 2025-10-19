from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
import pandas as pd
import joblib
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import urllib.parse

app = Flask(__name__)

# ------------------ MODEL AND VECTOR SETUP ------------------
model = joblib.load(open('./models/Logistic_regression_reviews.joblib', 'rb'))
tfidvectorizer = joblib.load('./models/tfidfvectorizer_reviews.joblib')
Stopwords_modified = set(stopwords.words('english')) - {'no', 'not','will', 'nor', 'but', 'however', 'although', 'yet', 'unfortunately', 'never', 'none', 'nobody', 'nowhere', 'nothing', 'neither', 'no one', 'without'}
CSV_FILE_PATH = '../data/DATA.csv'
corpus = []
lemmatizer = WordNetLemmatizer()

# ✅ Scrape.do API token
SCRAPE_DO_TOKEN = "c4f97c7b4dfb4dff91a0c20eecfe6406ca95efdccf5"


# ------------------ ROUTES ------------------

@app.route("/")
def Home():
    return render_template("index.html")


@app.route('/predict', methods=["POST"])
def predict():
    url = request.form['Review']
    
    if os.path.exists(CSV_FILE_PATH):
        os.remove(CSV_FILE_PATH)

    review_list = scrape_amazon_reviews(url)
    overall_sentiment = ""  
    result = ""

    if review_list:
        data = pd.DataFrame(review_list)
        data.to_csv('../data/DATA.csv', index=False)
        data['Predicted_Sentiment'] = ""
        data = pd.read_csv('../data/DATA.csv')
        data = data.dropna(subset=['Reviews'])
        data = data.drop_duplicates()

        for i in range(data.shape[0]):
            cleaned_text = re.sub('[^a-zA-Z]', ' ', data.iloc[i]['Reviews'])
            cleaned_text = re.sub(' +', ' ', cleaned_text)
            cleaned_text = cleaned_text.lower()
            tokenized_text = cleaned_text.split()
            lemma_text = [lemmatizer.lemmatize(word) for word in tokenized_text if word not in Stopwords_modified]
            lemma_text_str = ' '.join(lemma_text)
            corpus.append(lemma_text_str)

        x_prediction = tfidvectorizer.transform(corpus)
        y_predictions = model.predict(x_prediction)
        y_predictions = list(map(sentiment_mapping, y_predictions))
        positive_count = sum(1 for sentiment in y_predictions if sentiment == 'positive')
        negative_count = sum(1 for sentiment in y_predictions if sentiment == 'negative')
        
        total_predictions = len(y_predictions)
        positive_percentage = (positive_count / total_predictions) * 100
        negative_percentage = (negative_count / total_predictions) * 100

        if positive_count > negative_count:
            overall_sentiment = f'{positive_percentage:.2f}% of the reviews are positive '
            result = 'The product is good'
        else:
            overall_sentiment = f'{negative_percentage:.2f}% of the reviews are negative'
            result = 'The product is bad'

    return render_template("index.html", prediction_text=overall_sentiment, winning=result, scroll_to_form=True)


# ------------------  SCRAPING FUNCTION ------------------

def scrape_amazon_reviews(url):
    """
    Scrapes Amazon reviews using the Scrape.do API (with pagination support)
    """
    reviews = []

    def get_soup(target_url):
        api_url = f"http://api.scrape.do?token={SCRAPE_DO_TOKEN}&url={urllib.parse.quote_plus(target_url)}&geoCode=us"
        response = requests.get(api_url)
        return BeautifulSoup(response.text, "html.parser")

    def extract_reviews(soup):
        for review in soup.find_all("li", {"data-hook": "review"}):
            rating_elem = review.find("i", {"data-hook": "review-star-rating"}) or review.find("i", class_=re.compile(r"a-icon-star"))
            rating = rating_elem.find("span", class_="a-icon-alt").text.split()[0] if rating_elem else "N/A"

            content_elem = review.find("span", {"data-hook": "review-body"})
            content = content_elem.get_text(strip=True) if content_elem else "N/A"

            if content != "N/A":
                reviews.append({"rate": rating, "Reviews": content})

    # Handle multiple pages
    for i in range(1, 5):  # scrape up to 4 pages
        print(f"Scraping page {i}...")
        paged_url = f"{url}&pageNumber={i}" if "pageNumber=" not in url else re.sub(r'pageNumber=\d+', f'pageNumber={i}', url)
        soup = get_soup(paged_url)
        extract_reviews(soup)
        if not soup.find("li", {"class": "a-last"}):
            break

    print(f" Total reviews scraped: {len(reviews)}")
    return reviews


# ------------------ SENTIMENT MAPPING ------------------

def sentiment_mapping(x):
    return "positive" if x == 1 else "negative"


if __name__ == '__main__':
    app.run(debug=True)
