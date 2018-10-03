# if overall_result()[0] == 'homewin' or overall_result()[0] == 'awaywin' or overall_result()[0] == '12win' or overall_result()[0] == '1Xwin' or overall_result()[0] == 'X2win':
#     counter_win += 1
#     counter_won_odd += float(overall_result()[1])
# if overall_result()[0] == 'homewin' or overall_result()[0] == 'awaywin':
#     total_straight_win += 1
# elif overall_result()[0] == 'drawwin':
#     counter_win += 1
#     total_straight_win += 1
#     counter_won_odd += float(overall_result()[1])
# elif overall_result()[0] == 'drawlose' or overall_result()[0] == 'homelose' or overall_result()[0] == 'awaylose' or overall_result()[0] == '12lose' or overall_result()[0] == '1Xlose' or overall_result()[0] == 'X2lose':
#     counter_lose += 1
#     if overall_result()[0] == 'drawlose' or overall_result()[0] == 'homelose' or overall_result()[0] == 'awaylose':
#         total_straight_lose += 1
#         counter_lost_odd += float(overall_result()[1])
# elif overall_result()[0] == 'no_results_yet':
#     pass
#
# profit = counter_won_odd - (total_straight_win + total_straight_lose)
# context = {
#     "counter_lost_odd": counter_lost_odd, "counter_won_odd": counter_won_odd,
#     "counter_lose": counter_lose, "counter_win": counter_win,
#     "total_straight_lose": total_straight_lose,
#     "total_straight_win": total_straight_win,
#     "profit": profit * 49
#     }
