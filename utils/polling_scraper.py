
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

def scrape_polling_places():
    """
    Scrape polling place information from Hamilton County Election Commission website
    """
    try:
        # Create assets directory if it doesn't exist
        Path('assets').mkdir(exist_ok=True)
        
        # URL for Hamilton County Election Commission polling places
        url = "https://elect.hamiltontn.gov/Polling-Places"
        
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table with polling place information
        polling_places = []
        
        # Extract table data
        table = soup.find('table')
        if table:
            rows = table.find_all('tr')[1:]  # Skip header row
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3:
                    precinct = cols[0].text.strip()
                    location = cols[1].text.strip()
                    address = cols[2].text.strip()
                    
                    # Split address into components
                    addr_parts = address.split(',')
                    if len(addr_parts) >= 2:
                        street = addr_parts[0].strip()
                        city_state_zip = addr_parts[1].strip().split()
                        
                        city = 'Chattanooga'
                        state = 'TN'
                        zip_code = city_state_zip[-1] if city_state_zip else ''
                        
                        polling_places.append({
                            'precinct': precinct,
                            'location_name': location,
                            'address': street,
                            'city': city,
                            'state': state,
                            'zip': zip_code
                        })
        
        # Create DataFrame and save to CSV
        if polling_places:
            df = pd.DataFrame(polling_places)
            df.to_csv('assets/polling_places.csv', index=False)
            print(f"Successfully saved {len(polling_places)} polling places")
            return True
            
        return False
        
    except Exception as e:
        print(f"Error scraping polling places: {str(e)}")
        return False

if __name__ == '__main__':
    success = scrape_polling_places()
    if success:
        print("Polling places updated successfully")
    else:
        print("Failed to update polling places")
