from playwright.sync_api import sync_playwright
import re

SEEDS = [56, 57, 58, 59, 60, 61, 62, 63, 64, 65]

def scrape_seed(seed):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        url = f"https://data-kw4d.onrender.com/seed{seed}"
        print(f"Scraping {url}")
        
        page.goto(url, wait_until="networkidle")
        
        # Find all numbers in tables
        numbers = []
        tables = page.query_selector_all('table')
        
        for table in tables:
            cells = table.query_selector_all('td, th')
            for cell in cells:
                text = cell.text_content().strip()
                try:
                    num = float(text)
                    numbers.append(num)
                except ValueError:
                    pass
        
        browser.close()
        
        seed_sum = sum(numbers)
        print(f"  Found {len(numbers)} numbers: {numbers}")
        print(f"  Sum for seed {seed}: {seed_sum}\n")
        
        return numbers, seed_sum

def main():
    grand_total = 0
    all_numbers = []
    
    print("=" * 60)
    print("DataDash QA Automation - 23ds3000079@ds.study.iitm.ac.in")
    print("=" * 60 + "\n")
    
    for seed in SEEDS:
        numbers, seed_sum = scrape_seed(seed)
        all_numbers.extend(numbers)
        grand_total += seed_sum
    
    print("=" * 60)
    print(f"TOTAL NUMBERS FOUND: {len(all_numbers)}")
    print(f"GRAND TOTAL SUM: {grand_total}")
    print("=" * 60)

if __name__ == "__main__":
    main()