from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .models import Pool, PoolData


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
    table.pool1_percent = (table.pool1_count/total_clicks)*100
    table.pool2_percent = (table.pool2_count/total_clicks)*100
    table.pool3_percent = (table.pool3_count/total_clicks)*100
    table.pool4_percent = (table.pool4_count/total_clicks)*100
    table.save()
    pass


def calc_user_clicks(btn, table_id, user):
    table = Pool.objects.get(id=table_id)
    check_user = PoolData.objects.get_or_create(user_id=user, pool_id=table)
    print(check_user)
    if not check_user:
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
    if request.method == "POST":
        data = request.POST.get('button')
        table = request.POST.get('pool_table')
        user = request.user
        result = calc_user_clicks(data, table, user)
        print(result, '-------------result')
        return HttpResponseRedirect(reverse('home'))
    else:
        pool_data = Pool.objects.all()
        context = {
            "data": pool_data
        }
    return render(request, 'homepage.html', context)
