# ❓ Frequently Asked Questions

## General Questions

### Q: Is this legal?
**A:** Automation may violate Naukri's terms of service. Use at your own risk for educational purposes only.

### Q: Will my account get banned?
**A:** Possible if detected. The bot uses stealth mode to reduce risk, but there's no guarantee.

### Q: How many jobs can I apply to per day?
**A:** Start with 20-30 per day. Too many may trigger detection.

### Q: Do I need to pay for anything?
**A:** Gemini API is free (with limits). 2Captcha is optional (~$3/1000 captchas).

## Technical Questions

### Q: ChromeDriver version mismatch?
**A:** Use `webdriver-manager` - it handles this automatically.

### Q: What Python version do I need?
**A:** Python 3.8 or higher.

### Q: Can I run this on a server?
**A:** Yes, but you'll need a virtual display (Xvfb on Linux).

### Q: How do I run headless?
**A:** Add `chrome_options.add_argument('--headless')` in `setup_driver()`

### Q: Does it work on Windows?
**A:** Yes, tested on Windows 10/11.

## Configuration Questions

### Q: How do I change job search?
**A:** Edit the URL in `search_and_apply_jobs()` function.

### Q: Can I apply to multiple job types?
**A:** Yes, modify the script to loop through different search queries.

### Q: How do I increase wait time?
**A:** Change `random.randint(5, 10)` to higher values like `random.randint(10, 20)`.

## Troubleshooting

### Q: Bot stops after login?
**A:** Check if Naukri changed their website structure. May need script updates.

### Q: AI answers don't make sense?
**A:** Modify the prompt in `generate_ai_answer()` function.

### Q: CAPTCHA not solving?
**A:** Ensure 2Captcha API key is valid and account has credits.

### Q: No jobs found?
**A:** Check your search query URL is correct.

### Q: Browser won't close?
**A:** Force quit: `ps aux | grep chrome` then `kill -9 [PID]`

## Performance Questions

### Q: How fast does it apply?
**A:** ~5-7 minutes per job (with delays to appear human).

### Q: Can I speed it up?
**A:** Yes, but risks detection. Reduce `random_delay()` values carefully.

### Q: How much RAM does it use?
**A:** ~500MB for Python + Chrome combined.

### Q: Will it work on Raspberry Pi?
**A:** Possible but slow. Minimum 2GB RAM recommended.

## Error Messages

### Q: "Access Denied"
**A:** Your IP may be blocked. Try VPN or wait 30 minutes.

### Q: "Element not found"
**A:** Naukri's website changed. Script needs updating.

### Q: "Invalid API key"
**A:** Check Gemini API key is correct and active.

### Q: "Session expired"
**A:** Login timeout. Bot will retry automatically.

## Best Practices

### Q: Should I run this overnight?
**A:** Not recommended. Run during business hours for 2-3 hours max.

### Q: How often should I check logs?
**A:** Check daily to monitor success rate.

### Q: Should I modify AI answers?
**A:** Yes, customize prompts to match your style.

### Q: Can I run multiple instances?
**A:** Not recommended - risks account ban.

## Advanced

### Q: Can I add LinkedIn support?
**A:** Possible with modifications to the script.

### Q: How do I add email notifications?
**A:** Use Python's `smtplib` to send emails after each cycle.

### Q: Can I use different AI models?
**A:** Yes, modify `generate_ai_answer()` to use OpenAI, Claude, etc.

### Q: How do I add more logging?
**A:** Use Python's `logging` module for detailed logs.

## Still Have Questions?

Open an issue on [GitHub](https://github.com/yourusername/naukri-job-automation/issues)
