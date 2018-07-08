import datetime
import re
from datetime import timedelta

import bs4
import requests
from django.shortcuts import render

from .models import Prono


def topnavselector():
    date = datetime.datetime.now()
    return date


def homepage_today(request):
    today = topnavselector()
    res = requests.get('http://www.zulubet.com/tips-%d-0%d-%d.html' % (today.day, today.month, today.year))
    match_date = today.strftime("%d-%m")  # date when the match is
    games = parser(res, match_date)
    return render(request, 'mysite/index.html', {"games": games})


def yesterday(request):
    today = topnavselector() - timedelta(days=1)
    res = requests.get('http://www.zulubet.com/tips-%d-0%d-%d.html' % (today.day, today.month, today.year))
    match_date = today.strftime("%d-%m")  # date when the match is played
    games = parser(res, match_date)
    return render(request, 'mysite/index.html', {"games": games})


def tomorrow(request):
    today = topnavselector() + timedelta(days=1)
    res = requests.get('http://www.zulubet.com/tips-%d-0%d-%d.html' % (today.day, today.month, today.year))
    match_date = today.strftime("%d-%m")  # date when the match is played
    games = parser(res, match_date)
    return render(request, 'mysite/index.html', {"games": games})


def parser(res, match_date):
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
                        win_odd = game_info[0][11].split(":")[1]
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
                            win_odd = game_info[0][11].split(":")[1]
                            if result_away != result_home:
                                return ['12win', win_odd]
                            else:
                                return ['12lose', win_odd]
                        elif game_info[0][8] == '1X':
                            win_odd = game_info[0][10].split(":")[1]
                            if result_home >= result_away:
                                return ['homewin', win_odd]
                            else:
                                return ['homelose', win_odd]
                        elif game_info[0][8] == 'X2':
                            win_odd = game_info[0][12].split(":")[1]
                            if result_home <= result_away:
                                return ['awaywin', win_odd]
                            else:
                                return ['awaylose', win_odd]

                result_home = str(result_home)
                result_away = str(result_away)

                obj, created = Prono.objects.update_or_create(
                    teams=game_info[0][2],
                    defaults={'match_date': match_date, 'time': formatted_date,
                              'teams': game_info[0][2], 'chance': game_info[0][8],
                              'odd1': game_info[0][10], 'oddX': game_info[0][11],
                              'odd2': game_info[0][12], 'win_odd': overall_result()[1],
                              'match_result': game_info[0][14], 'result_overall': overall_result()[0]})

        games = Prono.objects.filter(match_date=match_date).order_by('time', 'teams')[:games_number]
        return games


def error_404(request):
    data = {}
    return render(request, 'mysite/error_404.html', {'data': data})


def error_500(request):
    data = {}
    return render(request, 'mysite/error_505.html', {'data': data})
