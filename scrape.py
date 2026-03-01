from playwright.sync_api import sync_playwright
import time

def scrape_all_seeds():
    seeds = [56, 57, 58, 59, 60, 61, 62, 63, 64, 65]
    grand_total = 0
    all_numbers = []
    
    print("="*60)
    print("DataDash QA Automation - 23ds3000079@ds.study.iitm.ac.in")
    print("="*60 + "\n")
    
    with sync_playwright() as p:
        # Launch browser with proper arguments for GitHub Actions
        browser = p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        
        for seed in seeds:
            page = None
            try:
                page = browser.new_page()
                url = f"https://data-kw4d.onrender.com/seed{seed}"
                print(f"Scraping {url}...")
                
                # Navigate with timeout
                page.goto(url, timeout=30000, wait_until="domcontentloaded")
                page.wait_for_timeout(2000)  # Wait for tables to load
                
                # Extract numbers from tables
                numbers = page.evaluate('''
                    () => {
                        const nums = [];
                        document.querySelectorAll('table td, table th').forEach(el => {
                            const val = parseFloat(el.textContent.trim());
                            if (!isNaN(val)) nums.push(val);
                        });
                        return nums;
                    }
                ''')
                
                seed_sum = sum(numbers)
                print(f"  Found {len(numbers)} numbers: {numbers}")
                print(f"  Sum for seed {seed}: {seed_sum}\n")
                
                grand_total += seed_sum
                all_numbers.extend(numbers)
                
            except Exception as e:
                print(f"  Error on seed {seed}: {str(e)}")
            finally:
                if page:
                    page.close()
        
        browser.close()
    
    # Print final results (CRITICAL - this must be in logs)
    print("="*60)
    print(f"TOTAL NUMBERS FOUND: {len(all_numbers)}")
    print(f"GRAND TOTAL SUM: {grand_total}")
    print("="*60)
    print("23ds3000079@ds.study.iitm.ac.in")
    
    # Return success
    return grand_total

if __name__ == "__main__":
    result = scrape_all_seeds()
    print(f"\n✅ Script completed successfully with total: {result}")
