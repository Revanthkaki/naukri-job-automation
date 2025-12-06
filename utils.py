import google.generativeai as genai
import requests
import time
from datetime import datetime
from config import Config

# Configure Gemini API
genai.configure(api_key=Config.GEMINI_API_KEY)

def generate_ai_answer(question):
    """Generate AI answer using Gemini"""
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"You are helping someone answer a job application question professionally. Question: {question}. Provide a professional answer in 2-3 sentences."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"AI answer generation failed: {e}")
        return "I am very interested in this position and believe my skills align well with the requirements."

def solve_captcha(site_key, page_url):
    """Solve CAPTCHA using 2Captcha service"""
    if not Config.TWOCAPTCHA_API_KEY:
        return None
    try:
        print("Solving CAPTCHA...")
        submit_url = "http://2captcha.com/in.php"
        params = {
            'key': Config.TWOCAPTCHA_API_KEY,
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
            check_url = f"http://2captcha.com/res.php?key={Config.TWOCAPTCHA_API_KEY}&action=get&id={captcha_id}&json=1"
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
    """Log errors to file"""
    with open('error.log', 'a') as f:
        f.write(f"{datetime.now().isoformat()} - {message}\n")

def write_stats_to_file(stats):
    """Write statistics to log file"""
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
