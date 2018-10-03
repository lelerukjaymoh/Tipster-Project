import datetime
from datetime import timedelta

from django.shortcuts import render, get_object_or_404
# from collections import Counter
from .models import Prono
from .cashbetting import CashBet
from .zulubet import ZuluBet


def topnavselector():
    date = datetime.datetime.now()

    return date

#
# def wallet(request):
#     from_date = request.POST.get('From')
#     to_date = request.POST.get('To')
#     submitbutton = request.POST.get('Submit')
#     from_date2 = ""
#     to_date2 = ""
#     try:
#         from_date2 = datetime.datetime.strptime(from_date, "%m/%d/%Y")
#     except:
#         pass
#     try:
#         to_date2 = datetime.datetime.strptime(to_date, "%m/%d/%Y")
#     except:
#         pass
#     progress_details = {}
#     try:
#         while from_date2 != to_date2 + timedelta(days=1):
#             res = requests.get(
#                 'http://www.zulubet.com/tips-0%d-%d-%d.html' % (from_date2.day, from_date2.month, from_date2.year))
#             formatted_date = from_date2.strftime("%d-%m")
#             progress_details = dict(Counter(progress_details) + Counter(parser(res, formatted_date)[1]))
#
#             from_date2 = from_date2 + timedelta(days=1)
#     except:
#         pass
#
#     confirm = {'from_date': from_date, 'to_date': to_date,
#                'submitbutton': submitbutton}
#
#     return render(request, 'mysite/wallet.html', {"progress": progress_details, "confirm": confirm})


def homepage_today(request):
    today = topnavselector()
    res = 'http://www.zulubet.com/tips-0%d-%d-%d.html' % (today.day, today.month, today.year)
    match_date = today.strftime("%d-%m")  # date when the match is played
    games = ZuluBet(res, match_date).zulu_procedure()
    request_from = "tod"
    return render(request, 'mysite/index.html',
                  {"games": games, "request_tom": request_from})


def yesterday(request):
    today = topnavselector() - timedelta(days=1)
    print(today)
    res = 'http://www.zulubet.com/tips-0%d-%d-%d.html' % (today.day, today.month, today.year)
    match_date = today.strftime("%d-%m")  # date when the match is played
    games = ZuluBet(res, match_date).zulu_procedure()
    request_from = "yest"
    return render(request, 'mysite/index.html',
                  {"games": games, "request_tom": request_from})


def tomorrow(request):
    today = topnavselector() + timedelta(days=1)
    res = 'http://www.zulubet.com/tips-0%d-%d-%d.html' % (today.day, today.month, today.year)
    match_date = today.strftime("%d-%m")  # date when the match is played
    games = ZuluBet(res, match_date).zulu_procedure()
    request_from = "tom"
    return render(request, 'mysite/index.html', {"games": games, "request_tom": request_from })


def featured(request):
    today = topnavselector()
    page_url = 'http://cashbettingtips.blogspot.com/%d/%d/0%d-october.html' % (today.year, today.month, 2)
    # match_date = today.strftime("%d-%m")  # date when the match is played
    games_dict = CashBet(page_url).procedure1()
    request_from = "tod"
    return render(request, 'mysite/featured.html', {"games": games_dict, "request_tom": request_from})


def game_details(request, pk):
    games_detail = get_object_or_404(Prono, pk=pk)
    return render(request, 'mysite/game_details.html', {'game': games_detail})
# no risk no reward


def comingsoon(request):
    return render(request, 'mysite/comingsoon.html')


def login(request):
    return render(request, 'mysite/login.html')


def error_404(request):
    data = {}
    return render(request, 'mysite/error_404.html', {'data': data})


def error_500(request):
    data = {}
    return render(request, 'mysite/error_505.html', {'data': data})
