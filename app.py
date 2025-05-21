from flask import Flask, render_template, request, redirect, url_for
import os
import requests
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
TICKET_MASTER_KEY = os.getenv("TICKET_MASTER_KEY")


def get_ticketmaster_events(keyword="", category="", date="", address=""):
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": TICKET_MASTER_KEY,
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

        # Debug output: how many events were found
        print(f"[DEBUG] Found {len(events)} Ticketmaster events.")
        return events
    else:
        print(f"[ERROR] Ticketmaster API failed: {response.status_code}")
        return []


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        category = request.form.get('category')
        date = request.form.get('date')
        address = request.form.get('address')
        keyword = request.form.get('keyword')

        ticketmaster_events = get_ticketmaster_events(keyword, category, date, address)
        return render_template('index.html', events=ticketmaster_events, cart_total=0)
    
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
