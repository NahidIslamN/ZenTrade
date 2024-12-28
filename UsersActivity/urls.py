

from django.urls import path
from UsersActivity.views import *


urlpatterns = [
    path('deshboard/', DeshBoard.as_view(), name='deshboard'),
    path('team-members/', Teams.as_view(), name = 'team-members'),
    path('reference-members/',ReferenceList.as_view(), name='reference-members'),
    path('all-bonus/', MyRewards.as_view(), name='all-bonus'),
    path('todaysincome/',MyTodayTradeIncome.as_view(), name='todaysincome'),
    path('getmyreword/', GetmyReward.as_view(), name='getmyreword'),
    path('reset-total-income/', ResetTotalIncomeHistory.as_view()),
    path('reset-payout-history/',ResetPayoutHistory.as_view()),
    path('view-notifications/', ViewMyNote.as_view(), name='view-notifications'),

    
]




