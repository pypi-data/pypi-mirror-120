from os import environ, startfile, remove
environ['PYTHONINSPECT'] = '1'
from os.path import exists
from tqdm import tqdm
from winsound import Beep
from time import sleep
from math import ceil
from tempfile import NamedTemporaryFile

work_min = 25
short_break_min = 5
long_break_min = 20
work_color = 'yellow'
break_color = 'green'

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
    break_html = None
    work_html = None
    if do_popup:
        break_html = NamedTemporaryFile('w',delete=False,suffix='.html')
        with break_html as f:
            f.write('''<div style="background: lime;
            font-size: 20px;
            color: black;
            padding: 10px;
            border: 1px solid black;
            margin: 10px;
            text-align: center;">
            Break!
        </div>''')
        work_html = NamedTemporaryFile('w',delete=False,suffix='.html')
        with work_html as f:
            f.write('''<div style="background: yellow;
            font-size: 20px;
            color: black;
            padding: 10px;
            border: 1px solid black;
            margin: 10px;
            text-align: center;">
            Work!
        </div>''')
    try:

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
                    startfile(html.name)
                for i in tqdm(range(int(ceil(60*duration/inc_sec))),desc=descr,colour=color):
                    sleep(inc_sec)
    finally:
        if work_html is not None:
            remove(work_html.name)
        if break_html is not None:
            remove(break_html.name)
