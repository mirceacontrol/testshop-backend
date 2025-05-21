Software engeneering test backend app

## Features

- Search for events by keyword, category, date, and address.
- Fetches 5 events each from Ticketmaster (via API) and Eventbrite (via web scraping).
- Displays event name, price, address, and link.

## Requirements

- Python 3.8+
- The following Python packages (install using `pip`):

    ```
    pip install flask python-dotenv requests beautifulsoup4 lxml
    ```

## Environment Setup

1. Create a virtual environment (optional but recommended):

    ```
    python -m venv venv
    ```

    Activate it:

    - **Windows:** `venv\Scripts\activate`

2. Install the required Python packages:

    ```
    pip install flask python-dotenv requests beautifulsoup4 lxml
    ```

3. Set up your `.env` file (in the project root) and add Ticketmaster API key:

    ```
    TICKET_MASTER_KEY=your_ticketmaster_api_key_here
    ```

## Running the App

1. Make sure you are in your project directory and your virtual environment is activated.
2. Start the Flask app:

    ```
    python app.py
    ```

3. Open your browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Notes

- **Eventbrite data is scraped:** Eventbrite uses dynamic HTML and may block or change its layout at any time. The app works as long as their structure does not change significantly.
- Couldn't fetch propper data from Eventbrite