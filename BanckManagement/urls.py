

from django.urls import path

from BanckManagement.views import *



urlpatterns = [
    #users
    path('managefunds/', ManageFund.as_view(), name='managefunds'),
    path('fundaceptor/', ViewMyAceptor.as_view(), name='fundaceptor'),
    path('fundaceptor/<id>/', ViewMyAceptor.as_view(), name='fundaceptor'),
    path('payout/', Payout.as_view(), name="payout"),
    path('deposite-funds/', DepositeFunds.as_view(),name='deposite-funds'),
    path('investmoney/', InvestMoney.as_view(), name='InvestMoney'),

    ##admin& user
    path('tradepackages/',Tradepackages.as_view(), name='tradepackages'),




    #Admin Urls
    path('processpayout/', AdminPayoutRequests.as_view(), name='processpayout'),
    path('processeddeposite/', AdminDepositeRequest.as_view(), name='processeddeposite' ),
    path('processeddeposite/<id>/', AdminDepositeRequest.as_view(), name='processeddeposite' ),
    
    

   

    
]



