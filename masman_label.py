import requests
import json
import openpyxl
from zebra import Zebra

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
        ^FO50,50^BY3^BCN,100,Y,N,N^FD{part_number}^FS
        ^CFA,10^FO60,280^A0N,15^FD{description}^FS
        ^CFA,10^FO60,300^A0N,15^FD{NB}^FS
        ^XZ
    """
    return zpl_template.format(part_number=part, description=desc, NB=nb or "")

def get_readable_data():
    return readable_data

def get_zpl_data():
    return zpl_data

def add_to_list(response):  # to do
    #data.append(generate_zpl(part, desc, nb))
    # Parses response to get "part" and "description from response
    # Then adds the zpl data to zpl_data
    # And adds readable data to readable_data as an array ["Part", "Description"]

    ## Testing only
    nb = None
    zpl_data.append(generate_zpl(response, "TestDesc", nb))
    readable_data.append("{} | {} Description".format(response, response))
    return

def zpl_print():   
    # Prints the zpl_data to the connected ZPL printer
    return

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