from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .models import Pool, PoolData
import plotly
from plotly import __version__
import chart_studio.plotly as py
import plotly.graph_objs as go
import numpy as np
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

# for pdf generation
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os


# Create your views here.

def user_login(request):
    if request.method == "POST":
        data = AuthenticationForm(request=request, data=request.POST)
        if data.is_valid():
            uname = data.cleaned_data['username']
            upass = data.cleaned_data['password']
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully')
                return redirect('home')
    else:
        fm = AuthenticationForm()
        context = {
            "fm": fm
        }
    return render(request, 'loginpage.html', context)


def calc_user_percent(table_id):
    table = Pool.objects.get(id=table_id)
    total_clicks = table.pool1_count + table.pool2_count + table.pool3_count + table.pool4_count
    print(total_clicks, " total clicks")
    if total_clicks == 0:
        total_clicks = 1
    print(total_clicks, " total clicks2")
    table.pool1_percent = (table.pool1_count / total_clicks) * 100
    table.pool2_percent = (table.pool2_count / total_clicks) * 100
    table.pool3_percent = (table.pool3_count / total_clicks) * 100
    table.pool4_percent = (table.pool4_count / total_clicks) * 100
    table.save()
    # -----------------
    # groups = [table.pool1_name, table.pool2_name, table.pool3_name, table.pool4_name]
    # amount = [table.pool1_percent, table.pool2_percent, table.pool3_percent, table.pool4_percent]
    # colors = ['#DE3163', '#6495ED', '#DFFF00', '#800080']
    # trace = go.Pie(labels=groups, values=amount,
    #                hoverinfo='label+percent', textinfo='value',
    #                textfont=dict(size=25),
    #                marker=dict(colors=colors, line=dict(color='#000000', width=3)))
    # i = iplot([trace])
    # print(trace)


def calc_user_clicks(btn, table_id, user):
    print(btn, table_id, user)
    table = Pool.objects.get(id=table_id)
    check_user, is_created = PoolData.objects.get_or_create(user_id=user, pool_id=table)

    print(check_user, is_created, 'outside if')
    # is_created is a boolean. True if created, False if it is fetched
    if is_created:
        print(check_user, 'inside if')
        if str(btn) == "btn-1":
            table.pool1_count = table.pool1_count + 1
            table.save()
        elif str(btn) == "btn-2":
            table.pool2_count = table.pool2_count + 1
            table.save()
        elif str(btn) == "btn-3":
            table.pool3_count = table.pool3_count + 1
            table.save()
        elif str(btn) == "btn-4":
            table.pool4_count = table.pool4_count + 1
            table.save()
    else:
        print("User Exists----", check_user)
    calc_user_percent(table_id)
    return btn, table_id


def homepage(request):
    a_float = 10.147593

    print(round(a_float, 2))
    print(__version__, 'PLOTLY Version')
    if request.method == "POST":
        data = request.POST.get('button')
        table = request.POST.get('pool_table')
        user = request.user
        print(data, table, user)
        result = calc_user_clicks(data, table, user)
        print(result, '-------------result')
        return HttpResponseRedirect(reverse('home'))
    else:
        pool_data = Pool.objects.all()
        context = {
            "data": pool_data
        }
    return render(request, 'homepage.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


def pdf_conversion(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    print(html, 'HTML__________________')
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def download_pool(request, pk):
    print(pk, "ID HERE")
    data = Pool.objects.get(id=pk)
    print(data)
    context = {
        "data": data,
    }
    pdf = pdf_conversion('dwld-pools.html', context)
    print(pdf)
    # return render(request, 'dwld-pools.html', context)
    return HttpResponse(pdf, content_type='application/pdf')
