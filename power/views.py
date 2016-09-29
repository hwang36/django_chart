import os
# from django.conf.
from django.shortcuts import render
import datetime
from django.db.models import Avg, Max, Min
from django.http import HttpResponse, HttpResponseRedirect
import csv
import json
import time
import sys
import traceback
# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the power index.")


def view_data(request, request_date):
    # file = "/Users/huawang/django/codetest/data/dataSheet.csv"
    file = "/Users/huawang/Downloads/t1.csv"
    return_json = {}
    # try:
    #     print "--1----------------------"
    #     print request.body
    #     print "------------------------"
    #     mydata = json.loads(str(request.body))
    #     if 'request_date' in mydata and mydata['request_date'] != '':
    #         request_date = mydata['request_date']
    #     print "--2----------------------"
    #     print request_date
    #     print "------------------------"
    # except:
    #     return_json['success'] = False
    #     print sys.exc_info()
    #     traceback.print_exc()
    #
    print "--3----------------------"
    print request_date
    print "------------------------"

    table = {}
    # indices
    device_id_idx_1 = 1
    time_stamp_idx_1 = 2
    kwh_idx_1 = 4
    power_idx_1 = 5
    device_id_idx_2 = 7
    kwh_idx_2 = 10
    power_idx_2 = 11
    kwh_sum_idx = 14
    power_sum_idx = 15

    # handle data from csv file
    with open(file, 'rb') as f:
        reader = csv.reader(f)
        reader.next()
        reader.next()
        for row in reader:
            # parse date out
            raw_date = row[time_stamp_idx_1]
            print (raw_date)
            parsed_date = time.strptime(raw_date, "%Y-%m-%d %H:%M:%S-07:00")
            parsed_date = datetime.datetime(*parsed_date[:6])

            # set table[date] according to the indices
            # date = str(parsed_date.tm_mon) + '-' + str(parsed_date.tm_mday)

            date = parsed_date.strftime("%Y-%m-%d")
            kwh1 = float(row[kwh_idx_1])
            kwh2 = float(row[kwh_idx_2])
            kwh_sum = float(row[kwh_sum_idx])
            hour = parsed_date.hour
            device_id_1 = row[device_id_idx_1]
            device_id_2 = row[device_id_idx_2]
            device_pair = str(device_id_1) + '-' + str(device_id_2)
            if not (date in table):
                table[date] = {}
            if not device_pair in table[date]:
                table[date][device_pair] = {
                    'device_id_1': device_id_1,
                    'device_id_2': device_id_2,
                    'kwh': {},
                    'power': {},
                    'labels': [],
                    'date': date,
                    'statistics': {}
                }
            if not device_id_1 in table[date][device_pair]['kwh']:
                table[date][device_pair]['kwh'][device_id_1] = []
            table[date][device_pair]['kwh'][device_id_1].append(kwh1)
            if not device_id_2 in table[date][device_pair]['kwh']:
                table[date][device_pair]['kwh'][device_id_2] = []
            table[date][device_pair]['kwh'][device_id_2].append(kwh2)
            if not 'kwh_sum' in table[date][device_pair]['kwh']:
                table[date][device_pair]['kwh']['kwh_sum'] = []
            table[date][device_pair]['kwh']['kwh_sum'].append(kwh_sum)
            if not 'categories' in table[date][device_pair]['kwh']:
                table[date][device_pair]['kwh']['categories'] = []
            table[date][device_pair]['kwh']['categories'].append(hour)

        print table

        keys = table.keys()
        keys.sort()
        sorted_dates = keys
        print(sorted_dates)

    # TODO: calculate the real statistics
    return_json['dev1_kwh_ave'] = 0.0
    return_json['dev1_kwh_max'] = 0.0
    return_json['dev1_kwh_min'] = 0.0

    # TODO: sort the dates and use the latest date when request_date is not set
    if request_date not in sorted_dates:
        request_date = sorted_dates[-1]
        response =  HttpResponseRedirect('/power/summary/' + request_date)
        return response

    data_for_request_date = table[request_date]
    data_series = []
    data_categories = []
    for k, v in data_for_request_date.items():
        data_series.append({
            'name': 'Device ' + device_id_1,
            'data': v['kwh'][device_id_1]
        })
        data_series.append({
            'name': 'Device ' + device_id_2,
            'data': v['kwh'][device_id_2]
        })
        data_series.append({
            'name': 'Sum',
            'data': v['kwh']['kwh_sum']
        })
        data_categories = v['kwh']['categories']

    return_json['data_series'] = data_series
    print("-----3--")
    print(data_series)

    # move statistics to be inside table
    device_pairs = data_for_request_date.keys()
    if (len(device_pairs) == 1) :
        device_pair = device_pairs[0]
        (device_id_1, device_id_2) = device_pair.split('-')
        kwhs_d1 = data_for_request_date[device_pairs[0]]['kwh'][device_id_1]
        kwh_ave_d1 = float (sum(kwhs_d1))/max(len(kwhs_d1), 1)
        kwh_min_d1 = min(kwhs_d1)
        kwh_max_d1 = max(kwhs_d1)
        return_json['dev1_kwh_ave'] = round(kwh_ave_d1, 5)
        return_json['dev1_kwh_max'] = round(kwh_max_d1, 5)
        return_json['dev1_kwh_min'] = round(kwh_min_d1, 5)
        return_json['dev1_id'] = device_id_1

        kwhs_d2 = data_for_request_date[device_pairs[0]]['kwh'][device_id_2]
        kwh_ave_d2 = float (sum(kwhs_d2))/max(len(kwhs_d2), 1)
        kwh_min_d2 = min(kwhs_d2)
        kwh_max_d2 = max(kwhs_d2)
        return_json['dev2_kwh_ave'] = round(kwh_ave_d2, 5)
        return_json['dev2_kwh_max'] = round(kwh_max_d2, 5)
        return_json['dev2_kwh_min'] = round(kwh_min_d2, 5)
        return_json['dev2_id'] = device_id_2

    return_json['data_categories'] = data_categories
    return_json['sorted_dates'] = sorted_dates
    return_json['request_date'] = request_date

    return render(request, 'summary.html', return_json)

