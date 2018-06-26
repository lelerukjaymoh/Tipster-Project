import re

import bs4
import requests
from django.shortcuts import render, get_object_or_404

from datetime import timedelta
import datetime

from .models import Prono


def homepage(request):
    # error = get_object_or_404(Prono)
    today = datetime.datetime.now()
    res = requests.get('http://www.zulubet.com/tips-%d-0%d-%d.html' % (21, today.month, today.year))
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
        getting_results = re.compile(r'\d+[^:]')
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
                    results = getting_results.findall(game_info[0][14])
                    result_home = int(results[0])
                    result_away = int(results[1])
                except Exception as no_score:
                    error_games += [no_score]
                    result_home = 10
                    result_away = 10

                def overall_result():
                    if result_home == 10 and result_away == 10:
                        return 'no_results_yet'
                    else:
                        if game_info[0][8] == 'X':
                            if result_home == result_away:
                                return 'drawwin'
                            else:
                                return 'drawlose'
                        elif game_info[0][8] == '1':
                            if result_home > result_away:
                                return 'homewin'
                            else:
                                return 'homelose'
                        elif game_info[0][8] == '2':
                            if result_away > result_home:
                                return 'awaywin'
                            else:
                                return 'awaylose'
                        elif game_info[0][8] == '12':
                            if result_away != result_home:
                                return '12win'
                            else:
                                return '12lose'
                        elif game_info[0][8] == '1X':
                            if result_home >= result_away:
                                return 'homewin'
                            else:
                                return 'homelose'
                        elif game_info[0][8] == 'X2':
                            if result_home <= result_away:
                                return 'awaywin'
                            else:
                                return 'awaylose'

                try:
                    prono = Prono.objects.get(date=game_info[0][0], time=formatted_date, teams=game_info[0][2],
                                              prob1=game_info[0][4], probX=game_info[0][5], prob2=game_info[0][6],
                                              chance=game_info[0][8], odd1=game_info[0][10], oddX=game_info[0][11],
                                              odd2=game_info[0][12], result_home=result_home,
                                              result_away=result_away, match_result=game_info[0][14],
                                              result_overall=overall_result())
                    prono.date = game_info[0][0]
                    prono.time = formatted_date
                    prono.teams = game_info[0][2]
                    prono.probX = game_info[0][5]
                    prono.prob2 = game_info[0][6]
                    prono.chance = game_info[0][8]
                    prono.odd1 = game_info[0][10]
                    prono.oddX = game_info[0][11]
                    prono.odd2 = game_info[0][12]
                    prono.result_home = result_home
                    prono.result_away = result_away
                    prono.match_result = game_info[0][14]
                    prono.result_overall = overall_result()
                    prono.save()
                except Prono.DoesNotExist:
                    prono = Prono(date=game_info[0][0], time=formatted_date, teams=game_info[0][2],
                                  prob1=game_info[0][4], probX=game_info[0][5], prob2=game_info[0][6],
                                  chance=game_info[0][8], odd1=game_info[0][10], oddX=game_info[0][11],
                                  odd2=game_info[0][12], result_home=result_home, match_result=game_info[0][14],
                                  result_away=result_away, result_overall=overall_result())
                    prono.save()

        games = Prono.objects.order_by('time', 'date')[:games_number]
        return render(request, 'mysite/index.html', {"games": games})
