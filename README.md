# WinPro: A Website for Selecting good Products in E-commerce Through Review Analysis

## Overview 🚀
Online shopping offers a vast array of choices, which can make decision-making increasingly difficult for both sellers and buyers. This challenge is especially pronounced for those relying on cash-on-delivery (COD) networks, where manual product selection introduces significant financial risks. Traditional methods are often time-consuming and resource-intensive, highlighting the need for a smarter, more efficient approach.

Additionally, customers benefit from this project by quickly identifying high-quality products without the hassle of sifting through hundreds of reviews. The system streamlines the decision-making process, enabling users to make faster, more informed choices with greater confidence.

This research presents a novel methodology that leverages sentiment analysis combined with machine learning to simplify product selection. By addressing the unique challenges faced by sellers and buyers alike, it enhances decision-making accuracy and efficiency within the dynamic e-commerce landscape.

## 🗂️ Project Structure

```bash
WEBSCRAPING-PROJECT/
├── code/                          # Main source code folder
│   ├── models/                    # Serialized ML models saved with joblib (Logistic Regression + TF-IDF)
│   ├── static/                    # Static web assets for the Flask interface (CSS, images)
│   ├── templates/                 # HTML templates for the Flask web app
│   ├── amazon_reviews_analysis.ipynb  # Jupyter Notebook for EDA and Machine Learning
│   ├── scraping.py                # Script responsible for web scraping Amazon product data
│   └── main.py                    # Flask app to serve the web interface and connect predictions
│
├── data/                          # CSV files used in the project
│   ├── raw-data.csv               # Raw scraped data before preprocessing
│   └── processed-data.csv         # Cleaned and processed data used for ML analysis
│
├── demo/                          # Folder containing demo materials
│   ├── images/                    # Visualizations generated from the notebook (EDA plots, word clouds, etc.)
│   └── videos/                    # Final project demonstration videos (e.g., amazon-project.mp4)
│
├── README.md                      # Project documentation (this file)
├── requirements.txt               # Python dependencies needed to run the project

```

## Key highlights :

- **Data Collection**: Collected Amazon electronics reviews using the Scrape.do API, which acts as a proxy + rendering layer to bypass anti-bot measures such as CAPTCHAs. After retrieving the rendered HTML from Scrape.do, we parse and extract review text, ratings, and metadata using requests and BeautifulSoup (bs4). This approach avoids running a local JS renderer and keeps scraping logic simple and reliable
- **Data Cleaning & Pre-Processing**: Employed meticulous data cleaning and preprocessing techniques to refine textual data, including the removal of punctuation and stop words, tokenization, and lemmatization, enhancing the effectiveness of sentiment analysis.

- **Exploratory Data Analysis (EDA)**: Conducted insightful visualizations and analyses to unravel key patterns and distributions within the dataset, facilitating a deeper understanding of underlying trends.

- **Machine Learning Models**: Explored a diverse range of machine learning algorithms, including Logistic Regression,and Naive Bayes to discern the most suitable approach for classifying Amazon electronics reviews accurately.

- **Feature Extraction**: Implemented advanced text processing methodologies to convert electronics reviews into numerical vectors, leveraging techniques such as TF-IDF and n-grams to capture nuanced insights.

- **Evaluation**: Employed rigorous evaluation metrics, including accuracy, precision, recall, and F1-score, to meticulously assess model performance. Leveraged grid search techniques to optimize model parameters, ultimately selecting Logistic Regression as the top-performing classifier for our task.

- **Deployment**: Created a user-friendly website with HTML, CSS, and Flask, offering intuitive design and enabling input of Amazon product URLs.

## Tools Used

- Python
- Flask
- HTML
- CSS

## Preview

![1](https://github.com/user-attachments/assets/b9675fb0-7abb-4371-b2cf-a4f2f580dfe4)
![2](https://github.com/user-attachments/assets/df57a8ab-f6ee-4f7a-b894-8278505c6201)
<img width="905" height="453" alt="3 3" src="https://github.com/user-attachments/assets/ea0f2400-7136-4ec9-97b7-12f78a7e4b89" />
![3](https://github.com/user-attachments/assets/9dc3a12b-cd42-48f4-8b69-b03b5d4bf92d)




## Workflow Summary

1. **Amazon URL**  
2. **Scraping** using Scrap.do + BeautifulSoup  
3. **Save as CSV**  
4. **Data Cleaning** using Pandas  
5. **Load Pretrained Models** (TF-IDF + Logistic Regression via joblib)  
6. **Sentiment Prediction** (Positive / Negative)


## 📡 Requirements & Scraping Strategy

Web scraping Amazon can be challenging due to strict anti-bot systems such as CAPTCHA, IP blocking, and JavaScript rendering. To overcome these challenges, we used the Scrape.do API, which acts as a proxy + rendering layer for reliable data extraction.

### How It Works

**1.** You send a request to the Scrape.do API with the target Amazon product URL.

**2.** Scrape.do fetches, renders, and returns the fully loaded HTML.

**3.** The project then parses the returned HTML using BeautifulSoup (bs4) and Requests to extract review text, ratings, and metadata.


##  Conclusion: Discussion on Results and Limitations

This project was driven by a simple yet powerful intuition: **customer reviews can serve as a reliable indicator of product quality**. By applying sentiment analysis and machine learning, we successfully built a prototype capable of predicting review polarity with reasonable accuracy.

However, several **limitations** emerged:

- **Small Dataset**: Only 932 reviews were scraped, due to the Scrape.do API’s free tier limit of 1000 requests. This is insufficient for training a production-grade sentiment model. A larger dataset would yield significantly better performance.
  
- **Data Quality**: Reviews may be fake or biased, introducing noise in predictions.

- **Platform Limitation**: Our model is trained only on Amazon reviews and may not generalize to other platforms like eBay or AliExpress.

- **Model Simplicity**: We used traditional ML models (TF-IDF + Logistic Regression). More advanced NLP models (e.g., BERT) could capture context more effectively.

- **Language Limitation**: The current system only supports English reviews.


### 🚀 Future Improvements

To improve this project:

- Scrape larger, more diverse datasets to improve model training.
- Adopt state-of-the-art NLP models like BERT or RoBERTa.
- Extend the system to support multiple e-commerce platforms and languages.
- Add a comparison dashboard for reviewing multiple products side-by-side.

## Authors
- [@manar1305](https://github.com/manar1305)
- [@HananeNadi](https://github.com/HananeNadi)
