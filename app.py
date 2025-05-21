from flask import Flask, render_template, request
import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup

app = Flask(__name__)

load_dotenv()
TICKETMASTER_API_KEY = os.getenv("TICKET_MASTER_KEY")


def get_ticketmaster_events(keyword="", category="", date="", address=""):
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": TICKETMASTER_API_KEY,
        "keyword": keyword,
        "size": 5
    }
    if category:
        params["classificationName"] = category
    if date:
        params["startDateTime"] = date
    if address:
        params["city"] = address

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        events = []
        for item in data.get('_embedded', {}).get('events', []):
            events.append({
                "url": item.get('url'),
                "price": "N/A (Ticketmaster)",
                "address": item.get('_embedded', {}).get('venues', [{}])[0].get('address', {}).get('line1', 'N/A'),
                "description": item.get('name')
            })

        print(f"[DEBUG] Found {len(events)} Ticketmaster events.")
        return events[:5]
    else:
        print(f"[ERROR] Ticketmaster API failed: {response.status_code}")
        return []


def get_eventbrite_events(keyword=""):
    events = []
    seen_links = set()

    try:
        search_term = keyword.replace(" ", "-") if keyword else "all-events"
        url = f"https://www.eventbrite.com/d/online/{search_term}/"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"[ERROR] Eventbrite HTTP error {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "lxml")
        cards = soup.select('a.event-card-link')[:10]  # Fetch more to allow filtering

        for card in cards:
            href = card.get("href", "")
            if not href.startswith("http"):
                href = "https://eventbrite.com" + href

            if href in seen_links:
                continue
            seen_links.add(href)

            title_tag = card.find("h3")
            price_tag = card.find_next("p")
            price_text = price_tag.text.strip() if price_tag and "$" in price_tag.text else "Free"

            events.append({
                "url": href,
                "description": title_tag.text.strip() if title_tag else "No title",
                "price": price_text,
                "address": "Online"
            })

            if len(events) >= 5:
                break

        with open("debug_eventbrite.html", "w", encoding="utf-8") as f:
            f.write(response.text)

        print(f"[DEBUG] Extracted {len(events)} unique Eventbrite events.")
        return events

    except Exception as e:
        print(f"[ERROR] Static Eventbrite scraping failed: {e}")
        return []


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        category = request.form.get('category')
        date = request.form.get('date')
        address = request.form.get('address')
        keyword = request.form.get('keyword')

        ticketmaster_events = get_ticketmaster_events(keyword, category, date, address)
        eventbrite_events = get_eventbrite_events(keyword)

        all_events = ticketmaster_events + eventbrite_events
        return render_template('index.html', events=all_events, cart_total=0)
    return render_template('index.html', events=[], cart_total=0)


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/fail')
def failed():
    return render_template('fail.html')


if __name__ == '__main__':
    print("Flask app starting...")
    app.run(debug=True)
