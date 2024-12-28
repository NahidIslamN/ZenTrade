from django.shortcuts import render, redirect
from django.views import View

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from AuthApp.models import Team, CustomUser, MyRefeList,MytodaysIncome,Notifications, DynamicControlScheduling, UserLoginActivity

from BanckManagement.models import *
from django.contrib import messages
from datetime import date
from django.db.models import F

import pytz
from django.utils import timezone

# Create your views here.


class DeshBoard(View):
    @method_decorator(login_required)
    def get(self,request):


        return render(request,'users/deshboard.html')
    


class Teams(View):
    @method_decorator(login_required)
    def get(self,request):
        users = request.user

        teammembers = Team.objects.get(team_admin = users )
        members = teammembers.members.all()

        cp = {
            "teammembers":members
        }

        return render(request,'users/teams.html', context=cp)
    
    @method_decorator(login_required)
    def post(self, request):
        users = request.user
        data = request.POST
        username = data.get('username')

        if CustomUser.objects.filter(username = username).exists():
            new_member = CustomUser.objects.get(username = username)
            Teams = Team.objects.get(team_admin = users)
            sets = Teams.members
            sets.add(new_member)
            Teams.save()
            redirect('/user/team-members/')
        else:
            teammembers = Team.objects.get(team_admin = users )
            members = teammembers.members.all()


            cp = {
                    "teammembers":members,
                    "data":data
            }

            messages.info(request,"username not found!")
            
            return render(request,'users/teams.html', context=cp)
             

        return redirect('/user/team-members/')
    


class ReferenceList(View):
    @method_decorator(login_required)
    def get(self, request):
        users = request.user

        teammembers = MyRefeList.objects.get(team_admin = users )
        members = teammembers.members.all()

        cp = {
            "teammembers":members
        }
        return render(request,'users/reference.html', context=cp)

    

class MyRewards(View):
    @method_decorator(login_required)    
    def get(self, request):
        users = request.user

        bonuses = GetReward.objects.filter(reward_amin = users).order_by('-created_at')
        

        cp = {
            "bonuses":bonuses
        }

        return render(request, 'users/bonuses.html', context=cp)



