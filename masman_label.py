import requests
import json
import openpyxl
import pythoncom
import win32api
import win32print
import re
from zebra import Zebra
from win32 import win32print
import random
zpl_data = []
readable_data = []

def get_product_price_avail(key, parts, field_list=None, wh=None, cust=None, prices=None):
    '''
    
    
    product = {"product": [{"part": part} for part in parts]}
    fields = {"fields": [{"field": field} for field in field_list]} if field_list else None

    params = {
        "f": "getProductPriceAvail",
        "key": key,
        "product": json.dumps(product),
    }
    
    if fields:
        params["fields"] = json.dumps(fields)
    if wh:
        params["wh"] = wh
    if cust:
        params["cust"] = cust
    if prices:
        params["incexgst"] = prices
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    url = "XXX"  # Get correct URL once completed

    response = requests.post(url, params=params, headers=headers)
    
    if response.status_code == 200:
        #return response.text
        add_to_list(response) # eventually
    else:
        response.raise_for_status()
    '''
    add_to_list(parts[0])


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

def add_to_list(response):  # to do

    ## To be replaced
    ## Testing only
    #part = "B08GWWBVL9-T1"
    #temp_str = "NETGEAR Orbi Whole Home WiFi 6 Tri-Band Mesh System, AX4200 Wireless Speed, Up to 4.2Gbps, 2 Pack, Model RBK752. NB: Turns On, No Further Testing."
    part = response
    temp_str =[
        "LOREM Ipsum Dolor Sit Amet, Consectetur Adipiscing Elit, Sed Do EuisMod Tempor. NB: Faulty, does not power on.",
        "GOURMIA 6.7L Digital Air Fryer , GAF798. NB: Has been used, missing tray accessories.",
        "HOMEDICS Shiatsu Bliss Foot Spa With Heat Boost, White. NB: Has been used, not in original box, missing 1x spinning attachment.",
        "HIDDEN WILD XL Folding Camp Cot, Green, L 200 x W 80 x H 47 cm. NB: Not in box.",
        "MAC SPORTS Extra Large Folding Wagon with Cargo Net, Grey, W 560 x H 200 x D 820 mm. NB: Minor bend on frame, in working order, not in box.",
        "MAC SPORTS Beach Day Lounger Combo Cart. NB: Minor use, not in original packaging."
        ]
    description, nb = parse_description_nb(random.choice(temp_str))
    zpl_data.append(generate_zpl(part, description, nb))
    readable_data.append("{}\n{}\n{}".format(part, description, nb))
    print (zpl_data[0])
    return

def parse_description_nb(full_desc):
    nb_keywords = ["N.B.", "NB:", "N.b:", "N.B:", "NB -"]
    regex_pattern = '|'.join(re.escape(keyword) for keyword in nb_keywords)
    match = re.search(regex_pattern, full_desc, flags=re.IGNORECASE)

    if match:
        description = full_desc[:match.start()].strip()
        nb = "NB: " + full_desc[match.end():].strip()
    else:
        description = description
        nb = ""
    
    return description, nb


def zpl_print():   
    z = Zebra()
    q = z.getqueues()
    z.setqueue(q[0])
    z.setup()
    for label in zpl_data:
        z.output(label)
    

def clear_list():   # to do
    zpl_data.clear()
    readable_data.clear()


if __name__ == "__main__":
    key = "97479037"
    parts = ["CC90935"]
    field_list = []
    wh = ""
    cust = ""
    prices = "X"
    try:
        result = get_product_price_avail(key, parts, field_list, wh, cust, prices) # result = ["code", "description"]
        print(result)
    except Exception as e:
        print("Error:", str(e))