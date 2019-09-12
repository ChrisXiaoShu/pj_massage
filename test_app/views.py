from datetime import datetime, timedelta, timezone
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
import pytz
from test_app.models import Customer, Reservation, Master, MasterGroup
from test_app.google_calendar import CalendarManager


# Create your views here.

@csrf_exempt #to disable the CSRF restrict
def post_reservation(request):
    if request.method =="POST" :
        status = "POST"
    
    master_id = request.POST.get('master_id', 'default_mid')
    dt_str = request.POST.get('dt', 'default_time')
    line_id = request.POST.get('line_id', 'default_lineid')
    name = request.POST.get('name', 'default_name')
    phone = request.POST.get('phone', 'default_phone')

    m = Master.objects.get(master_id=master_id)
    c, created = Customer.objects.get_or_create(
        line_id=line_id,
        defaults={'name': name, 'phone': phone},
    )
    dt = datetime.strptime(dt_str, '%Y%m%d%H%M')

    dt.replace(tzinfo=pytz.timezone('Asia/Taipei'))
    obj, created = Reservation.objects.get_or_create(
        master=m,
        datetime=dt,
        defaults={'customer': c, 'name': name, 'phone': phone},
    )

    if created:
        CM = CalendarManager()
        event = CM.write_event(m.master_id, dt, (name + phone))
        if event:
            obj, created = Reservation.objects.update_or_create(
                master=m,
                datetime=dt,
                defaults={'event_id': event['id']},
            )                 
            return JsonResponse({'status':'success' , 
                                'info' : {'master' : m.master_id, 
                                        'line_id' : line_id, 
                                        'datetime' : dt_str, 
                                        'name' : name,
                                        'phone' : phone,
                                        'reservation_id' : obj.id,
                                        'event_id' : event['id']}
                                })
    return JsonResponse({'status':'fail', 'info' : {}})
    # result = {'status' : 'success or fail', 
    #         'info' : {'master' : 'master_id_name', 
    #                 'line_id' : 'line_id', 
    #                 'datetime' : 'datetime_str', 
    #                 'name' : 'reservation_name',
    #                 'phone' : 'phone_number',
    #                 'reservation_id' : 'reservation_id_number'}
    #         }

def get_reservation(request):
    if request.method =="GET" :
        status = "GET"

    line_id = request.GET.get('line_id', 'default_id')
    c = Customer.objects.get(line_id = line_id)
    r = Reservation.objects.filter(customer = c)

    tztaipei = timezone(timedelta(seconds=28800))
    infos = []
    for item in r:
        infos.append({'master' : item.master.name,
                    'line_id' : item.customer.line_id, 
                    'datetime' : item.datetime.astimezone(tztaipei).strftime('%Y%m%d%H%M'), 
                    'name' : item.name,
                    'phone' : item.phone,
                    'reservation_id' : item.id})


    result = {'status' : len(infos), #'reservation_numbers', 
            'infos' : infos}
    return JsonResponse(result)

def delete_reservation(request):
    if request.method =="GET" :
        status = "GET"  

    r_id = request.GET.get('reservation_id', 'default_id')
    r = Reservation.objects.get(id=r_id)
    status = 'fail'
    except_type = ''

    try :
        CM = CalendarManager()
        delete_result = CM.delete_event(r.master.master_id, r.event_id)
    except Exception as e:
        except_type = str(type(e))
    else:
        try:
            Reservation.objects.filter(id=r_id).delete()
        except Exception as e:
            except_type = str(type(e))
        else:
            status = 'success'
    finally:
        result = {'status' : status,
                'info' : {'master' : r.master.master_id, 
                        'line_id' : r.customer.line_id, 
                        'datetime' : r.datetime, 
                        'name' : r.name,
                        'phone' : r.phone,
                        'reservation_id' : r.id,
                        'exception' : except_type
                    }
                }
    return JsonResponse(result)

