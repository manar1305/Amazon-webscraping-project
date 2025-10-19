# WinPro: A Website for Selecting good Products in E-commerce Through Review Analysis

## Overview 🚀

Online shopping presents a vast array of choices, making it increasingly challenging for both sellers and buyers. Sellers, especially those utilizing cash-on-delivery (COD) networks, face heightened financial risks due to manual selection processes. Traditional methods demand substantial time and resources, necessitating a smarter alternative. This research introduces a methodology enriched with sentiment analysis to streamline product selection. By integrating sentiment analysis with machine learning, it addresses sellers' unique challenges and enhances decision-making precision in the dynamic e-commerce landscape.

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

<img width="849" alt="1" src="https://github.com/HananeNadi/Sentiment-Analysis-of-Amazon-Reviews/assets/127529925/b4031cca-4f3c-45a6-ad70-b484e1ecc4a9">

<img width="849" alt="2" src="https://github.com/HananeNadi/Sentiment-Analysis-of-Amazon-Reviews/assets/127529925/9ef75d23-7deb-4437-bde2-6975fb8969ff">

<img width="849" alt="3" src="https://github.com/HananeNadi/Sentiment-Analysis-of-Amazon-Reviews/assets/127529925/a7a161d0-ac0f-4eb8-9531-69384e9ed52f">

<img width="849" alt="4" src="https://github.com/HananeNadi/Sentiment-Analysis-of-Amazon-Reviews/assets/127529925/4b9c8825-7636-411c-b65b-2d079828199c">

## Behind the scenes

![URL](https://github.com/HananeNadi/Sentiment-Analysis-of-Amazon-Reviews/assets/127529925/dd33282a-e7b0-44d6-a457-09faace5e8f9)

## Requirement

Web scraping Amazon can be challenging due to strict anti-bot systems such as CAPTCHA, IP blocking, and JavaScript rendering. To overcome these challenges, we used the Scrape.do API, which acts as a proxy + rendering layer for reliable data extraction.

### How It Works

**1.** You send a request to the Scrape.do API with the target Amazon product URL.

**2.** Scrape.do fetches, renders, and returns the fully loaded HTML.

**3.** The project then parses the returned HTML using BeautifulSoup (bs4) and Requests to extract review text, ratings, and metadata.

## Authors

- [@HananeNadi](https://github.com/HananeNadi)
