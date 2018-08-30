import datetime
import re
from datetime import timedelta

import bs4
import requests
from django.shortcuts import render, get_object_or_404
from collections import Counter
from .models import Prono, Progress


def topnavselector():
    date = datetime.datetime.now()
    return date


def wallet(request):
    from_date = request.POST.get('From')
    to_date = request.POST.get('To')
    submitbutton = request.POST.get('Submit')
    from_date2 = ""
    to_date2 = ""
    try:
        from_date2 = datetime.datetime.strptime(from_date, "%m/%d/%Y")
    except:
        pass
    try:
        to_date2 = datetime.datetime.strptime(to_date, "%m/%d/%Y")
    except:
        pass
    progress_details = {}
    try:
        while from_date2 != to_date2 + timedelta(days=1):
            res = requests.get(
                'http://www.zulubet.com/tips-%d-0%d-%d.html' % (from_date2.day, from_date2.month, from_date2.year))
            formatted_date = from_date2.strftime("%d-%m")
            progress_details = dict(Counter(progress_details) + Counter(parser(res, formatted_date)[1]))

            from_date2 = from_date2 + timedelta(days=1)
    except:
        pass

    confirm = {'from_date': from_date, 'to_date': to_date,
               'submitbutton': submitbutton}

    return render(request, 'mysite/wallet.html', {"progress": progress_details, "confirm": confirm})


def homepage_today(request):
    today = topnavselector()
    res = requests.get('http://www.zulubet.com/tips-%d-0%d-%d.html' % (today.day, today.month, today.year))
    match_date = today.strftime("%d-%m")  # date when the match is played
    games = parser(res, match_date)[0]
    progress_details = parser(res, match_date)[1]
    request_from = "tod"
    return render(request, 'mysite/index.html',
                  {"games": games, "request_tom": request_from, "progress": progress_details})


def yesterday(request):
    today = topnavselector() - timedelta(days=1)
    res = requests.get('http://www.zulubet.com/tips-%d-0%d-%d.html' % (today.day, today.month, today.year))
    match_date = today.strftime("%d-%m")  # date when the match is played
    games = parser(res, match_date)[0]
    progress_details = parser(res, match_date)[1]
    request_from = "yest"
    return render(request, 'mysite/index.html',
                  {"games": games, "request_tom": request_from, "progress": progress_details})


def tomorrow(request):
    today = topnavselector() + timedelta(days=1)
    res = requests.get('http://www.zulubet.com/tips-%d-0%d-%d.html' % (today.day, today.month, today.year))
    match_date = today.strftime("%d-%m")  # date when the match is played
    games = parser(res, match_date)[0]
    progress_details = parser(res, match_date)[1]
    request_from = "tom"
    return render(request, 'mysite/index.html', {"games": games, "request_tom": request_from,
                                                 "progress": progress_details})


