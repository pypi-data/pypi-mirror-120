from os import environ, startfile
environ['PYTHONINSPECT'] = '1'
from os.path import exists
from tqdm import tqdm
from winsound import Beep
from time import sleep
from math import ceil

work_min = 25
short_break_min = 5
long_break_min = 20
work_color = 'yellow'
break_color = 'green'
work_html = 'pomodoro_work.html'
break_html = 'pomodoro_break.html'

break_sound = [(2000,200),(3000,200),(1000,400)]
work_sound = [(2000,200),(1000,200),(3000,400)]

inc_sec = 1

def pomodoro(
        work_min=work_min,
        short_break_min=short_break_min,
        long_break_min=long_break_min,
        inc_sec=inc_sec,
        do_popup=True,
        do_sound=True,
        ):
    if do_popup:
        if not exists(break_html):
            with open(break_html,'w') as f:
                f.write('''<div style="background: lime;
            font-size: 20px;
            color: black;
            padding: 10px;
            border: 1px solid black;
            margin: 10px;
            text-align: center;">
            Break!
        </div>''')
        if not exists(work_html):
            with open(work_html,'w') as f:
                f.write('''<div style="background: red;
            font-size: 20px;
            color: black;
            padding: 10px;
            border: 1px solid black;
            margin: 10px;
            text-align: center;">
            Work!
        </div>''')

    while True:
        for descr,duration,start_sound,color,html in [
            ('Pomodoro 1',work_min,work_sound,work_color,work_html),
            ('Break 1',short_break_min,break_sound,break_color,break_html),
            ('Pomodoro 2',work_min,work_sound,work_color,work_html),
            ('Break 2',short_break_min,break_sound,break_color,break_html),
            ('Pomodoro 3',work_min,work_sound,work_color,work_html),
            ('Break 3',short_break_min,break_sound,break_color,break_html),
            ('Pomodoro 4',work_min,work_sound,work_color,work_html),
            ('Long Break',long_break_min,break_sound,break_color,break_html),
            ]:
            if do_sound:
                for tone in start_sound:
                    Beep(*tone)
            if do_popup:
                startfile(html)
            for i in tqdm(range(int(ceil(60*duration/inc_sec))),desc=descr,colour=color):
                sleep(inc_sec)
