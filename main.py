import json
from time import sleep
import random
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time

def random_sleep(min_seconds=1, max_seconds=3):
    """Sleep for a random time between min_seconds and max_seconds (inclusive)."""
    duration = random.uniform(min_seconds, max_seconds)
    print(f"Sleeping for {duration:.2f} seconds...")
    sleep(duration)

def random_retry_sleep(min_seconds=60, max_seconds=180):
    """Sleep for a longer time before retrying after failure."""
    duration = random.uniform(min_seconds, max_seconds)
    print(f"[RETRY] Sleeping for {duration:.2f} seconds before retrying...")
    sleep(duration)

def create_driver():
    """Creates a fresh instance of undetected Chrome driver."""
    options = uc.ChromeOptions()
    options.headless = True  # type: ignore
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    return uc.Chrome(options=options)

def scrape_most_actives():
    base_url = "https://finance.yahoo.com/research-hub/screener/most_actives/?start={}&count=25"
    start = 0
    results = []
    max_retries = 3
    retries = 0

    driver = create_driver()

    try:
        while True:
            try:
                url = base_url.format(start)
                print(f"Scraping: {url}")
                driver.get(url)
                time.sleep(3)  # Wait for JS to render

                soup = BeautifulSoup(driver.page_source, "html.parser")
                rows = soup.select("table tr")

                if not rows:  # adjust limit here if needed
                    print("No more data found or reached scraping limit. Stopping.")
                    break

                count_this_page = 0
                for row in rows:
                    symbol_cell = row.select_one("td:nth-child(2) a div")
                    name_cell = row.select_one("td:nth-child(3) div")
                    if symbol_cell and name_cell:
                        results.append({
                            "symbol": symbol_cell.text.strip(),
                            "name": name_cell.text.strip()
                        })
                        count_this_page += 1

                print(f"Scraped {count_this_page} items from page.")
                start += 25
                retries = 0  # reset retry count on success
                random_sleep(5, 15)

            except Exception as e:
                print(f"[ERROR] Scraping failed at start={start}: {e}")
                retries += 1
                try:
                    driver.quit()
                except:
                    pass

                if retries > max_retries:
                    print(f"[FATAL] Max retries exceeded at start={start}. Exiting.")
                    break

                random_retry_sleep()
                driver = create_driver()  # Restart browser

    finally:
        driver.quit()

    return results

if __name__ == "__main__":
    stocks = scrape_most_actives()
    print(f"Total items scraped: {len(stocks)}")

    # Write to JSON file
    with open("most_actives.json", "w") as f:
        json.dump(stocks, f, indent=2)

    print("Saved to most_actives.json")