def get_freetime(request):
    if request.method =="GET" :
        status = "GET"    

    d_interval = timedelta(days=2)
    d_delay = timedelta(days=0)
    d_worktime = timedelta(hours=1)
    tztaipei = timezone(timedelta(seconds=28800))

    d_starttime = datetime.now().astimezone(tztaipei).replace(hour=8, minute=0, second=0, microsecond=0) + d_delay
    #d_starttime = datetime(2019, 9, 1, 8, 0, tzinfo=tztaipei) + d_delay
    d_endtime = d_starttime + d_interval
    even_worktime_set = set()
    odd_worktime_set = set()
    while d_starttime < d_endtime:
        for i in range(10):
            if i % 2:
                tmp = d_starttime + d_worktime*i
                odd_worktime_set.add(tmp)                
            else:
                tmp = d_starttime + d_worktime*i
                if tmp.hour != 12:
                    even_worktime_set.add(tmp)
        d_starttime += timedelta(days=1)

    d_starttime = datetime.now().astimezone(tztaipei).replace(hour=8, minute=0, second=0, microsecond=0) + d_delay
    #d_starttime = datetime(2019, 9, 1, 8, 0, tzinfo=tztaipei) + d_delay
    d_endtime = d_starttime + d_interval

    group_name = request.GET.get('group_name', 'A')
    g = MasterGroup.objects.get(name=group_name)
    m_list = Master.objects.filter(group=g)
    m_id = [ m.master_id for m in m_list ]
    m_name = [m.name for m in m_list]
    m_id_name = dict(zip(m_id,m_name))

    CM = CalendarManager()
    busy_result = CM.get_busy(d_starttime, d_endtime, *m_id)

    free_result = {}
    for m in m_list:
        if m.work_type == 1:
            free_result[m.master_id] = odd_worktime_set - busy_result[m.master_id]
        else:
            free_result[m.master_id] = even_worktime_set - busy_result[m.master_id]

    all_worktime_set  = odd_worktime_set | even_worktime_set
    info_result = []
    for t in all_worktime_set:
        for key, value in free_result.items():
            if t in value:
                info_result.append({ 'master_id' : key, 'master_name' : m_id_name[key], 'datetime' : t.strftime('%Y%m%d%H%M')})

    info_result = sorted(info_result, key = lambda x : x['datetime'])

    result = {'status' : 'success',
            "infos" : info_result}
    # result = {'status' : 'success or fail', 
    #         'infos' : [{'master' : 'master_id_name',  
    #                 'datetime' : 'datetime_str'} 
    #                 ,{}]
    #         }
    return JsonResponse(result)

#post {status : "" , info : {reservation info}}
#get {status : "reservation number ", "infos" : [{id:'id', name:'nmae', ph, reservation id},{},{}]
#delet {status : "bool" }
#freetime get : {status : '', infos : [{'mid':'mid, 'date': dt },{'mid':'mid', 'date' : dt.str}, order by date]

def get_customer(request):
    if request.method =="GET" :
        status = "GET"

    line_id = request.GET.get('line_id', 'default_id')
    status = 'fail'    
    try:
        c = Customer.objects.get(line_id = line_id)
    except Exception as e:
        info = {'exception' : str(type(e))}
    else:
        status = 'seccess'
        info = {'line_id' : line_id,
                'name' : c.name,
                'phone' : c.phone,
                'is_black' : c.is_black}
    finally:
        result = {'status' : status,
                'info' : info}
        
    return JsonResponse(result)

@csrf_exempt #to disable the CSRF restrict
def post_customer(request):
    if request.method =="POST" :
        status = "POST"
        
    line_id = request.POST.get('line_id', 'default_lineid')
    name = request.POST.get('name', 'default_name')
    phone = request.POST.get('phone', 'default_phone')
    
    obj, created = Customer.objects.get_or_create(
        line_id=line_id,
        defaults={'name': name, 'phone': phone},
    )
    
    if created:
        status = 'success'
    else:
        status = 'fail'
        
    result = {'status' : status, 
              'info' : {'line_id' : obj.line_id,
                        'name' : obj.name, 
                        'phone' : obj.phone,
                        'is_black' : obj.is_black}
             }
    return JsonResponse(result)

def get_group(request):
    if request.method =="GET" :
        status = "GET"
    g_queryset = MasterGroup.objects.all()
    infos = []
    for g in g_queryset:
        tmp = { 'group' : g.name,
                'descript' : g.descript,
                'image' : g.image}
        infos.append(tmp)
     
    result = {'status' : 'success',
              'infos' : infos}
    return JsonResponse(result)
