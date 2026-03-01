from playwright.sync_api import sync_playwright
import time

def scrape_all_seeds():
    seeds = [56, 57, 58, 59, 60, 61, 62, 63, 64, 65]
    grand_total = 0
    all_numbers = []
    
    print("="*60)
    print("DataDash QA Automation - 23ds3000079@ds.study.iitm.ac.in")
    print("="*60)
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        
        for seed in seeds:
            page = None
            try:
                print(f"\n📌 Processing seed {seed}...")
                page = browser.new_page()
                
                url = f"https://sanand0.github.io/tdsdata/js_table/?seed={seed}"
                print(f"   URL: {url}")
                
                # Navigate and wait for network to be idle (JS executed)
                page.goto(url, wait_until="networkidle", timeout=30000)
                
                # Additional wait to ensure table is rendered
                page.wait_for_selector("table", timeout=5000)
                page.wait_for_timeout(2000)  # Extra safety
                
                # Extract numbers from the table
                numbers = page.evaluate('''
                    () => {
                        const nums = [];
                        // Select all table cells
                        const cells = document.querySelectorAll('table td, table th');
                        cells.forEach(cell => {
                            const text = cell.textContent.trim();
                            // Check if it's a number (integer)
                            if (text && /^\d+$/.test(text)) {
                                nums.push(parseInt(text, 10));
                            }
                        });
                        return nums;
                    }
                ''')
                
                if numbers and len(numbers) > 0:
                    seed_sum = sum(numbers)
                    print(f"   ✅ Found {len(numbers)} numbers: {numbers}")
                    print(f"   ✅ Sum for seed {seed}: {seed_sum}")
                    grand_total += seed_sum
                    all_numbers.extend(numbers)
                else:
                    print(f"   ⚠️ No numbers found. Checking page content...")
                    # Debug: check if table exists
                    has_table = page.evaluate('document.querySelector("table") !== null')
                    print(f"   Table exists: {has_table}")
                    
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
            finally:
                if page:
                    page.close()
        
        browser.close()
    
    # Final output
    print("\n" + "="*60)
    print("📊 FINAL RESULTS")
    print("="*60)
    print(f"Total numbers found across all seeds: {len(all_numbers)}")
    print(f"GRAND TOTAL SUM: {grand_total}")
    print("="*60)
    print("23ds3000079@ds.study.iitm.ac.in")
    
    # Save results
    with open('results.txt', 'w') as f:
        f.write(f"Grand Total: {grand_total}\n")
        f.write(f"Total Numbers: {len(all_numbers)}\n")
    
    return grand_total

if __name__ == "__main__":
    scrape_all_seeds()
