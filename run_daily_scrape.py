# run_daily_scrape.py

from scraper import scrape_navi_mumbai_properties
from analyzer import analyze_properties
import database

if __name__ == "__main__":
    print("--- STARTING DAILY GITHUB ACTIONS SCRAPE JOB ---")
    database.init_db()
    raw_df = scrape_navi_mumbai_properties()
    if not raw_df.empty:
        analyzed_df = analyze_properties(raw_df)
        if not analyzed_df.empty:
            database.save_properties(analyzed_df)
    print("--- DAILY GITHUB ACTIONS SCRAPE JOB FINISHED ---")