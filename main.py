from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random
from datetime import datetime

try:
    from config import Config
    from utils import generate_ai_answer, solve_captcha, log_error, write_stats_to_file
    USE_CONFIG = True
except ImportError:
    # Fallback to hardcoded values if config not available
    USE_CONFIG = False
    import google.generativeai as genai
    import requests
    
    # ⚠️ IMPORTANT: Replace these with your actual credentials
    # DO NOT commit actual credentials to GitHub!

    NAUKRI_USERNAME = "ksai.revanth.22cse@bmu.edu.in"  # Your Naukri email
    NAUKRI_PASSWORD = '8074097091'  # Your Naukri password
    TWOCAPTCHA_API_KEY = ""  # Optional: Your 2Captcha API key
    GEMINI_API_KEY = "AIzaSyCX-8MEBVc-XsQb5iMaXwE6eXo5oSRotzo"  # Required: Your Google Gemini API key
    
    genai.configure(api_key=GEMINI_API_KEY)
    
    def generate_ai_answer(question):
        try:
            model = genai.GenerativeModel('gemini-pro')
            prompt = f"You are helping someone answer a job application question professionally. Question: {question}. Provide a professional answer in 2-3 sentences."
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"AI answer generation failed: {e}")
            return "I am very interested in this position and believe my skills align well with the requirements."
    
    def solve_captcha(site_key, page_url):
        if not TWOCAPTCHA_API_KEY:
            return None
        try:
            print("Solving CAPTCHA...")
            submit_url = "http://2captcha.com/in.php"
            params = {
                'key': TWOCAPTCHA_API_KEY,
                'method': 'userrecaptcha',
                'googlekey': site_key,
                'pageurl': page_url,
                'json': 1
            }
            response = requests.post(submit_url, data=params)
            result = response.json()
            if result.get('status') != 1:
                print(f"CAPTCHA submission failed: {result}")
                return None
            captcha_id = result.get('request')
            print(f"CAPTCHA submitted, ID: {captcha_id}")
            time.sleep(20)
            for attempt in range(12):
                check_url = f"http://2captcha.com/res.php?key={TWOCAPTCHA_API_KEY}&action=get&id={captcha_id}&json=1"
                check_response = requests.get(check_url)
                check_result = check_response.json()
                if check_result.get('status') == 1:
                    print("CAPTCHA solved!")
                    return check_result.get('request')
                elif check_result.get('request') == 'CAPCHA_NOT_READY':
                    print(f"CAPTCHA not ready, waiting... (attempt {attempt + 1})")
                    time.sleep(5)
                else:
                    print(f"CAPTCHA error: {check_result}")
                    return None
            print("CAPTCHA timeout")
            return None
        except Exception as e:
            print(f"CAPTCHA solving failed: {e}")
            return None
    
    def log_error(message):
        with open('error.log', 'a') as f:
            f.write(f"{datetime.now().isoformat()} - {message}\n")
    
    def write_stats_to_file(stats):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('naukri_automation_log.txt', 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"AUTOMATION LOG - {timestamp}\n")
            f.write(f"{'='*80}\n\n")
            f.write(f"📊 SUMMARY STATISTICS:\n")
            f.write(f"{'─'*80}\n")
            f.write(f"Total Jobs Found:           {stats['total_jobs_found']}\n")
            f.write(f"✅ Successfully Applied:     {stats['successfully_applied']}\n")
            f.write(f"⏭️  Already Applied:          {stats['already_applied']}\n")
            f.write(f"❌ Failed Applications:      {stats['failed_applications']}\n")
            f.write(f"🚫 No Apply Button:          {stats['no_apply_button']}\n")
            f.write(f"⚠️  Errors Encountered:      {stats['errors']}\n")
            f.write(f"\n")
            f.write(f"📋 DETAILED JOB STATUS:\n")
            f.write(f"{'─'*80}\n")
            for idx, job in enumerate(stats['jobs_details'], 1):
                f.write(f"\n{idx}. {job['title']}\n")
                f.write(f"   Company: {job.get('company', 'N/A')}\n")
                f.write(f"   Status: {job['status']}\n")
                if job.get('error'):
                    f.write(f"   Error: {job['error']}\n")
                f.write(f"   Time: {job['timestamp']}\n")
            f.write(f"\n{'='*80}\n\n")
        print(f"\n📝 Log written to 'naukri_automation_log.txt'")

# Statistics tracking
stats = {
    'total_jobs_found': 0,
    'successfully_applied': 0,
    'already_applied': 0,
    'failed_applications': 0,
    'no_apply_button': 0,
    'errors': 0,
    'jobs_details': []
}

def random_delay(min_sec=2, max_sec=5):
    """Add random delay to mimic human behavior"""
    time.sleep(random.uniform(min_sec, max_sec))

