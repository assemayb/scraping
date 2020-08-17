import os
import sys
import datetime
import requests
from requests_html import HTML
import pandas as pd

BASE_DIR = os.path.dirname(__file__)


SITE_URL = "https://www.boxofficemojo.com/year/world"

def data_to_text_or_save(url, save=False):
    now = datetime.datetime.now()
    year = now.year
    # filename = f"world-{year}.html"
    r = requests.get(url)
    if r.status_code == 200:
        html_text = r.text
        if save:
            with open(f"world-{year}.html", "w") as f:
                f.write(html_text)
        return html_text
    return None


def parse_and_extract(url, name="2020"):
    r_txt = data_to_text_or_save(url)
    if r_txt is None:
        return False

    r_html = HTML(html=r_txt)
    table_class = ".imdb-scroll-table"
    table = r_html.find(table_class)
    table_data = []
    table_header_names = []
    if len(table) == 1:
        table_rows = table[0].find("tr")  # a list
        header_row = table_rows[0]
        header_cols = header_row.find("th")
        table_header_names = [x.text for x in header_cols]
        table_header_names[1] = "Movie Title"

        for row in table_rows[1:]:
            cols = row.find("td")
            row_data = []
            for i, col in enumerate(cols):
                row_data.append(col.text)
            table_data.append(row_data)

    df = pd.DataFrame(table_data, columns=table_header_names)
    path = os.path.join(BASE_DIR, 'data')
    os.makedirs(path, exist_ok=True)
    filepath = os.path.join('data', f"{name}.csv")
    df.to_csv(filepath, index=False)
    return True


def run(start_year, years_ago):
    if start_year == None:
        now = datetime.datetime.now()
        start_year = now.year

    assert isinstance(start_year, int)
    assert len(f"{start_year}") == 4
    assert isinstance(years_ago, int)
    print(start_year)
    for i in range(0, years_ago + 1):
        url = f"https://www.boxofficemojo.com/year/world/{start_year}/"
        finished = parse_and_extract(url, name=start_year)
        if finished:
            print("--------------->")
            print(f"{start_year} Finished")
        else:
            print(f"{start_year} not finished")
        start_year -= 1


if __name__ == "__main__":
    try:
        start = int(sys.argv[1])
    except:
        start = None
    try:    
        count = int(sys.argv[2])
    except:
        count = 0
    run(start_year=start, years_ago=count)
