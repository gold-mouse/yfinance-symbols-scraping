# Yahoo Finance Most Active Stocks Scraper

## 📄 Description
This Python script scrapes the **"Most Actives"** stock listings from [Yahoo Finance](https://finance.yahoo.com/research-hub/screener/most_actives) using a headless browser powered by `undetected-chromedriver`. It collects stock symbols and names and saves the data as a JSON file.

---

## 🚀 Features
- Headless Chrome browser automation via `undetected-chromedriver`
- Scrapes stock symbols and names from a dynamic webpage
- Implements randomized sleep to mimic human browsing and avoid detection
- Automatic retry on scraping failures
- Outputs clean, structured data to `most_actives.json`

---

## 🧰 Requirements

- Python 3.7+
- Install required packages:

```bash
pip install undetected-chromedriver beautifulsoup4 lxml
```

---

## 📦 Usage

Run the script from your terminal:

```bash
python scrape_yahoo_most_actives.py
```

### What it does:
- Begins scraping from index 50025
- Extracts stock symbol and company name from each page
- Handles retries and browser restarts if any errors occur
- Saves the results in `most_actives.json`

---

## 📁 Output

A sample output (`most_actives.json`):

```json
[
  {
    "symbol": "AAPL",
    "name": "Apple Inc."
  },
  {
    "symbol": "MSFT",
    "name": "Microsoft Corporation"
  }
]
```

---

## 📝 Notes

- You can modify the `start` variable in the script to change the page index to start scraping from.
- Use responsibly and in accordance with Yahoo Finance's terms of service.

---

## 👤 Author

@gold-mouse