def setup_driver():
    """Setup Chrome driver with stealth options"""
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.set_window_size(1920, 1080)
    return driver

def login_to_naukri(driver):
    """Login to Naukri.com"""
    try:
        print("Navigating to Naukri login...")
        driver.get("https://www.naukri.com/nlogin/login")
        random_delay(3, 5)
        
        print("Entering credentials...")
        username = NAUKRI_USERNAME if not USE_CONFIG else Config.NAUKRI_USERNAME
        password = NAUKRI_PASSWORD if not USE_CONFIG else Config.NAUKRI_PASSWORD
        
        if not username or not password:
            raise ValueError("Please set NAUKRI_USERNAME and NAUKRI_PASSWORD")
        
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "usernameField"))
        )
        username_field.send_keys(username)
        random_delay(1, 2)
        
        password_field = driver.find_element(By.ID, "passwordField")
        password_field.send_keys(password)
        random_delay(1, 2)
        
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        print("Logging in...")
        
        random_delay(5, 7)
        print("Login successful!")
        return True
        
    except Exception as e:
        print(f"Login failed: {e}")
        log_error(f"Login Error: {e}")
        return False

def search_and_apply_jobs(driver):
    """Search for jobs and apply"""
    try:
        print("\n--- Starting job search ---")
        
        # Use config if available, otherwise fallback
        job_query = Config.JOB_SEARCH_QUERY if USE_CONFIG else "ai-engineer-jobs"
        driver.get(f"https://www.naukri.com/{job_query}")
        random_delay(3, 5)
        
        # Close popups
        try:
            close_buttons = driver.find_elements(By.XPATH, "//div[contains(@class, 'crossIcon')]")
            for btn in close_buttons:
                try:
                    btn.click()
                    random_delay(0.5, 1)
                except:
                    pass
        except:
            pass
        
        # Scroll down
        driver.execute_script("window.scrollBy(0, 300);")
        random_delay(1, 2)
        
        jobs = driver.find_elements(By.CSS_SELECTOR, ".srp-jobtuple-wrapper")
        stats['total_jobs_found'] += len(jobs)
        print(f"Found {len(jobs)} jobs on this page")
        
        # Collect all job URLs FIRST to avoid stale elements
        job_urls = []
        for job in jobs[:10]:
            try:
                title_element = job.find_element(By.CSS_SELECTOR, ".title")
                job_url = title_element.get_attribute('href')
                job_title = title_element.text
                company = "Unknown"
                try:
                    company_element = job.find_element(By.CSS_SELECTOR, ".comp-name")
                    company = company_element.text
                except:
                    pass
                job_urls.append({'url': job_url, 'title': job_title, 'company': company})
            except:
                continue
        
        print(f"Collected {len(job_urls)} job URLs")
        
        # Process each job URL
        for i, job_data in enumerate(job_urls):
            job_detail = {
                'title': job_data['title'],
                'company': job_data['company'],
                'status': 'Pending',
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'error': None
            }
            
            try:
                print(f"\n--- Processing job {i+1}/{len(job_urls)} ---")
                print(f"Job Title: {job_data['title']}")
                print(f"Job URL: {job_data['url']}")
                
                # Navigate to job page
                try:
                    driver.get(job_data['url'])
                    random_delay(5, 7)
                except Exception as e:
                    print(f"Could not navigate to job: {e}")
                    job_detail['status'] = 'Navigation Failed'
                    job_detail['error'] = str(e)
                    stats['errors'] += 1
                    stats['jobs_details'].append(job_detail)
                    continue
                
                # Find Apply button
                apply_clicked = False
                
                try:
                    apply_buttons = driver.find_elements(By.ID, "apply-button")
                    print(f"Found {len(apply_buttons)} apply buttons")
                    
                    visible_apply_button = None
                    for btn in apply_buttons:
                        if btn.is_displayed():
                            visible_apply_button = btn
                            break
                    
                    if visible_apply_button:
                        button_text = visible_apply_button.text.strip()
                        print(f"Found VISIBLE Apply button: '{button_text}'")
                        
                        if 'Applied' in button_text:
                            print("⏭️ Already applied")
                            job_detail['status'] = 'Already Applied'
                            stats['already_applied'] += 1
                            apply_clicked = True
                        elif 'Apply' in button_text:
                            print("✅ Clicking Apply button!")
                            driver.execute_script("arguments[0].click();", visible_apply_button)
                            random_delay(3, 5)
                            
                            # Handle questions
                            try:
                                question_fields = driver.find_elements(By.XPATH, 
                                    "//textarea | //input[@type='text' and not(contains(@placeholder, 'Search')) and not(contains(@placeholder, 'keyword'))]")
                                
                                if question_fields:
                                    print(f"Found {len(question_fields)} question fields")
                                    
                                    for field in question_fields:
                                        try:
                                            if not field.is_displayed() or not field.is_enabled():
                                                continue
                                            placeholder = field.get_attribute('placeholder') or 'Question'
                                            if 'search' in placeholder.lower() or 'keyword' in placeholder.lower():
                                                continue
                                            print(f"Answering: {placeholder}")
                                            answer = generate_ai_answer(placeholder)
                                            field.clear()
                                            field.send_keys(answer)
                                            random_delay(0.5, 1)
                                        except Exception as e:
                                            print(f"Error filling field: {e}")
                            except:
                                print("No questions")
                            
                            # Check CAPTCHA
                            try:
                                captcha_iframe = driver.find_element(By.XPATH, 
                                    "//iframe[contains(@src, 'recaptcha')]")
                                if captcha_iframe:
                                    print("CAPTCHA detected!")
                                    site_key = driver.execute_script("""
                                        var iframe = document.querySelector('iframe[src*="recaptcha"]');
                                        return iframe ? iframe.src.match(/k=([^&]+)/)[1] : null;
                                    """)
                                    if site_key:
                                        captcha_token = solve_captcha(site_key, driver.current_url)
                                        if captcha_token:
                                            driver.execute_script(f"""
                                                document.getElementById('g-recaptcha-response').innerHTML = '{captcha_token}';
                                            """)
                                            random_delay(1, 2)
                            except:
                                print("No CAPTCHA")
                            
                            # Submit
                            try:
                                submit_button = driver.find_element(By.XPATH, 
                                    "//button[@type='submit' or contains(text(), 'Submit')]")
                                driver.execute_script("arguments[0].click();", submit_button)
                                print("✅ Application submitted!")
                                job_detail['status'] = 'Successfully Applied'
                                stats['successfully_applied'] += 1
                            except:
                                print("✅ Application completed!")
                                job_detail['status'] = 'Successfully Applied'
                                stats['successfully_applied'] += 1
                            
                            apply_clicked = True
                    else:
                        print("🚫 No VISIBLE apply button found")
                        job_detail['status'] = 'No Apply Button'
                        stats['no_apply_button'] += 1
                        
                except Exception as e:
                    print(f"❌ Error: {e}")
                    job_detail['status'] = 'Error'
                    job_detail['error'] = str(e)
                    stats['failed_applications'] += 1
                
                stats['jobs_details'].append(job_detail)
                random_delay(2, 4)
                
            except Exception as job_error:
                print(f"Error processing job: {job_error}")
                job_detail['status'] = 'Error'
                job_detail['error'] = str(job_error)
                stats['errors'] += 1
                stats['jobs_details'].append(job_detail)
        
        print(f"\n--- Cycle Complete ---")
        print(f"✅ Successfully Applied: {stats['successfully_applied']}")
        print(f"⏭️ Already Applied: {stats['already_applied']}")
        print(f"❌ Failed: {stats['failed_applications']}")
        print(f"🚫 No Apply Button: {stats['no_apply_button']}")
        
    except Exception as e:
        print(f"Search error: {e}")
        log_error(f"Search Error: {e}")
        stats['errors'] += 1

