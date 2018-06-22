import re

import bs4
import requests
from django.shortcuts import render, get_object_or_404

from .models import Prono


def homepage(request):
    # error = get_object_or_404(Prono)
    res = requests.get('http://www.zulubet.com/tips-21-06-2018.html')
    try:
        res.raise_for_status()

    except Exception as error:
        print('There was a problem getting web data: %s' % error)

    zulu_soup = bs4.BeautifulSoup(res.content, 'html.parser')
    error_games = 0

    if type(zulu_soup) == bs4.BeautifulSoup:
        tr_elems = zulu_soup.findAll("tr", bgcolor=re.compile('^#.*'))
        games_number = len(tr_elems)
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
                error_games += 1
            else:
                try:
                    prono = Prono.objects.get(date=game_info[0][0], time=game_info[0][1], teams=game_info[0][2],
                                              prob1=game_info[0][4], probX=game_info[0][5], prob2=game_info[0][6],
                                              chance=game_info[0][8], odd1=game_info[0][10], oddX=game_info[0][11],
                                              odd2=game_info[0][12], result=game_info[0][14])

                    prono.date = game_info[0][0]
                    prono.time = game_info[0][1]
                    prono.teams = game_info[0][2]
                    prono.prob1 = game_info[0][4]
                    prono.probX = game_info[0][5]
                    prono.prob2 = game_info[0][6]
                    prono.chance = game_info[0][8]
                    prono.odd1 = game_info[0][10]
                    prono.oddX = game_info[0][11]
                    prono.odd2 = game_info[0][12]
                    prono.result = game_info[0][14]
                    prono.save()
                except Prono.DoesNotExist:
                    prono = Prono(date=game_info[0][0], time=game_info[0][1], teams=game_info[0][2],
                                  prob1=game_info[0][4], probX=game_info[0][5], prob2=game_info[0][6],
                                  chance=game_info[0][8], odd1=game_info[0][10], oddX=game_info[0][11],
                                  odd2=game_info[0][12], result=game_info[0][14])
                    prono.save()

        games = Prono.objects.all().reverse()
        return render(request, 'mysite/index.html', {"games": games})
