from datetime import datetime, timedelta
import calendar

def get_week_of_month(date):
    """
    Връща номера на седмицата от месеца (1-5)
    Седмица 1 започва от първия понеделник на месеца
    Дните преди първия понеделник се броят към последната седмица на предходния месец
    """
    first_day = date.replace(day=1)
    first_weekday = first_day.weekday()  # 0=понеделник, 6=неделя
    
    # Намираме първия понеделник от месеца
    if first_weekday == 0:
        first_monday = first_day
    else:
        first_monday = first_day + timedelta(days=(7 - first_weekday))
    
    # Ако датата е преди първия понеделник, връщаме 0 (последна седмица на предходния месец)
    if date < first_monday:
        return 0
    
    # Изчисляваме седмицата спрямо първия понеделник
    delta_days = (date - first_monday).days
    return (delta_days // 7) + 1

def get_week_dates(year, month, week_number):
    """
    Връща началната и крайната дата на дадена седмица от месеца
    week_number: 1-5 (1 = първия пълен понеделник)
    """
    first_day = datetime(year, month, 1)
    first_weekday = first_day.weekday()
    
    # Намираме първия понеделник
    if first_weekday == 0:
        first_monday = first_day
    else:
        first_monday = first_day + timedelta(days=(7 - first_weekday))
    
    # Изчисляваме началната дата на седмицата
    week_start = first_monday + timedelta(weeks=(week_number - 1))
    week_end = week_start + timedelta(days=6)
    
    return week_start, week_end

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

        # Смяна 1 → ВАРИАНТ А → вчера 23:00
        def night_event(title, facility, description):
            return {
                'datetime': (current - timedelta(days=1)).replace(hour=23),
                'title': title,
                'facility': facility,
                'description': description,
                'shift': 'Смяна 1'
            }

        # Смяна 2 → 07:00
        def morning_event(title, facility, description):
            return {
                'datetime': current.replace(hour=7),
                'title': title,
                'facility': facility,
                'description': description,
                'shift': 'Смяна 2'
            }

        # Смяна 3 → 15:00
        def afternoon_event(title, facility, description):
            return {
                'datetime': current.replace(hour=15),
                'title': title,
                'facility': facility,
                'description': description,
                'shift': 'Смяна 3'
            }

        # --- ВСИЧКИ УСЛОВИЯ ---
        # ВНИМАНИЕ: Сега week==1 означава първия пълен понеделник от месеца

        if month in [2,9] and current.weekday()==0 and week==1:
            events.append(afternoon_event(' Проверка АВР','Аварийно осветление','Проверка АВР на захранването-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if day in [11,12]:
            events.append(afternoon_event(' ЕЕ ЦПС-1','ЕЕ ЦПС-1','Проверка изправноста на аварийно осветление-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if month in [3,10] and current.weekday()==0 and week in [1,2]:
            events.append(morning_event(' Ф.И. Проверка','По процедура','Ф.И аварийно осветление-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if day == 15:
            events.append(afternoon_event(' МЗ и ЕЕ ЦПС-1','МЗ и ЕЕ ЦПС-1','Проверка евакуационно осветление-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if is_last_monday_of_quarter(current):
            events.append(afternoon_event(' Проверка АВР (Пон.)','МЗ,ЦПС-1','Проверка АВР на сборки 0.4кВ захранвани от 3 и 4БН-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if is_last_tuesday_of_quarter(current):
            events.append(afternoon_event(' Проверка АВР (Вт.)','МЗ','Проверка АВР на сборки 0.4кВ захранвани от 23 и 24БН-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if is_last_wednesday_of_quarter(current):
            events.append(afternoon_event(' Проверка АВР (Ср.)','МЗ','Проверка АВР на сборки 0.4кВ на съответната система I(II,III)-блок3-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if is_last_thursday_of_quarter(current):
            events.append(afternoon_event(' Проверка АВР (Четв.)','МЗ','Проверка АВР на сборки 0.4кВ на съответната система I(II,III)-блок4-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if is_last_friday_of_quarter(current):
            events.append(night_event(' Проверка АВР (Петък)','МЗ,ХВО и ЦПС-1','Проверка АВР на сборки 0.4кВ/без сборки захр.от 3,4,23,24БН,33I-III,43I-III/-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if day == 8:
            events.append(night_event(' Секции 0,4кВ-ГК','Секции 0,4кВ-ГК','Проверка АВР na ~ШУ и изправноста на сигнализацията на панел "С"в БЩУ4 за повикване в КРУ-[color=ff0000]ДИС,ОЕОи СКУ[/color]'))

        if day == 18:
            events.append(afternoon_event(' Вентилни отводи','Вентилни отводи','Отчитане на вентилни отводи-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if day == 1:
            events.append(night_event(' Ел.двигатели 6кВ','Ел.двигатели 6кВ','Измерване Riso на ел.двигатели 6кВ-ПВТ в резерв,1 и 2 ПВТ -[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))
            events.append(morning_event(' Отчитане електромери','Методика','Отчитане показанията на електромерите за консумираната ел.енергия-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if month in [1,4,7,10] and current.weekday()==0 and week==1:
            events.append(morning_event(' Проверка ДГ-А','ДГ-А','Ф.И на автономен товар за време ≥60мин-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if month in [1,4,7,10] and current.weekday()==0 and week==2:
            events.append(morning_event(' Проверка ДГ-Б','ДГ-Б','Ф.И на автономен товар за време ≥60мин-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if month in [1,4,7,10] and current.weekday()==2 and week==3:
            events.append(morning_event(' Проверка 2АДГ-ДСАПП-4','2АДГ-ДСАПП-4','Ф.И аварийно захранване на СПИ-[color=ff0000]НСЕО,ЕнергетикПРАО[/color]'))

        if month in [1,4,7,10] and current.weekday()==3 and week==3:
            events.append(morning_event(' Проверка ДГ-КАС','ДГ-КАС','Ф.И аварийно захранване на СПИ-[color=ff0000]НСЕО,ЕнергетикПРАО[/color]'))

        if month in [6,12] and current.weekday()==0 and week==3:
            events.append(morning_event(' Проверка ГРТ-ЦНРД','ГРТ-ЦНРД','Изпробване АВР на ел.захранването-[color=ff0000]НСЕО,ЕнергетикПРАО,ДИС[/color]'))

        if current.weekday() == 5 and week == 3:
            events.append(morning_event(' Проверка ТП1,ТП3','ТП1,ТП3','Изпробване на охлаждащите вентилатори на 1ТП и 3ТП чрез ръчно включване-[color=ff0000]НСЕО[/color]'))

        if current.weekday() in [2,5] and week == 3:
            events.append(night_event(' Измерване стойности по фидери','Методика','Измерване стойностите по фидери за АКС,СБК-2 и ТРЗ/Бюро пропуски -[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))
            events.append(morning_event(' Измерване стойности по фидери','Методика','Измерване стойностите по фидери за АКС,СБК-2 и ТРЗ/Бюро пропуски-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))
            events.append(afternoon_event(' Измерване стойности по фидери','Методика','Измерване стойностите по фидери за АКС,СБК-2 и ТРЗ/Бюро пропуски-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        current += timedelta(days=1)

    return sorted(events, key=lambda x: x['datetime'])

# Тест за проверка
if __name__ == "__main__":
    # Показване на всички седмици за юли 2026
    print("Седмици за юли 2026:")
    print("=" * 50)
    for w in range(0, 6):
        if w == 0:
            start, end = get_week_dates(2026, 6, 5)  # последната седмица на юни
            print(f"Седмица 0 (от юни): {start.strftime('%d.%m')} - {end.strftime('%d.%m')}")
        else:
            start, end = get_week_dates(2026, 7, w)
            print(f"Седмица {w}: {start.strftime('%d.%m')} - {end.strftime('%d.%m')}")
    
    print("\n" + "=" * 50)
    
    # Тест за конкретни дати
    test_dates = [
        datetime(2026, 7, 1),
        datetime(2026, 7, 6),
        datetime(2026, 7, 12),
        datetime(2026, 7, 13),
        datetime(2026, 7, 19),
        datetime(2026, 7, 26),
    ]
    
    print("\nСедмици за конкретни дати:")
    for date in test_dates:
        week = get_week_of_month(date)
        print(f"{date.strftime('%d.%m.%Y')} ({date.strftime('%A')}) → седмица {week}")
    
    # Генериране на графика за 2026
    events = generate_yearly_schedule(2026)
    
    # Показване на събитията за днес
    today = datetime(2026, 7, 26)
    today_events = [e for e in events if e['datetime'].date() == today.date()]
    print(f"\nСъбития за {today.strftime('%d.%m.%Y')}:")
    print("=" * 50)
    if today_events:
        for ev in today_events:
            print(f"  {ev['title']}")
            print(f"  {ev['shift']} - {ev['facility']}")
            print(f"  {ev['description']}")
            print("-" * 30)
    else:
        print("  Няма събития за днес")
