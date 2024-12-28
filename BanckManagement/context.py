
from django.contrib.auth.models import AnonymousUser
from BanckManagement.models import BankAccount, PayOut, Deposite,GetReward,InvastMents,PayOut
from django.db.models import Sum

def content(request):
    # Check if the user is authenticated
    if isinstance(request.user, AnonymousUser):
        # Return default values for anonymous users
        balance = 0.00
        walet_balance = 0.00
        income_balance = 0.00
        total_sum = 0.00
        total_sumdp = 0.00
        total_sumreward = 0.00
        deptorew = 0.00
        total_suminvestment = 0.00
        total_sumpayouts = 0.00
        status=  0.00
    else:
        # Fetch notifications for logged-in users
        users = request.user
        BA = BankAccount.objects.get(account_admin = users )


        balance = BA.bank_balance
        walet_balance = float(BA.walet_balance)
        income_balance = BA.income_balance
        total_payout = PayOut.objects.filter(admin_take=users, aproved_status=True,removed_status = False).aggregate(total_sum=Sum('payout_ammount'))

        total_sum = total_payout['total_sum'] if total_payout['total_sum'] is not None else 0
        









        # Admin Conttexts # Admin Conttexts # Admin Conttexts # Admin Conttexts





        totaldeposites = Deposite.objects.filter(aproved_status = True).aggregate(total_sumdp=Sum('deposite_ammount'))
        total_sumdp = totaldeposites['total_sumdp'] if totaldeposites['total_sumdp'] is not None else 0



        totalreward = GetReward.objects.filter().aggregate(total_sumrew=Sum('ammount'))
        total_sumreward = totalreward['total_sumrew'] if totalreward['total_sumrew'] is not None else 0


        totalinv = InvastMents.objects.filter().aggregate(total_suminv=Sum('inv_ammount'))
        total_suminvestment = totalinv['total_suminv'] if totalinv['total_suminv'] is not None else 0


        totalpayout = PayOut.objects.filter(aproved_status = True).aggregate(total_sumpay=Sum('payout_ammount'))
        total_sumpayouts = totalpayout['total_sumpay'] if totalpayout['total_sumpay'] is not None else 0



        totalbankbalance = BankAccount.objects.filter().aggregate(total_bankbal=Sum('bank_balance'))

        total_sumbankbalance = totalbankbalance['total_bankbal'] if totalbankbalance['total_bankbal'] is not None else 0



        totalwalbalance = BankAccount.objects.filter().aggregate(total_walbalance=Sum('walet_balance'))

        total_sumwalbalance = totalwalbalance['total_walbalance'] if totalwalbalance['total_walbalance']  is not None else 0


        abilitypayouts = total_sumbankbalance + total_sumwalbalance

        status = total_sumdp-(abilitypayouts+total_sumpayouts)



        deptorew = total_sumdp-total_sumpayouts
       

        
    # Return the variables to be globally available in templates
    return {
        'balance':balance,
        'walet_balance':walet_balance,
        'income_balance':income_balance,
        'total_sum':total_sum,


        ####admin context
        "total_sumdp":total_sumdp,
        'total_sumreward':total_sumreward,
        'deptorew':deptorew,
        'total_suminvestment':total_suminvestment,
        'total_sumpayouts':total_sumpayouts,
        'status':status
       
    }
