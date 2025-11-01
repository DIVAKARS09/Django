from django.shortcuts import render
from datetime import datetime
from dateutil.relativedelta import relativedelta

def index(request):
    result = None

    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%I:%M") 
    current_period = datetime.now().strftime("%p")  

    from_date = ''
    from_time = ''
    from_period = 'AM'

    to_date = current_date
    to_time = current_time
    to_period = current_period

    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        from_time = request.POST.get('from_time')
        from_period = request.POST.get('from_period')
        to_date = request.POST.get('to_date')
        to_time = request.POST.get('to_time')
        to_period = request.POST.get('to_period')

        from_hour, from_minute = map(int, from_time.split(':'))
        to_hour, to_minute = map(int, to_time.split(':'))

        if from_period == 'PM' and from_hour != 12:
            from_hour += 12
        if from_period == 'AM' and from_hour == 12:
            from_hour = 0
        if to_period == 'PM' and to_hour != 12:
            to_hour += 12
        if to_period == 'AM' and to_hour == 12:
            to_hour = 0

        from_dt = datetime.fromisoformat(f"{from_date}T{from_hour:02d}:{from_minute:02d}")
        to_dt = datetime.fromisoformat(f"{to_date}T{to_hour:02d}:{to_minute:02d}")

        if to_dt >= from_dt:
            diff = relativedelta(to_dt, from_dt) #it shows the difference in the years,months and days

            # these show the differece in the hour,minutes
            total_seconds = int((to_dt - from_dt).total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60

            result = {
                'years': diff.years,
                'months': diff.months,
                'days': diff.days,
                'hours': hours,
                'minutes': minutes,
            }

    context = {
        'result': result,
        'from_date': from_date,
        'from_time': from_time,
        'from_period': from_period,
        'to_date': to_date,
        'to_time': to_time,
        'to_period': to_period
    }
    return render(request, 'index.html', context)
