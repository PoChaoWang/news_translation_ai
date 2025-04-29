## Introduction
This project is dedicated to using the OpenAI API.

Originally, this project was created to help me quickly access overseas F1 news. Watching F1 races is my hobby, but I don't want to spend too much time searching for news or reading English articles. Therefore, I used Open Router's Gemini to translate overseas news and published the content on https://f1-news.netlify.app/.

### Main Files

- **`main.py`**: The main script responsible for executing the entire pipeline, including news scraping, data cleaning, and translation.
- **`crawler.py`**: Handles news scraping from RSS feeds and parsing article content.
- **`cleaning.py`**: Cleans the scraped news data by removing unnecessary HTML tags and duplicates.
- **`translate_openai.py`**: Translates news titles and content using the OpenAI API.
- **`prompts/`**: Contains Jinja2 templates required for translation.

## Features

### 1. News Scraping
Uses the `run_f1_news_crawler` function in `crawler.py` to scrape news from multiple RSS feed sources and parse article content.

### 2. Data Cleaning
Uses the `merge_and_clean_data` function in `cleaning.py` to clean the scraped data by removing duplicates and unnecessary HTML tags.

### 3. News Translation
Uses the `fetch_and_translate_column` function in `translate_openai.py` to translate the cleaned news content into Chinese.

## Installation and Usage

### 1. Install Dependencies
Ensure Python 3.9 or above is installed, then run the following command to install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Set the OpenAI API key in the `.env` file.

### 3. Run the Pipeline
Execute the main script:

```bash
python main.py
```

### 4. Output Results
- Raw data is stored in `debug/raw/`.
- Cleaned data is stored in `debug/cleaned_data/`.
- Translated data is stored in `debug/translated_data/`.

### Logs
Log files are stored in `logs/translate_errors.log`, recording errors and information during the scraping, cleaning, and translation processes.

## File Details

### `crawler.py`
- `fetch_f1_news`: Scrapes news from RSS feeds.
- `scrape_article_content`: Parses article content.
- `run_f1_news_crawler`: Executes the news scraping process and saves the results.

### `cleaning.py`
- `clean_data`: Cleans data by removing unnecessary HTML tags and attributes.
- `merge_and_clean_data`: Merges and cleans data, removing duplicates.

### `translate_openai.py`
- `translate_text`: Translates text using the OpenAI API.
- `fetch_and_translate_column`: Translates cleaned data and saves the results.

## Notes
- Ensure the `.env` file is configured with the correct OpenAI API key.
- The translation process may take some time due to random delays between requests.