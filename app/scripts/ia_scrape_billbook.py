import requests
from bs4 import BeautifulSoup
import time
import json
import os
import base64

"""
TODO:
- Check to see which returned bills are not in the database
- If the bill is note in the database, use the curl request to pull down the bill html
- Send the html to the bill_text endpoint
- Hit the new manual_bill_entry endpoint with the data
"""

def get_bill_html(bill_number):
    url = f"https://www.legis.iowa.gov/docs/publications/LGI/91/attachments/{bill_number}.html?layout=false"
    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Referer': f'https://www.legis.iowa.gov/legislation/BillBook?ba={bill_number}&ga=91',
        'Sec-Fetch-Dest': 'iframe',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"'
    }

    # Set up the proxies for requests
    proxy_url = os.getenv("QUOTAGUARDSTATIC_URL")
    proxies = {
        "http": proxy_url,
        "https": proxy_url
    }
    
    try:
        response = requests.get(url, headers=headers, proxies=proxies)
        
        if response.status_code == 404:
            print(f"Bill {bill_number} not found (404)")
            return None
            
        response.raise_for_status()
        
        if len(response.text) < 50:
            print(f"Bill {bill_number} returned empty or invalid content")
            return None
            
        return response.text
        
    except requests.RequestException as e:
        print(f"Error fetching bill {bill_number}: {e}")
        return None
    
def convert_to_base64(html_content):
    return base64.b64encode(html_content.encode()).decode('utf-8')

def convert_to_markdown(html_content):
    try:
        response = requests.post(
            "https://html-processor-a2023f193a99.herokuapp.com/api/v1/bill-text/convert",
            json={"html_content_base64": html_content},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()["text"]
    except requests.RequestException as e:
        print(f"Error converting HTML to markdown: {e}")
        return None

def scrape_bills():
    os.makedirs("bills", exist_ok=True)
    
    url = "https://www.legis.iowa.gov/legislation/billTracking/billpacket"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        bill_table = soup.find('table', class_='standard sortable divideVert')
        
        if bill_table:
            bill_links = bill_table.find_all('a')
            for link in bill_links:
                bill_number = link.text.strip().replace(" ", "")
                print(f"Fetching bill: {bill_number}")
                
                bill_html = get_bill_html(bill_number)
                if bill_html:
                    base64_html = convert_to_base64(bill_html)
                    markdown_text = convert_to_markdown(base64_html)
                    if markdown_text:
                        with open(f"bills/{bill_number}.txt", "w", encoding="utf-8") as f:
                            f.write(markdown_text)
                        print(f"Saved bill {bill_number} text")
                    else:
                        print(f"Failed to convert bill {bill_number} to markdown")
                time.sleep(1)
                
    except requests.RequestException as e:
        print(f"An error occurred while fetching the page: {e}")

def main():
    while True:
        print("Scraping bills:")
        scrape_bills()
        print("\nWaiting for 15 minutes before next scrape...")
        time.sleep(900)  # Wait for 15 minutes

if __name__ == "__main__":
    main()
