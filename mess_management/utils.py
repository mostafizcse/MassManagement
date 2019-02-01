from django.utils.timezone import datetime

today = datetime.now().date().day

def next_day():
    next_date = today + 1