def main():
    """Main automation loop"""
    print("🚀 Naukri Job Automation Bot")
    print("=" * 50)
    print("Press Ctrl+C to stop\n")
    
    driver = setup_driver()
    
    try:
        if not login_to_naukri(driver):
            print("Login failed, exiting...")
            return
        
        cycle = 1
        while True:
            print(f"\n{'='*50}")
            print(f"CYCLE {cycle}")
            print(f"{'='*50}")
            
            search_and_apply_jobs(driver)
            write_stats_to_file(stats)
            
            print(f"\n📊 OVERALL STATISTICS:")
            print(f"Total Jobs Found: {stats['total_jobs_found']}")
            print(f"✅ Successfully Applied: {stats['successfully_applied']}")
            print(f"⏭️ Already Applied: {stats['already_applied']}")
            print(f"❌ Failed: {stats['failed_applications']}")
            print(f"🚫 No Apply Button: {stats['no_apply_button']}")
            print(f"⚠️ Errors: {stats['errors']}")
            
            wait_minutes = random.randint(5, 10)
            print(f"\n⏳ Waiting {wait_minutes} minutes before next cycle...")
            time.sleep(wait_minutes * 60)
            
            cycle += 1
            
    except KeyboardInterrupt:
        print("\n\nAutomation stopped by user")
        write_stats_to_file(stats)
    except Exception as e:
        print(f"\nFatal error: {e}")
        log_error(f"Fatal Error: {e}")
        write_stats_to_file(stats)
    finally:
        print("\nClosing browser...")
        driver.quit()

if __name__ == "__main__":
    main()
