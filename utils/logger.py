from datetime import datetime

def setup_logger():
    pass

def log_error(message):
    with open('error.log', 'a') as f:
        f.write(f"{datetime.now().isoformat()} - {message}\n")

def write_stats_to_file(stats):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('naukri_automation_log.txt', 'a', encoding='utf-8') as f:
        f.write(f"\n{'='*80}\n")
        f.write(f"AUTOMATION LOG - {timestamp}\n")
        f.write(f"{'='*80}\n\n")
        f.write(f"Total Jobs Found: {stats['total_jobs_found']}\n")
        f.write(f"✅ Successfully Applied: {stats['successfully_applied']}\n")
        f.write(f"⏭️ Already Applied: {stats['already_applied']}\n")
        f.write(f"❌ Failed: {stats['failed_applications']}\n")
        f.write(f"🚫 No Apply Button: {stats['no_apply_button']}\n")
        f.write(f"⚠️ Errors: {stats['errors']}\n\n")
        f.write(f"📋 DETAILED JOB STATUS:\n")
        for idx, job in enumerate(stats['jobs_details'], 1):
            f.write(f"\n{idx}. {job['title']}\n")
            f.write(f"   Company: {job.get('company', 'N/A')}\n")
            f.write(f"   Status: {job['status']}\n")
            if job.get('error'):
                f.write(f"   Error: {job['error']}\n")
        f.write(f"\n{'='*80}\n\n")
    print(f"\n📝 Log written to 'naukri_automation_log.txt'")
