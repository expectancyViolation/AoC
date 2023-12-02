import os
from pathlib import Path

import jinja2


def task_template_day():
    def template(year, day):
        templateLoader = jinja2.FileSystemLoader(searchpath="./")
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "template_day.py.j2"
        template = templateEnv.get_template(TEMPLATE_FILE)
        out_path = f"./{year}"
        Path(out_path).mkdir(parents=True, exist_ok=True)
        out_file = os.path.join(out_path, f"day{int(day):02}.py")
        if not os.path.exists(out_file):
            template.stream(year=year, day=day).dump(out_file)

    year_param = {'name': 'year', 'short': 'y', 'default': '2023'}
    day_param = {'name': 'day', 'short': 'd', 'default': '1'}
    return {
        'actions': [template],
        'params': [year_param, day_param],
        "verbosity": 2
    }
