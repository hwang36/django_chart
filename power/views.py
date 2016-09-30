from django.shortcuts import render
import datetime
from django.http import HttpResponse, HttpResponseRedirect
import csv
import time


def view_data(request, request_date):
    """Entry point of the summary page. It parse the data and get
    the data for a certain day, and send it back to the client.
    :param request: the http request
    :param request_date: date for the data
    :return: the http response
    """
    return_json = {}

    # handle data from csv file and prepare it

    # NOTE: in the real scenario, the file would be in some network share folder
    # or in the cloud.
    # file = "/Users/huawang/django/codetest/data/dataSheet.csv"
    file = "/Users/huawang/Downloads/t1.csv"

    # NOTE: we are reading the whole file when the user is only asking for
    # one day's data. There are two ways to imrprove it:
    # 1. skip a line when it's not for the date being asked
    # 2. use SPA(single page application) style, and the client only
    #    get the whole dataset once.
    table = process_data_file(file)

    print(table)

    # use the latest date as the default date when request_date is not set
    # correctly
    keys = table.keys()
    keys.sort()
    sorted_dates = keys
    if request_date not in sorted_dates:
        request_date = sorted_dates[-1]
        response =  HttpResponseRedirect('/power/summary/' + request_date)
        return response

    # prepare the data to be used in charts
    data_for_request_date = table[request_date]
    data_series = []
    data_categories = []
    data_stats = {}
    device_id_1 = ''
    device_id_2 = ''

    for k, v in data_for_request_date.items():
        device_id_1 = v['device_id_1']
        device_id_2 = v['device_id_2']
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
        data_stats = v['stats']

    return_json['data_series'] = data_series
    return_json['data_stats'] = data_stats
    return_json['device_id_1'] = device_id_1
    return_json['device_id_2'] = device_id_2
    return_json['data_categories'] = data_categories
    return_json['sorted_dates'] = sorted_dates
    return_json['request_date'] = request_date

    return render(request, 'summary.html', return_json)


def calculate_statistics(table):
    for date, pair_dict in table.items():
        # NOTE: we assume that one device only shows up in one device-pair,
        # so we can put the statistics data in the device-pair dict
        for k, v in pair_dict.items():
            v['stats'] = {}
            device_id_1 = v['device_id_1']
            kwhs_1 = v['kwh'][device_id_1]
            v['stats']['device_1_min'] = round(min(kwhs_1), 8)
            v['stats']['device_1_max'] = round(max(kwhs_1), 8)
            v['stats']['device_1_avg'] = round(float (sum(kwhs_1))/max(len(kwhs_1), 1), 8)

            device_id_2 = v['device_id_2']
            kwhs_2 = v['kwh'][device_id_2]
            v['stats']['device_2_min'] = round(min(kwhs_2), 8)
            v['stats']['device_2_max'] = round(max(kwhs_2), 8)
            v['stats']['device_2_avg'] = round(float (sum(kwhs_2))/max(len(kwhs_2), 1), 8)


def process_data_file(file):
    table = {}
    # indices. Because there are duplicated headers, we use indices to locate
    # the fields.
    device_id_idx_1 = 1
    time_stamp_idx_1 = 2
    kwh_idx_1 = 4
    power_idx_1 = 5
    device_id_idx_2 = 7
    kwh_idx_2 = 10
    power_idx_2 = 11
    kwh_sum_idx = 14
    power_sum_idx = 15
    with open(file, 'rb') as f:
        reader = csv.reader(f)
        # skip the top empty row and the header row
        reader.next()
        reader.next()

        for row in reader:
            # parse date out
            raw_date = row[time_stamp_idx_1]
            parsed_date = time.strptime(raw_date, "%Y-%m-%d %H:%M:%S-07:00")
            parsed_date = datetime.datetime(*parsed_date[:6])

            # set table[date] according to the indices
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
                    'date': date
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

    calculate_statistics(table)

    return table


