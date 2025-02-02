
LOG = True
LOG_FILE = "commit_bot.log"
OUTPUT_FILE = "commit_bot.txt"

# Enhanced commit options
BASE_COMMIT_CHANCE = 0.85  # Base chance to make any commits
MIN_COMMITS = 0
MAX_COMMITS = 15
MEAN_COMMITS = 5
STD_DEV = 2.5

# Time randomization
MAX_DELAY_MINUTES = 240  # 4 hour window for commit times

# Commit message variety
COMMIT_MESSAGES = [
    "Update documentation",
    "Refactor code",
    "Fix typo",
    "Add new feature",
    "Optimize performance",
    "Merge branch",
    "Update dependencies",
    "Code cleanup",
    "Fix formatting",
    "Tweak configuration"
]

# Weekend behavior modifiers
WEEKEND_COMMIT_FACTOR = 0.6
WEEKEND_SKIP_INCREMENT = 0.15

# Import enhanced modules
from sys import argv
from pathlib import Path
from os import system
from random import gauss, choice, random, randint
from datetime import datetime, timedelta
import time

# Improved cron setup
def setup_cron():
    system("crontab -l > cron.txt")
    with open("cron.txt", "r") as f:
        if "commit_bot.py" not in f.read():
            with open("cron.txt", "a") as f:
                # Randomize daily execution within 4-hour window
                hour = randint(8, 11)
                minute = randint(0, 59)
                f.write(f"{minute} {hour} * * * cd {Path.cwd()} && python3 commit_bot.py\n")
                f.close()
                system("crontab cron.txt")
        system("rm -f cron.txt")

# Natural commit distribution
def get_commit_count():
    today = datetime.today()
    # Reduce activity on weekends
    if today.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
        base = max(MEAN_COMMITS * WEEKEND_COMMIT_FACTOR, 1)
    else:
        base = MEAN_COMMITS
        
    commits = round(gauss(base, STD_DEV))
    return max(MIN_COMMITS, min(commits, MAX_COMMITS))

# Randomized commit timing
def random_commit_delay():
    delay = randint(0, MAX_DELAY_MINUTES * 60)
    time.sleep(delay)

# Human-like commit messages
def create_commit():
    with open(OUTPUT_FILE, "w") as f:
        f.write(str(datetime.now()))
        f.close()
    system(f"git add {OUTPUT_FILE}")
    message = choice(COMMIT_MESSAGES)
    system(f'git commit -m "{message}"')

# Dynamic activity probability
def should_commit():
    today = datetime.today()
    skip_chance = 1 - BASE_COMMIT_CHANCE
    
    # Increase skip chance on weekends
    if today.weekday() >= 5:
        skip_chance += WEEKEND_SKIP_INCREMENT
    
    # Random weekly variation
    if randint(1, 7) == 1:  # 1/7 chance of "busy day"
        skip_chance += 0.25
        
    return random() > skip_chance

# Enhanced logging
def log(message):
    if LOG:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] {message}\n")

# Main execution flow
if __name__ == "__main__":
    setup_cron()
    
    if should_commit():
        random_commit_delay()
        commits = get_commit_count()
        
        # Create multiple commits with random intervals
        for _ in range(commits):
            create_commit()
            time.sleep(randint(60, 3600))  # 1-60 minutes between commits
            
        system("git push")
        log(f"Committed {commits} times with natural pattern")
    else:
        log("No commits today - natural activity variation")