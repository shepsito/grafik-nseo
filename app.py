from flask import Flask, jsonify
from datetime import datetime, timedelta
import calendar
import os

app = Flask(__name__)

# ========== ГЕНЕРИРАНЕ НА ГРАФИК ==========

def get_week_of_month(date):
    first_day = date.replace(day=1)
    first_weekday = first_day.weekday()
    
    if first_weekday == 0:
        first_monday = first_day
    else:
        first_monday = first_day + timedelta(days=(7 - first_weekday))
    
    if date < first_monday:
        return 0
    
    delta_days = (date - first_monday).days
    return (delta_days // 7) + 1

def is_last_monday_of_quarter(date):
    return date.weekday() == 0 and date.month in [3,6,9,12] and calendar.monthrange(date.year,date.month)[1] - date.day < 7

def is_last_tuesday_of_quarter(date):
    return date.weekday() == 1 and date.month in [3,6,9,12] and calendar.monthrange(date.year,date.month)[1] - date.day < 7

def is_last_wednesday_of_quarter(date):
    return date.weekday() == 2 and date.month in [3,6,9,12] and calendar.monthrange(date.year,date.month)[1] - date.day < 7

def is_last_thursday_of_quarter(date):
    return date.weekday() == 3 and date.month in [3,6,9,12] and calendar.monthrange(date.year,date.month)[1] - date.day < 7

def is_last_friday_of_quarter(date):
    return date.weekday() == 4 and date.month in [3,6,9,12] and calendar.monthrange(date.year,date.month)[1] - date.day < 7

def generate_yearly_schedule(year):
    events = []
    current = datetime(year,1,1)
    end = datetime(year,12,31)

    while current <= end:
        day = current.day
        month = current.month
        week = get_week_of_month(current)

        def night_event(title, facility, description):
            return {
                'datetime': current.replace(hour=23, minute=0, second=0, microsecond=0),
                'title': title.strip(),
                'facility': facility,
                'description': description,
                'shift': 'Смяна 1'
            }

        def morning_event(title, facility, description):
            return {
                'datetime': current.replace(hour=7, minute=0, second=0, microsecond=0),
                'title': title.strip(),
                'facility': facility,
                'description': description,
                'shift': 'Смяна 2'
            }

        def afternoon_event(title, facility, description):
            return {
                'datetime': current.replace(hour=15, minute=0, second=0, microsecond=0),
                'title': title.strip(),
                'facility': facility,
                'description': description,
                'shift': 'Смяна 3'
            }

        # --- УСЛОВИЯ ---
        if month in [2,9] and current.weekday()==0 and week==1:
            events.append(afternoon_event('Проверка АВР','Аварийно осветление','Проверка АВР на захранването-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if day in [11,12]:
            events.append(afternoon_event('ЕЕ ЦПС-1','ЕЕ ЦПС-1','Проверка изправноста на аварийно осветление-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if month in [3,10] and current.weekday()==0 and week in [1,2]:
            events.append(morning_event('Ф.И. Проверка','По процедура','Ф.И аварийно осветление-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if day == 15:
            events.append(afternoon_event('МЗ и ЕЕ ЦПС-1','МЗ и ЕЕ ЦПС-1','Проверка евакуационно осветление-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if is_last_monday_of_quarter(current):
            events.append(afternoon_event('Проверка АВР (Пон.)','МЗ,ЦПС-1','Проверка АВР на сборки 0.4кВ захранвани от 3 и 4БН-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if is_last_tuesday_of_quarter(current):
            events.append(afternoon_event('Проверка АВР (Вт.)','МЗ','Проверка АВР на сборки 0.4кВ захранвани от 23 и 24БН-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if is_last_wednesday_of_quarter(current):
            events.append(afternoon_event('Проверка АВР (Ср.)','МЗ','Проверка АВР на сборки 0.4кВ на съответната система I(II,III)-блок3-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if is_last_thursday_of_quarter(current):
            events.append(afternoon_event('Проверка АВР (Четв.)','МЗ','Проверка АВР на сборки 0.4кВ на съответната система I(II,III)-блок4-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if is_last_friday_of_quarter(current):
            events.append(night_event('Проверка АВР (Петък)','МЗ,ХВО и ЦПС-1','Проверка АВР на сборки 0.4кВ/без сборки захр.от 3,4,23,24БН,33I-III,43I-III/-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        # СЕКЦИИ 0,4кВ-ГК - започва в 23:00 на 7-ми, приключва в 07:00 на 8-ми
        if day == 8:
            night_before = current - timedelta(days=1)
            night_before = night_before.replace(hour=23, minute=0, second=0, microsecond=0)
            
            events.append({
                'datetime': night_before,
                'title': 'Секции 0,4кВ-ГК',
                'facility': 'Секции 0,4кВ-ГК',
                'description': 'Проверка АВР na ~ШУ и изправноста на сигнализацията на панел "С"в БЩУ4 за повикване в КРУ-[color=ff0000]ДИС,ОЕОи СКУ[/color]',
                'shift': 'Смяна 1'
            })

        if day == 18:
            events.append(afternoon_event('Вентилни отводи','Вентилни отводи','Отчитане на вентилни отводи-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        # 1-ви ден от месеца - нощна смяна започва в 23:00 на последния ден от предходния месец
        if day == 1:
            night_before = current - timedelta(days=1)
            night_before = night_before.replace(hour=23, minute=0, second=0, microsecond=0)
            
            events.append({
                'datetime': night_before,
                'title': 'Ел.двигатели 6кВ',
                'facility': 'Ел.двигатели 6кВ',
                'description': 'Измерване Riso на ел.двигатели 6кВ-ПВТ в резерв,1 и 2 ПВТ -[color=ff0000]НСЕО,ОЕОи СКУ[/color]',
                'shift': 'Смяна 1'
            })
            events.append(morning_event('Отчитане електромери','Методика','Отчитане показанията на електромерите за консумираната ел.енергия-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if month in [1,4,7,10] and current.weekday()==0 and week==1:
            events.append(morning_event('Проверка ДГ-А','ДГ-А','Ф.И на автономен товар за време ≥60мин-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if month in [1,4,7,10] and current.weekday()==0 and week==2:
            events.append(morning_event('Проверка ДГ-Б','ДГ-Б','Ф.И на автономен товар за време ≥60мин-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if month in [1,4,7,10] and current.weekday()==2 and week==3:
            events.append(morning_event('Проверка 2АДГ-ДСАПП-4','2АДГ-ДСАПП-4','Ф.И аварийно захранване на СПИ-[color=ff0000]НСЕО,ЕнергетикПРАО[/color]'))

        if month in [1,4,7,10] and current.weekday()==3 and week==3:
            events.append(morning_event('Проверка ДГ-КАС','ДГ-КАС','Ф.И аварийно захранване на СПИ-[color=ff0000]НСЕО,ЕнергетикПРАО[/color]'))

        if month in [6,12] and current.weekday()==0 and week==3:
            events.append(morning_event('Проверка ГРТ-ЦНРД','ГРТ-ЦНРД','Изпробване АВР на ел.захранването-[color=ff0000]НСЕО,ЕнергетикПРАО,ДИС[/color]'))

        if current.weekday() == 5 and week == 3:
            events.append(morning_event('Проверка ТП1,ТП3','ТП1,ТП3','Изпробване на охлаждащите вентилатори на 1ТП и 3ТП чрез ръчно включване-[color=ff0000]НСЕО[/color]'))

        if current.weekday() in [2,5] and week == 3:
            events.append(night_event('Измерване стойности по фидери','Методика','Измерване стойностите по фидери за АКС,СБК-2 и ТРЗ/Бюро пропуски -[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))
            events.append(morning_event('Измерване стойности по фидери','Методика','Измерване стойностите по фидери за АКС,СБК-2 и ТРЗ/Бюро пропуски-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))
            events.append(afternoon_event('Измерване стойности по фидери','Методика','Измерване стойностите по фидери за АКС,СБК-2 и ТРЗ/Бюро пропуски-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        current += timedelta(days=1)

    return sorted(events, key=lambda x: x['datetime'])

# ========== ПОМОЩНИ ФУНКЦИИ ==========

def format_bg_datetime(dt):
    """Форматира дата на български"""
    day = dt.day
    months = ["януари","февруари","март","април","май","юни","юли","август","септември","октомври","ноември","декември"]
    month = months[dt.month - 1]
    hours = str(dt.hour).zfill(2)
    minutes = str(dt.minute).zfill(2)
    return f"{day} {month}, {hours}:{minutes}"

def get_events_for_date(events, date):
    """Връща ВСИЧКИ събития за дадена дата"""
    date_events = []
    
    for event in events:
        if event['datetime'].date() == date.date():
            date_events.append(event)
    
    return sorted(date_events, key=lambda x: x['datetime'])

# ========== FLASK РУТОВЕ ==========

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>График НСЕО</title></head>
    <body>
        <h1>📅 График НСЕО</h1>
        <p>API endpoints:</p>
        <ul>
            <li><a href="/api/events/today">/api/events/today</a></li>
            <li><a href="/api/events/next">/api/events/next</a></li>
            <li><a href="/api/events/past">/api/events/past</a></li>
        </ul>
        <p>За да видите графиките, отворете <a href="/static/index.html">/static/index.html</a></p>
    </body>
    </html>
    '''

@app.route('/api/events/today')
def get_today_events():
    """Всички събития за днес (от 00:01 до 23:59)"""
    year = 2026
    events = generate_yearly_schedule(year)
    today = datetime.now()
    
    today_events = get_events_for_date(events, today)
    
    result = []
    for ev in today_events:
        if ev['shift'] == 'Смяна 1':
            dt = ev['datetime']
            next_day = dt + timedelta(days=1)
            months = ["януари","февруари","март","април","май","юни","юли","август","септември","октомври","ноември","декември"]
            month = months[next_day.month - 1]
            formatted_time = f"{next_day.day} {month}, 00:00 🌙 (започва в 23:00 на {dt.day} {months[dt.month - 1]})"
        elif ev['shift'] == 'Смяна 2':
            formatted_time = format_bg_datetime(ev['datetime']) + ' ☀️ (започва в 07:00)'
        elif ev['shift'] == 'Смяна 3':
            formatted_time = format_bg_datetime(ev['datetime']) + ' 🌅 (започва в 15:00)'
        else:
            formatted_time = format_bg_datetime(ev['datetime'])
        
        result.append({
            'title': ev['title'].strip(),
            'datetime': ev['datetime'].isoformat(),
            'formatted_time': formatted_time,
            'shift': ev['shift'],
            'facility': ev['facility'],
            'description': ev['description']
        })
    
    return jsonify(result)

@app.route('/api/events/past')
def get_past_events():
    """Минали събития - приключили"""
    year = 2026
    events = generate_yearly_schedule(year)
    today = datetime.now()
    
    past_events = []
    for ev in events:
        if ev['shift'] == 'Смяна 1':
            end_time = ev['datetime'] + timedelta(hours=8)
        elif ev['shift'] == 'Смяна 2':
            end_time = ev['datetime'] + timedelta(hours=8)
        elif ev['shift'] == 'Смяна 3':
            end_time = ev['datetime'] + timedelta(hours=8)
        else:
            end_time = ev['datetime']
        
        if end_time < today:
            past_events.append(ev)
    
    past_events = past_events[-10:]
    
    result = []
    for ev in past_events:
        if ev['shift'] == 'Смяна 1':
            dt = ev['datetime']
            next_day = dt + timedelta(days=1)
            months = ["януари","февруари","март","април","май","юни","юли","август","септември","октомври","ноември","декември"]
            formatted_time = f"{next_day.day} {months[next_day.month - 1]}, 00:00 🌙 (започва в 23:00 на {dt.day} {months[dt.month - 1]})"
        elif ev['shift'] == 'Смяна 2':
            formatted_time = format_bg_datetime(ev['datetime']) + ' ☀️ (започва в 07:00)'
        elif ev['shift'] == 'Смяна 3':
            formatted_time = format_bg_datetime(ev['datetime']) + ' 🌅 (започва в 15:00)'
        else:
            formatted_time = format_bg_datetime(ev['datetime'])
        
        result.append({
            'title': ev['title'].strip(),
            'datetime': ev['datetime'].isoformat(),
            'formatted_time': formatted_time,
            'shift': ev['shift'],
            'facility': ev['facility'],
            'description': ev['description']
        })
    
    return jsonify(result)

@app.route('/api/events/next')
def get_next_events():
    """Следващи събития"""
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
        if ev['shift'] == 'Смяна 1':
            dt = ev['datetime']
            next_day = dt + timedelta(days=1)
            months = ["януари","февруари","март","април","май","юни","юли","август","септември","октомври","ноември","декември"]
            formatted_time = f"{next_day.day} {months[next_day.month - 1]}, 00:00 🌙 (започва в 23:00 на {dt.day} {months[dt.month - 1]})"
        elif ev['shift'] == 'Смяна 2':
            formatted_time = format_bg_datetime(ev['datetime']) + ' ☀️ (започва в 07:00)'
        elif ev['shift'] == 'Смяна 3':
            formatted_time = format_bg_datetime(ev['datetime']) + ' 🌅 (започва в 15:00)'
        else:
            formatted_time = format_bg_datetime(ev['datetime'])
        
        result.append({
            'title': ev['title'].strip(),
            'datetime': ev['datetime'].isoformat(),
            'formatted_time': formatted_time,
            'shift': ev['shift'],
            'facility': ev['facility'],
            'description': ev['description']
        })
    
    return jsonify(result)

# ========== СТАРТИРАНЕ ==========

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
