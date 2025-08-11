# main.py (Final architectural version)

from scraper import scrape_navi_mumbai_properties
from analyzer import analyze_properties
from dashboard import create_dashboard
import database

if __name__ == "__main__":
    
    database.init_db()
    print("Starting the Real-Time Mumbai Property Deal Hunter...")
    
    # Run the scraper and analyzer to update our database
    raw_properties_df = scrape_navi_mumbai_properties()
    
    if not raw_properties_df.empty:
        print(f"\n--- Scraped {len(raw_properties_df)} new properties ---")
        analyzed_df = analyze_properties(raw_properties_df)
        if not analyzed_df.empty:
            database.save_properties(analyzed_df)
    else:
        print("\n--- Could not scrape any new data. ---")
        
    # THIS IS THE CHANGE: We always load from the database and launch the dashboard
    # The dashboard itself is now smart enough to handle being empty.
    print("Loading all data from database...")
    all_time_df = database.load_all_properties()
    
    print("Launching Dashboard...")
    create_dashboard(all_time_df)
        
    print("\nProcess finished.")