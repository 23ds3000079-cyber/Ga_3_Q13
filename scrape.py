from playwright.sync_api import sync_playwright
import time
import sys

def main():
    seeds = [56, 57, 58, 59, 60, 61, 62, 63, 64, 65]
    grand_total = 0
    all_numbers = []
    
    print("="*60)
    print("DataDash QA Automation - 23ds3000079@ds.study.iitm.ac.in")
    print("="*60)
    
    try:
        with sync_playwright() as p:
            # Launch with specific args for GitHub Actions
            browser = p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--disable-setuid-sandbox',
                    '--no-first-run',
                    '--no-zygote',
                    '--single-process'
                ]
            )
            
            for seed in seeds:
                page = None
                try:
                    print(f"\n📌 Processing seed {seed}...")
                    page = browser.new_page()
                    
                    # Navigate to URL
                    url = f"https://data-kw4d.onrender.com/seed{seed}"
                    print(f"   URL: {url}")
                    
                    response = page.goto(url, timeout=30000, wait_until="domcontentloaded")
                    if not response or not response.ok:
                        print(f"   ❌ Failed to load: {response.status if response else 'No response'}")
                        continue
                    
                    # Wait for content
                    page.wait_for_timeout(3000)
                    
                    # Extract numbers
                    numbers = page.evaluate('''
                        () => {
                            const nums = [];
                            // Try multiple selectors
                            document.querySelectorAll('table td, table th, td, th, .data, .number').forEach(el => {
                                const text = el.textContent.trim();
                                if (text && /^\\d+(\\.\\d+)?$/.test(text)) {
                                    nums.push(parseFloat(text));
                                }
                            });
                            return nums;
                        }
                    ''')
                    
                    if numbers:
                        seed_sum = sum(numbers)
                        print(f"   ✅ Found {len(numbers)} numbers: {numbers}")
                        print(f"   ✅ Sum: {seed_sum}")
                        grand_total += seed_sum
                        all_numbers.extend(numbers)
                    else:
                        print(f"   ⚠️ No numbers found")
                    
                except Exception as e:
                    print(f"   ❌ Error: {str(e)}")
                finally:
                    if page:
                        page.close()
            
            browser.close()
        
        # Final output - THIS IS CRITICAL
        print("\n" + "="*60)
        print(f"📊 FINAL RESULTS")
        print("="*60)
        print(f"Total numbers found: {len(all_numbers)}")
        print(f"GRAND TOTAL: {grand_total}")
        print("="*60)
        print("23ds3000079@ds.study.iitm.ac.in")
        
        # Save to file
        with open('results.txt', 'w') as f:
            f.write(f"Grand Total: {grand_total}\n")
            f.write(f"Total Numbers: {len(all_numbers)}\n")
        
        return 0
        
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
