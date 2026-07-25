from flask import Flask, jsonify, send_from_directory
from datetime import datetime, timedelta
from service_logic import generate_yearly_schedule

app = Flask(__name__, static_folder="static")

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/api/events/today")
def api_today():
    now = datetime.now()
    today = now.date()
    events = generate_yearly_schedule(now.year)

    today_events = []
    for ev in events:
        d = ev['datetime'].date()

        if d == today:
            today_events.append(ev)
            continue

        if ev['shift'] == "Смяна 1" and d == today - timedelta(days=1) and now.hour < 7:
            today_events.append(ev)
            continue

    return jsonify(today_events)

@app.route("/api/events/next")
def api_next():
    now = datetime.now()
    events = generate_yearly_schedule(now.year)

    future = [e for e in events if e['datetime'] > now]
    future.sort(key=lambda e: e['datetime'])

    return jsonify(future[:10])

if __name__ == "__main__":
    app.run()
