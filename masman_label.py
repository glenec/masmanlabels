import requests
import json
import openpyxl
import pythoncom
import win32api
import win32print
import re
import config
from zebra import Zebra
from win32 import win32print

zpl_data = []
readable_data = []

# to build:
# python3 -m  PyInstaller --onefile --noconsole --collect-data sv_ttk run.py 

def get_product_price_avail(parts):
    
    url = config.url
    payload = 'f=getProductPriceAvail&key={}&product=%7B%22product%22%3A%5B%7B%22part%22%3A%22{}%22%7D%5D%7D&fields=%7B%22fields%22%3A%5B%7B%22field%22%3A%22descr%22%7D%5D%7D&wh=&cust=&incexgst=X'.format(config.apikey, parts[0])
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    
    if response.status_code == 200:
        return add_to_list(response.text)
    else:
        response.raise_for_status()


def generate_zpl(part, desc, nb=None):
    zpl_template = """
        ^XA
        ^FO30,60^BY3^BCN,100,N,N,N,A^FD{part_number}^FS
        ^CFA,10^FO30,180^A0N,60^FD{part_number}^FS
        ^CFA,10^FO30,280^A0N,30^FD{description}^FS
        ^CFA,10^FO30,315^A0N,30^FD{NB}^FS
        ^XZ
    """
    return zpl_template.format(part_number=part, description=desc, NB=nb or "")

def get_readable_data():
    return readable_data

def get_zpl_data():
    return zpl_data

def add_to_list(response): 
    response_dict = json.loads(response)
    part = response_dict["Product"][0]["Part"]
    descr = response_dict["Product"][0]["descr"]
    valid_part = response_dict["Product"][0]["ValidPart"]
    if valid_part == "False":
        return False

    description, nb = parse_description_nb(descr)
    zpl_data.append(generate_zpl(part, description, nb))
    readable_data.append("{}\n{}\n{}".format(part, description, nb))
    return True

def parse_description_nb(full_desc):

    nb_keywords = ["N.B.", "NB:", "N.b:", "N.B:", "NB -"]
    regex_pattern = '|'.join(re.escape(keyword) for keyword in nb_keywords)
    match = re.search(regex_pattern, full_desc, flags=re.IGNORECASE)

    if match:
        description = full_desc[:match.start()].strip()
        nb = "NB: " + full_desc[match.end():].strip()
    else:
        description = full_desc
        nb = ""

    return description, nb


def zpl_print():   
    z = Zebra(config.printerName)
    q = z.getqueues()
    z.setqueue(q[0])
    z.setup()
    for label in zpl_data:
        z.output(label)
    

def clear_list():
    zpl_data.clear()
    readable_data.clear()


if __name__ == "__main__":
    parts = ["cc90935"]
    try:
        result = get_product_price_avail(parts) 
        print(result)
    except Exception as e:
        print("Error:", str(e))