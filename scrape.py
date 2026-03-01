import requests
from playwright.sync_api import sync_playwright

def scrape_and_sum():
    seeds = [56, 57, 58, 59, 60, 61, 62, 63, 64, 65]
    grand_total = 0
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        for seed in seeds:
            page = browser.new_page()
            url = f"https://data-kw4d.onrender.com/seed{seed}"
            page.goto(url)
            
            # Extract numbers from tables
            numbers = page.eval_on_selector_all('table td, table th', 
                                                'els => els.map(el => parseFloat(el.textContent)).filter(n => !isNaN(n))')
            seed_sum = sum(numbers)
            print(f"Seed {seed}: sum = {seed_sum}")
            grand_total += seed_sum
            page.close()
        
        browser.close()
    
    # CRITICAL: Print the total in a clear, detectable format
    print("="*50)
    print(f"GRAND TOTAL: {grand_total}")  # This line must be present
    print("="*50)
    print("23ds3000079@ds.study.iitm.ac.in")

if __name__ == "__main__":
    scrape_and_sum()
