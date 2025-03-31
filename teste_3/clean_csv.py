import os
import re


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
CLEANED_PREFIX = "cleaned_"

csvs = [i for i in os.listdir(os.path.join(BASE_DIR, "downloads")) if i.endswith(".csv") and not CLEANED_PREFIX in i]

def set_default_value(row):
    changed = False
    for k in range(len(row)):
        if not row[k]:
            row[k] = '"NULL"'
            changed = True
    return row, changed

def clean_csv(filename, replace=False):
    path = os.path.join(BASE_DIR, "downloads", filename)
    cleaned_lines = []
    header = True
    columns = -1
    dirty = 0
    with open(path, encoding="utf-8") as file:
        for line in file:
            line = line.rstrip()
            if header:
                columns = len(line.split(";"))
                header = False
            
            row = line.split(";")
            row, changed = set_default_value(row)
            for i, e in enumerate(row):
                if not (e.startswith('"') and e.endswith('"')):
                    e = e.replace('"', '')
                    row[i] = f'"{e}"'
                    changed = True
                
                # match = re.match(r'"?\d{4}-\d{2}-\d{2}', e)
                # if match:
                #     e = e.replace('"', '')
                #     e = e.replace("'", '')
                #     e = "\"'"+e+"'\""
                #     row[i] = e
                #     changed = True

                if re.match(r'"?-?\d+,\d', e):
                    e = e.replace(",", ".")
                    row[i] = e
                    changed = True
                
                if re.match(r'"?\d{2}/\d{2}/\d{4}', e):
                    e = e.replace('"', '')
                    d,m,y = e.split("/")
                    ymd = "-".join([y,m,d])
                    e = '"'+ymd+'"'
                    row[i] = e
                    changed = True


            cleaned_lines.append(";".join(row))
            if changed:
                dirty+=1

    if dirty > 0:
        if not replace:
            filename = CLEANED_PREFIX+filename
        path = os.path.join(BASE_DIR, "downloads", filename)
        text = "\n".join(cleaned_lines)
        with open(path, "w", encoding="utf-8") as file:
            file.write(text)
            file.close()
    print(f"File {filename} cleaned with {dirty} rows rejected!")
    # print(row)

for csv in csvs[::-1]:
    clean_csv(csv)
