from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import json

app = Flask(__name__)
CORS(app)

# Тук сложи generate_yearly_schedule() функцията

@app.route('/api/events/today')
def get_today_events():
    """Връща всички активни събития за днес"""
    year = 2026
    events = generate_yearly_schedule(year)
    today = datetime.now()
    
    print(f"\n{'='*60}")
    print(f"📅 ЗАЯВКА ЗА ДНЕС: {today.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    # Вземаме всички събития за днес (включително нощните от вчера)
    today_events = get_events_for_date(events, today)
    
    print(f" Намерени {len(today_events)} активни събития за днес:")
    
    result = []
    for ev in today_events:
        # Показваме детайлно всяко събитие
        print(f"\n  📌 {ev['title']}")
        print(f"     📅 Дата: {ev['datetime'].strftime('%Y-%m-%d')}")
        print(f"     ⏰ Час: {ev['datetime'].strftime('%H:%M')}")  # <-- ТУК ВИЖ ЧАСА
        print(f"     👤 Смяна: {ev['shift']}")
        print(f"     🏢 Обект: {ev['facility']}")
        
        result.append({
            'title': ev['title'].strip(),
            'datetime': ev['datetime'].isoformat(),
            'shift': ev['shift'],
            'facility': ev['facility'],
            'description': ev['description']
        })
    
    print(f"\n📤 JSON отговор:")
    print(json.dumps(result[:3], indent=2, ensure_ascii=False))
    print(f"{'='*60}\n")
    
    return jsonify(result)

@app.route('/api/events/next')
def get_next_events():
    year = 2026
    events = generate_yearly_schedule(year)
    today = datetime.now()
    
    future_events = []
    for ev in events:
        if ev['datetime'] > today:
            future_events.append(ev)
        if len(future_events) >= 30:
            break
    
    result = []
    for ev in future_events[:15]:
        result.append({
            'title': ev['title'].strip(),
            'datetime': ev['datetime'].isoformat(),
            'shift': ev['shift'],
            'facility': ev['facility'],
            'description': ev['description']
        })
    
    return jsonify(result)

@app.route('/api/events/past')
def get_past_events():
    year = 2026
    events = generate_yearly_schedule(year)
    today = datetime.now()
    
    past_events = []
    for ev in events:
        if ev['datetime'] < today:
            past_events.append(ev)
    
    past_events = past_events[-10:]
    
    result = []
    for ev in past_events:
        result.append({
            'title': ev['title'].strip(),
            'datetime': ev['datetime'].isoformat(),
            'shift': ev['shift'],
            'facility': ev['facility'],
            'description': ev['description']
        })
    
    return jsonify(result)

if __name__ == '__main__':
    print("🚀 СТАРТИРАНЕ НА СЪРВЪРА")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
