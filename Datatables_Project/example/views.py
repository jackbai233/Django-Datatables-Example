import json
import random

from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from example.models import User


def index(request):
    return render(request, 'example/index.html')


def initial_database(request):
    """
    初始化数据库表user
    :param request:
    :return:
    """
    f_values = open('names.log', 'r', encoding='utf-8')

    for value in f_values:
        value = value.strip()
        if not value:
            continue
        age = random.randint(10, 25)
        user = User.objects.filter(name=value).first()
        if not user:
            user = User(name=value, age=age)
            user.save()

    f_values.close()
    return HttpResponse('initial database successfully')


def get_basic_tables(request):
    """
    创建基本的DataTables表格
    """
    user_list = []
    for user_info in User.objects.all():
        user_list.append({
            'name': user_info.name,
            'age': user_info.age
        })

    return render(request, 'example/basic_tables.html', {
        'users': user_list
    })


def use_ajax_tables(request):
    """
    ajax例子的DataTables模版
    :param request:
    :return:
    """
    return render(request, 'example/ajax_tables.html', )


def request_ajax(request):
    """
    处理ajax的例子中的post请求
    :param request:
    :return:
    """
    try:
        if request.method == "POST":
            # print(request.POST)
            #  获取到前端页面ajax传递过来的age
            age = int(request.POST.get('age', 22))

            user_list = []
            for user_info in User.objects.filter(age=age):
                user_list.append({
                    'name': user_info.name,
                    'age': user_info.age
                })

            # 主要是将数据库查询到的数据转化为json形式返回给前端
            return HttpResponse(json.dumps(user_list), content_type="application/json")
        else:
            return HttpResponse(f'非法请求方式')
    except Exception as e:
        return HttpResponse(e.args)


def slice_in_backend_tables(request):
    """
    在后端进行分页的例子
    :param request:
    :return:
    """
    return render(request, 'example/backend_tables.html')


# 暂时跳过csrf的保护
@csrf_exempt
def request_backend(request):
    """
    处理后端分页例子中的post请求
    :param request:
    :return:
    """
    try:
        if request.method == "POST":
            # 获取翻页后该页要展示多少条数据。默认为10；此时要是不清楚dataTables的ajax的post返回值
            # 可以打印一下看看print(request.POST)
            page_length = int(request.POST.get('iDisplayLength', '10'))
            # 该字典将转化为json格式的数据返回给前端，字典中的key默认的名字不能变
            rest = {
                "iTotalRecords": page_length,  # 本次加载记录数量
            }
            # 获取传递过来的该页的起始位置，第一页的起始位置为0.
            page_start = int(request.POST.get('iDisplayStart', '0'))
            # 该页的结束位置则就是"开始的值 + 该页的长度"
            page_end = page_start + page_length
            # 开始查询数据库，只请求这两个位置之间的数据

            users = User.objects.all()[page_start:page_end]
            total_length = User.objects.all().count()

            user_list = []
            for user_info in users:
                user_list.append({
                    'name': user_info.name,
                    'age': user_info.age
                })
            # print(start, ":", length, ":", draw)
            # 此时的key名字就是aaData，不能变
            rest['aaData'] = user_list
            # 总记录数量
            rest['iTotalDisplayRecords'] = total_length
            return HttpResponse(json.dumps(rest), content_type="application/json")
        else:
            return HttpResponse(f'非法请求方式')
    except Exception as e:
        return HttpResponse(e.args)
