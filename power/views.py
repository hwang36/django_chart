from django.shortcuts import render
import datetime
from django.db.models import Avg, Max, Min
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the power index.")


def view_data(request):
    days = 3
    today = datetime.datetime.today()

    # all_device_ids = View_data.objects.all().distinct()
    # one_day_summary = {}
    # devices_summary = {}
    # for x in range(0, days):
    #     day = today + x
    #     all_device_one_day = View_data.objects.all().filter(excel_data = day)
    #     for device_id in all_device_ids:
    #         one_device_data = all_device_one_day.filter(device_id = device_id)
    #         one_device_summary = {}
    #         one_device_summary['max_kwh'] = one_device_data.aggregate(Max('kwh'))
    #         one_device_summary['min_kwh'] = one_device_data.aggregate(Min('kwh'))
    #         one_device_summary['ave_kwh'] = one_device_data.aggregate(Avg('kwh'))
    #         one_device_summary['graphNm'] = device_id + day
    #         devices_summary[device_id] = one_device_summary
    #
    #     one_day_summary[day] = devices_summary

    return_json = {}
    return_json['one_set'] = [3.9, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8]
    return_json['ave'] = 5
    return_json['max'] = 10
    return_json['min'] = 3
    return_json['deviceId'] = '522'

    return render(request, 'summary.html', return_json)

