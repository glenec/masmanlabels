import requests
import json
import openpyxl

data = []

def get_product_price_avail(key, parts, field_list=None, wh=None, cust=None, prices=None):
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
        return response.text
    else:
        response.raise_for_status()


def parse_response():   # to do
    return

def add_to_list():  # to do
    return

def save_and_print():   # to do
    return

def clear_list(data):   # to do
    data = []


if __name__ == "__main__":

    try:
        key = "97479037"
        parts = ["CC90935"]
        field_list = []
        wh = ""
        cust = ""
        prices = "X"
        data = []
        result = get_product_price_avail(key, parts, field_list, wh, cust, prices) # result = ["code", "description"]
        data.append(result)
        save_and_print()
        print(result)

        clear_list()

    except Exception as e:
        print("Error:", str(e))