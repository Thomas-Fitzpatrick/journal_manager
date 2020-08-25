import os
import glob
from flask import render_template, send_from_directory
from app import app
from shutil import copyfile

path = r"C:\Users\thoma\Desktop\test_journal_DS"
live_files = os.path.join(os.getcwd(), 'app', 'static', 'live_files') + '\\'

@app.route('/')
@app.route('/index')
def year_index():
    years = os.listdir(path)
    return render_template('years.html', years=years)


@app.route('/index/<year>')
def date_index(year):
    dates = os.listdir(os.path.join(path, year))
    return render_template('dates.html', dates=dates, year=year)


@app.route('/index/<year>/<date>')
def entry(year, date):
    entry_dir = os.path.join(path, year, date)
    contents = os.listdir(entry_dir)
    entry_file, entry_content = None, None
    photos = []
    for file in contents:
        if '.jpg' in file:
            photos.append(file)
        elif '.entry' in file:
            entry_file = os.path.join(entry_dir, file)

    for file in glob.glob(os.path.join(live_files, '*')):
        os.remove(file)

    print(entry_file, entry_content)
    if entry_file:
        with open(entry_file, 'r') as f:
            entry_content = f.read()

    for photo in photos:
        copyfile(os.path.join(entry_dir, photo), os.path.join(live_files, photo))

    return render_template('entry.html', photos=photos, entry=entry_content)