def parser(res, match_date):
    total_straight_lose = 0
    total_straight_win = 0
    counter_lost_odd = 0.0
    counter_won_odd = 0.0
    counter_win = 0
    profit = 0
    counter_lose = 0
    context = {}
    try:
        res.raise_for_status()

    except Exception as error:
        print('There was a problem getting web data: %s' % error)

    zulu_soup = bs4.BeautifulSoup(res.content, 'html.parser')

    if type(zulu_soup) == bs4.BeautifulSoup:
        tr_elems = zulu_soup.findAll("tr", bgcolor=re.compile('^#.*'))
        games_number = len(tr_elems)
        error_games = []
        removing_mf_usertime = re.compile(r'^mf_usertime(.*);')

        for gameNo in range(games_number):
            team = removing_mf_usertime.sub('', tr_elems[gameNo].getText())
            groupings_trial = re.compile(r'''(
        \d+-\d+,\s)                                                       #date
        (\d+:\d+\s)                                                       #time
        ([\w+\W+]*(\s\w+)*\s-\s\w+[^1:]*)              #teams
        ([\d+]*[\s\w+]*1:\s+\d+%)*   #1
        (X:\s+\d+%)*   #X
        (2:\s+\d+%)*   #2
        (\d+%\d+%\d+%)   #
        (12|1X|1|2|X2|X)      #chance
        (\d[^1:])*
        ([1:\s\d+.\d+]+[^X:]*)  #prob1
        (X:\s\d+.\d{2})         #probX
        (2:\s\d+.\d{2})         #prob2
        (\d+.\d+.\d+.\d{2})
        (\d+:\d+|[\s-]*)              #result

        ''', re.VERBOSE)
            game_info = groupings_trial.findall(team)
            if len(game_info) < 1:
                error_games += ["empty list"]

            else:
                game_time = game_info[0][1].strip()
                full_date = datetime.datetime.strptime(game_time, "%H:%M")
                full_date = full_date + timedelta(hours=2)
                formatted_date = full_date.strftime("%H:%M")
                try:
                    results = game_info[0][14].split(':')
                    if len(results) == 2:
                        result_home = int(results[0])
                        result_away = int(results[1])
                    else:
                        result_home = 'no_result'
                        result_away = 'no_result'
                except Exception as no_score:
                    error_games += [no_score]

                def overall_result():
                    if result_home == 'no_result' or result_away == 'no_result':
                        win_odd = 0
                        if game_info[0][8] == 'X':
                            win_odd = game_info[0][11].split(":")[1]
                        elif game_info[0][8] == '1':
                            win_odd = game_info[0][10].split(":")[1]
                        elif game_info[0][8] == '2':
                            win_odd = game_info[0][12].split(":")[1]
                        return ['no_results_yet', win_odd]
                    else:
                        if game_info[0][8] == 'X':
                            win_odd = game_info[0][11].split(":")[1]
                            if result_home == result_away:
                                return ['drawwin', win_odd]
                            else:
                                return ['drawlose', win_odd]
                        elif game_info[0][8] == '1':
                            win_odd = game_info[0][10].split(":")[1]
                            if result_home > result_away:
                                return ['homewin', win_odd]
                            else:
                                return ['homelose', win_odd]
                        elif game_info[0][8] == '2':
                            win_odd = game_info[0][12].split(":")[1]
                            if result_away > result_home:
                                return ['awaywin', win_odd]
                            else:
                                return ['awaylose', win_odd]
                        elif game_info[0][8] == '12':
                            win_odd = 0
                            if result_away != result_home:
                                return ['12win', win_odd]
                            else:
                                return ['12lose', win_odd]
                        elif game_info[0][8] == '1X':
                            win_odd = 0
                            if result_home >= result_away:
                                return ['1Xwin', win_odd]
                            else:
                                return ['1Xlose', win_odd]
                        elif game_info[0][8] == 'X2':
                            win_odd = 0
                            if result_home <= result_away:
                                return ['X2win', win_odd]
                            else:
                                return ['X2lose', win_odd]

                result_home = str(result_home)
                result_away = str(result_away)
                if overall_result()[0] == 'homewin' or overall_result()[0] == 'awaywin' or overall_result()[
                    0] == '12win' or overall_result()[0] == '1Xwin' or overall_result()[0] == 'X2win':
                    counter_win += 1
                    counter_won_odd += float(overall_result()[1])
                    if overall_result()[0] == 'homewin' or overall_result()[0] == 'awaywin':
                        total_straight_win += 1
                elif overall_result()[0] == 'drawwin':
                    counter_win += 1
                    total_straight_win += 1
                    counter_won_odd += float(overall_result()[1])
                elif overall_result()[0] == 'drawlose' or overall_result()[0] == 'homelose' or overall_result()[
                    0] == 'awaylose' or overall_result()[0] == '12lose' or overall_result()[0] == '1Xlose' \
                        or overall_result()[0] == 'X2lose':
                    counter_lose += 1
                    if overall_result()[0] == 'drawlose' or overall_result()[0] == 'homelose' or overall_result()[
                    0] == 'awaylose':
                        total_straight_lose += 1
                    counter_lost_odd += float(overall_result()[1])
                elif overall_result()[0] == 'no_results_yet':
                    pass

                print(total_straight_win)
                profit += float((counter_won_odd - (total_straight_win + total_straight_lose))*49)

                print(profit)
                context = {
                    "counter_lost_odd": counter_lost_odd, "counter_won_odd": counter_won_odd,
                    "counter_lose": counter_lose, "counter_win": counter_win,
                    "total_straight_lose": total_straight_lose,
                    "total_straight_win": total_straight_win,
                    "profit": profit
                    }

                obj, created = Prono.objects.update_or_create(
                    teams=game_info[0][2],
                    defaults={'match_date': match_date, 'time': formatted_date,
                              'teams': game_info[0][2], 'chance': game_info[0][8],
                              'odd1': game_info[0][10], 'oddX': game_info[0][11],
                              'odd2': game_info[0][12], 'win_odd': overall_result()[1],
                              'match_result': game_info[0][14], 'result_overall': overall_result()[0]})

        games = Prono.objects.filter(match_date=match_date).order_by('time', 'teams')[:games_number]

        return [games, context]


def error_404(request):
    data = {}
    return render(request, 'mysite/error_404.html', {'data': data})


def error_500(request):
    data = {}
    return render(request, 'mysite/error_505.html', {'data': data})


def featured(request):
    today = topnavselector()
    res = requests.get('http://www.zulubet.com/tips-%d-0%d-%d.html' % (today.day, today.month, today.year))
    match_date = today.strftime("%d-%m")  # date when the match is played
    games = parser(res, match_date)[0]
    request_from = "tod"
    return render(request, 'mysite/featured.html', {"games": games[:7], "request_tom": request_from})


def game_details(request, pk):
    games_detail = get_object_or_404(Prono, pk=pk)
    return render(request, 'mysite/game_details.html', {'game': games_detail})


def login(request):
    return render(request, 'mysite/login.html')
