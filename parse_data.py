from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import csv
import sys
from datetime import datetime, timedelta
from tqdm import tqdm
import math


# Load your original HTML document
with open("Dominion - ══ SUPPORT - 📜｜whitelist-log [731298096373432320].html", "r", encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

# Find all transcript link elements
transcript_links = soup.select('a[href^="https://tickettool.xyz/direct?url="]')

total_transcripts = len(transcript_links)
accepted_transcripts = 0
denied_transcripts = 0
withdrawn_transcripts = 0
last_date = ''

# Prepare the CSV file
with open("applications.csv", "w", newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Date', 'Status', 'Users', 'UUIDs', 'Link', 'Ticket Number', 'Legundo Mentioned']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    # Define Firefox options
    options = Options()

    # Disable CSS
    options.set_preference('permissions.default.stylesheet', 2)

    # Disable images
    options.set_preference('permissions.default.image', 2)

    # Disable Flash
    options.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

    # Initiate the driver with the preferences
    driver = webdriver.Firefox(options=options)

    # Define the initial sleep time
    sleep_time = 3

    # List to store the URLs that caused a CAPTCHA
    captcha_urls = transcript_links.copy()

    # Record start time for calculating ETA
    start_time = datetime.now()

    while captcha_urls:
        for i, link in tqdm(enumerate(captcha_urls), total=len(captcha_urls), ncols=70):
            transcript_url = link['href']
            driver.get(transcript_url)

            # Wait until the "application" text appears on the page
            try:
                element = WebDriverWait(driver, 10).until(
                    lambda driver: "application" in driver.page_source.lower()
                )
                # Decrease the sleep time if page loaded successfully
                sleep_time = max(2, sleep_time - 0.1)
            except TimeoutException:
                captcha_urls.append(transcript_url)
                if "Performance & security by Cloudflare" in driver.page_source:
                    # If there's a CAPTCHA, increase the sleep time
                    sleep_time += 1
                continue

            transcript_soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Attempt to find date
            date_element = transcript_soup.find("span", class_="chatlog__timestamp")
            date = date_element.text if date_element else last_date

            # Update last_date
            last_date = date

            transcript_text = transcript_soup.get_text()

            if "play.dominionserver.net" in transcript_text:
                status = 'Accepted'
                accepted_transcripts += 1
            elif "wish you the best" in transcript_text:
                status = 'Denied'
                denied_transcripts += 1
            else:
                status = 'Withdrawn'
                withdrawn_transcripts += 1

            # Find users in transcript
            user_elements = transcript_soup.find_all("span", class_="chatlog__author-name")
            users = set()
            user_ids = set()
            for user_element in user_elements:
                users.add(user_element.get('title'))
                user_ids.add(user_element.get('data-user-id'))

            # Extract ticket number from title
            title_element = transcript_soup.find("title")
            ticket_number = title_element.text[-4:] if title_element else 'Unknown'

            # Check if Legundo is mentioned
            legundo_mentioned = "legundo" in transcript_text.lower()

            # Write to the CSV file
            writer.writerow({
                'Date': date, 
                'Status': status, 
                'Users': list(users), 
                'UUIDs': list(user_ids), 
                'Link': transcript_url, 
                'Ticket Number': ticket_number,
                'Legundo Mentioned': legundo_mentioned
            })

            # Live update
            # Calculate ETA
            elapsed_time = datetime.now() - start_time
            eta_seconds = elapsed_time / (i + 1) * (total_transcripts - (i + 1))
            eta_seconds = math.floor(eta_seconds.total_seconds() + 0.5)
            eta = timedelta(seconds=eta_seconds)

            # Format the estimated remaining time as hours, minutes, and seconds
            eta_str = str(eta).split('.')[0]

            # Calculate the progress percentage
            progress_percentage = (i + 1) / total_transcripts * 100

            # Print the progress update
            print(f"\rTicket {ticket_number}: {status}.", end='', flush=True)
            print(f"\r{ticket_number}: {status}. Progress: {progress_percentage:.2f}% Processed {i + 1} out of {total_transcripts} applications.", end='', flush=True)
            tqdm.write(f"{ticket_number}: {status}. Accepted: {accepted_transcripts}, Denied: {denied_transcripts}, Withdrawn: {withdrawn_transcripts}")
            sys.stdout.flush()

            try:
                # Remove the processed URL from the CAPTCHA list
                captcha_urls.remove(transcript_url)
            except ValueError:
                # The URL was already removed, do nothing
                pass

            time.sleep(sleep_time)

    driver.quit()  # don't forget to quit the driver at the end!

# Calculate final acceptance rate
acceptance_rate = accepted_transcripts / total_transcripts

print(f"\nFinal acceptance rate: {acceptance_rate * 100}%")
