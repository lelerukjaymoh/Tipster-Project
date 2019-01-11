# import datetime
# import requests
# from datetime import timedelta
# from collections import Counter
# from django.shortcuts import render
#
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
#     return render(request, 'mysite/wallet.html', {
#         "progress": progress_details, "confirm": confirm
#         })
