from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from Main.models import Metric

def daily_count(request):
    startDate = request.GET.get('startDate', '')
    endDate = request.GET.get('endDate', '')
    data = []
    for item in Metric.summary.daily_count(startDate, endDate):
        data.append({'date': item.date, 'focus': item.focus, 'comment': item.comment})
    return HttpResponse(simplejson.dumps(data), 'application/javascript')
