# Tweety
Scrape twitter profiles & All user tweets! (no 3200 limit).

# Usage
- Clone the Repo locally.
- Ensure you have all the dependencies in [requirements.txt](/requirements.txt) installed into your py packages.
  _Using a virtual environment is highly prefered_
- Run app.py.
- Choose whether you want to extract Profile data or User's tweets.

## Notes:
- Only X urls are allowed, with no params like **lang=en, or similar params).**
(in future update username will be allowed)
- There's a rate limit of about 800 tweets for the same local IP address, after which X API will send
  a message "Rate Limit Exceeded".
  Proxy will be added for bypassing this limit.