class MyTodayTradeIncome(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user

        income_today = MytodaysIncome.objects.get(income_admin = user)

        cp = {
            "income_today":income_today
        }


        return render(request,'users\incometodays.html', context=cp)

class ResetTotalIncomeHistory(View):
    @method_decorator(login_required)
    def get(self,request):
        user = request.user
        BN = BankAccount.objects.get(account_admin = user)
        BN.income_balance = 0.00
        BN.save()
        title = "Removed Total Income History!"
        text = 'You are successfully removed your total income history! '
        N = Notifications.objects.create(
            to_user = user,
            title = title,
            discription = text
        )
        N.save()
        return redirect('/user/deshboard/')

    

class ResetPayoutHistory(View):
    @method_decorator(login_required)
    def get(self,request):
        user = request.user
        PayPal = PayOut.objects.filter(admin_take = user, removed_status = False)
        for payout in PayPal:
            payout.removed_status = True
            payout.save()

        title = "Removed Payout History!"
        text = 'You are successfully removed your Payout History! '
        N = Notifications.objects.create(
            to_user = user,
            title = title,
            discription = text
        )
        N.save()
        return redirect('/user/deshboard/')



class ViewMyNote(View):
    @method_decorator(login_required)
    def get(self,request):
        user = request.user
        all_note = Notifications.objects.filter(to_user=user).order_by('-created_at')

        cp = {
            'all_note':all_note
        }
      
        return render(request,'users/notifications.html', context = cp)
    
    @method_decorator(login_required)
    def post(self, request):
        user = request.user
        data = request.POST
        try:
            note = Notifications.objects.get(id = data.get('noteid'))
            if note.to_user == user:
                note.seen_status= True
                note.save()
            else:
                pass
        except:
            pass

        return redirect('/user/view-notifications/')



####################################################################################adminpart##



class GetmyReward(View):
    @method_decorator(login_required)
    def get(self,request):
        AdminAprove_Status = DynamicControlScheduling.objects.get(id = 1)
        if AdminAprove_Status.getreward:
            user = request.user
            UserActivitys = UserLoginActivity.objects.filter(user = user).order_by('-login_time')[0]
            timezones = pytz.timezone(UserActivitys.timezone)
        
            if InvastMents.objects.filter(investor = user).exists():
                datetoday = timezone.now()
                localized_time = datetoday.astimezone(timezones)
                localized_date = localized_time.date()

                
                if GetReward.objects.filter(reward_amin = user, created_at__date=localized_date).exists():
                    message.info(request,"Already Get todays bonus!")
                    return redirect('/user/deshboard/')
                else:
                    inv = InvastMents.objects.filter(investor = user)[0]
                    invbal = inv.inv_ammount
                    if TradePackeges.objects.filter( Plan_start__lte=invbal, Plan_end__gte=invbal).exists():
                        tpack = TradePackeges.objects.filter( Plan_start__lte=invbal, Plan_end__gte=invbal)[0]
                        daily_reward_amount = invbal*(((tpack.range_start+tpack.range_end)/2)/100)
                        
                        account = BankAccount.objects.get(account_admin = user)
                        account.income_balance = F('income_balance') + daily_reward_amount
                        account.walet_balance = F('walet_balance') + daily_reward_amount
                        account.save()
                        TIT = MytodaysIncome.objects.get(income_admin = account.account_admin)
                        TIT.incomefee = daily_reward_amount
                        TIT.save()                    


                    

                            # Send a notification to the account admin
                        subject = 'Daily Reward Notification'
                        message = f'Dear {account.account_admin.email},You have received a daily reward of {daily_reward_amount:.2f}. Best regards, QuickTrade'
                            
                        N = Notifications.objects.create(
                            to_user=account.account_admin,
                            title=subject,
                            discription= message
                        )
                        N.save()
                    

                        G = GetReward.objects.create(
                                reward_amin = account.account_admin,
                                title = "Daily Reward",
                                ammount = daily_reward_amount,
                        )
                        G.save()
        else:
            messages.info(request,f'{AdminAprove_Status.sks}')  
        return redirect('/accounts/investmoney/')
    





    @method_decorator(login_required)
    def get(self,request):
        AdminAprove_Status = DynamicControlScheduling.objects.get(id = 1)
        if AdminAprove_Status.getreward:
            user = request.user
            UserActivitys = UserLoginActivity.objects.filter(user = user).order_by('-login_time')[0]
            timezones = pytz.timezone(UserActivitys.timezone)
        
            if InvastMents.objects.filter(investor = user).exists():
                datetoday = timezone.now()
                localized_time = datetoday.astimezone(timezones)
                localized_date = localized_time.date()

                
                if GetReward.objects.filter(reward_amin = user, created_at__date=localized_date).exists():
                    message.info(request,"Already Get todays bonus!")
                    return redirect('/user/deshboard/')
                else:
                    inv = InvastMents.objects.filter(investor = user)[0]
                    invbal = inv.inv_ammount
                    if TradePackeges.objects.filter( Plan_start__lte=invbal, Plan_end__gte=invbal).exists():
                        tpack = TradePackeges.objects.filter( Plan_start__lte=invbal, Plan_end__gte=invbal)[0]
                        daily_reward_amount = invbal*(((tpack.range_start+tpack.range_end)/2)/100)
                        
                        account = BankAccount.objects.get(account_admin = user)
                        account.income_balance = F('income_balance') + daily_reward_amount
                        account.walet_balance = F('walet_balance') + daily_reward_amount
                        account.save()
                        TIT = MytodaysIncome.objects.get(income_admin = account.account_admin)
                        TIT.incomefee = daily_reward_amount
                        TIT.save()                    


                    

                                # Send a notification to the account admin
                        subject = 'Daily Reward Notification'
                        message = f'Dear {account.account_admin.email},You have received a daily reward of {daily_reward_amount:.2f}. Best regards, QuickTrade'
                            
                        N = Notifications.objects.create(
                            to_user=account.account_admin,
                            title=subject,
                            discription= message
                        )
                        N.save()
                    

                        G = GetReward.objects.create(
                                reward_amin = account.account_admin,
                                title = "Daily Reward",
                                ammount = daily_reward_amount,
                        )
                        G.save()
        else:
            messages.info(request,f'{AdminAprove_Status.sks}')  
        return redirect('/accounts/investmoney/')