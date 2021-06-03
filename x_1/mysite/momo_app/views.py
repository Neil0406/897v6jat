from django.shortcuts import render ,redirect, HttpResponse
import json
import pandas as pd
from momo_app import data


def index(request):
    all_val, val, val2 = data.momo()
    bank_val = data.bank()
    special_val = data.special()
    limited_val = data.limited()
    
    return render(request,"index.html",locals())

def api(request):

    return render(request,"api.html")

def momo_api(request):

    api_data = pd.read_csv('momo.csv').to_dict('recode')
    return HttpResponse(json.dumps(api_data, ensure_ascii=False),content_type="application/json")