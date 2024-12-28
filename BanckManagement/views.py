from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from AuthApp.models import CustomUser,MyRefeList
from BanckManagement.models import *
from django.contrib import messages
from AuthApp.models import *
from django.db.models import F
from django.utils import timezone
import pytz
from django.db.models import Q


# Create your views here.


class ManageFund(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        where_i_manage = WaletShate.objects.filter(to_user = user).order_by('-created_at')
        
        cp = {
            'where_i_manage':where_i_manage

        }
        return render(request,'BanckManagement/managefund.html', context=cp)
    
    @method_decorator(login_required)
    def post(self, request):
        AdminAprove_Status = DynamicControlScheduling.objects.get(id = 1)
        if AdminAprove_Status.manage_fund:
            to_user = request.user

            data = request.POST
            managetype = data.get("managetype")
            email = data.get("email")
            ammount  = data.get('ammount')
            details = data.get('remarks')
            remarks = data.get('remarks')
            
            
            try:
                from_user = CustomUser.objects.get(email = email)
            except:
                from_user = None

            if from_user:
                if managetype == "True":
                    share = WaletShate.objects.create(
                        from_user = from_user,
                        to_user = to_user,
                        share_ammount = ammount,
                        main_account = True,
                        remarks = remarks,
                        Txn_Details = details
                    )
                    share.save()
                    messages.info(request,"Succeessfully sent request to user!")
                    return redirect('/accounts/managefunds/')
                elif managetype == "False":
                    share = WaletShate.objects.create(
                        from_user = from_user,
                        to_user = to_user,
                        share_ammount = ammount,
                        remarks = remarks,
                        Txn_Details = details                
                    )
                    share.save()
                    messages.info(request,"Succeessfully sent request to user!")
                    return redirect('/accounts/managefunds/')

                else:
                    return render(request,'BanckManagement/managefund.html', context={'data':data})
                
            else:
                messages.info(request,"Request failed! User not exeists!")
                return render(request,'BanckManagement/managefund.html', context={'data':data})
            
        else:
            messages.info(request,f'{AdminAprove_Status.sks}')
            return redirect('/accounts/managefunds/')
        

        


class ViewMyAceptor(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        where_i_manage = WaletShate.objects.filter(from_user = user).order_by('-created_at')
        
        cp = {
            'where_i_manage':where_i_manage

        }
        return render(request,'BanckManagement/aprovemyaceptor.html', context=cp)
    
    @method_decorator(login_required)
    def delete(self, request, id):
        users= request.user
        try:
            pay_request = WaletShate.objects.get(id = id)
            if pay_request.from_user == users:
                pay_request.delete()
                messages.info(request,"Delete Successfully")
                return redirect('/accounts/fundaceptor/')
            else:
                messages.info(request,"you can't delete the request")
                return redirect('/accounts/fundaceptor/')
        except:
            messages.info(request,"you can't delete the request")
            return redirect('/accounts/fundaceptor/')
    @method_decorator(login_required)
    def aprove(self,request,id):
        users = request.user
        try:
            ws_model= WaletShate.objects.get(id = id)
            if ws_model.from_user == users:
                ammout = ws_model.share_ammount
                FromBN = BankAccount.objects.get(account_admin = users)
                touser = ws_model.to_user
                TOBN = BankAccount.objects.get(account_admin = touser)
                mainstatus = ws_model.main_account

                if mainstatus:
                    if FromBN.bank_balance >= ammout:
                        FromBN.bank_balance = FromBN.bank_balance-ammout
                        TOBN.bank_balance = TOBN.bank_balance+ammout
                        ws_model.aproved_status = True
                        ws_model.save()
                        TOBN.save()
                        FromBN.save()

                        title = 'transition complete'
                        disc = f'Successfully Transiction complete! from {users.email} accept your request and sent to you {ammout}USDT.'
                        note = Notifications.objects.create(
                            to_user = touser,
                            title = title,
                            discription = disc

                        )
                        note.save()


                        title = 'transition complete'
                        disc = f'Successfully Transiction complete! to {touser.email}! you pay {ammout}USDT.'
                        note2 = Notifications.objects.create(
                            to_user = users,
                            title = title,
                            discription = disc

                        )
                        note2.save()

                        
                        messages.info(request,"Successfully Accepet")
                        return redirect('/accounts/fundaceptor/')
                        
                    else:
                        messages.info(request,"insuficent fund!")
                        return redirect('/accounts/fundaceptor/')
                    




                else:
                    if FromBN.walet_balance >= ammout:
                        FromBN.walet_balance = FromBN.walet_balance-ammout
                        TOBN.bank_balance = TOBN.bank_balance + ammout
                        ws_model.aproved_status = True
                        ws_model.save()
                        TOBN.save()
                        FromBN.save()

                        title = 'transition complete'
                        disc = f'Successfully Transiction complete! from {users.email} accept your request and sent to you {ammout} USDT.'
                        note = Notifications.objects.create(
                            to_user = touser,
                            title = title,
                            discription = disc

                        )
                        note.save()


                        title = 'transition complete'
                        disc = f'Successfully Transiction complete! to {touser.email}! you pay {ammout}USDT.'
                        note2 = Notifications.objects.create(
                            to_user = users,
                            title = title,
                            discription = disc

                        )
                        note2.save()

                        
                        messages.info(request,"Successfully Accepet")
                        return redirect('/accounts/fundaceptor/')
                        
                    else:
                        messages.info(request,"insuficent fund!")
                        return redirect('/accounts/fundaceptor/')
                    



            else:
                messages.info(request,"you can't accept the request!")
                return redirect('/accounts/fundaceptor/')
        except:
            messages.info(request,"Somthing want to wrong!")
            return redirect('/accounts/fundaceptor/')

        
        

    @method_decorator(login_required)
    def post(self, request, id):
        AdminAprove_Status = DynamicControlScheduling.objects.get(id = 1)
        if AdminAprove_Status.manage_fund:
                
            method = request.POST.get('_method', '').upper()
            if method == 'DELETE':
                return self.delete(request,id)
            elif method == 'PUT':
                return self.aprove(request,id)

        

            return redirect('/accounts/fundaceptor/')
        else:
            messages.info(request,f'{AdminAprove_Status.sks}')
            return redirect('/accounts/fundaceptor/')



class Payout(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        where_i_manage = PayOut.objects.filter(admin_take = user).order_by('-created_at')
        AdminAprove_Status = DynamicControlScheduling.objects.get(id = 1)
        payoutcharge = AdminAprove_Status.payout_charge
        
        cp = {
            'where_i_manage':where_i_manage,
            "payoutcharge":payoutcharge

        }
        return render(request,'BanckManagement/payout.html', context=cp)
    
    @method_decorator(login_required)
    def post(self,request):
        data = request.POST

 
        AdminAprove_Status = DynamicControlScheduling.objects.get(id = 1)
        if AdminAprove_Status.payout and float(data.get('ammount'))>=20:
            users = request.user
            
            managetype = data.get('managetype')
            binence_accounts = data.get('binenceaccount')
            ammount = float(data.get('ammount',0))
            details = data.get('details')
            remarks = data.get('remarks')
            charge = float(data.get('charge',0)) 
            try:
                BN = BankAccount.objects.get(account_admin = users)

                if managetype == "False":
                    bb = BN.walet_balance
                    if bb>=ammount+charge:
                        if PayOut.objects.filter(admin_take = users, aproved_status = False).exists():
                            messages.info(request,"you already have a pyout request try again later for security reson!")
                            return redirect('/accounts/payout/')

                        else:
                            pp = PayOut.objects.create(
                                admin_take = users,
                                BN = BN,
                                Txn_Details = details,
                                payout_ammount = ammount,
                                Charges = charge,
                                binence_account = binence_accounts,
                                remarks = remarks
                            )
                            pp.save()
                            messages.info(request,"successfully withdrow request sent! wait for admin processing and confirmation!")
                            return redirect('/accounts/payout/')

                    else:
                        messages.info(request,"insuficiend funds")
                        return render(request,'BanckManagement/payout.html', context={"data":data})


                else:
                    bb = BN.bank_balance
                    if bb>=ammount+charge:
                        if PayOut.objects.filter(admin_take = users, aproved_status = False).exists():
                            messages.info(request,"you already have a pyout request try again later for security reson!")
                            return redirect('/accounts/payout/')

                        else:
                            pp = PayOut.objects.create(
                                admin_take = users,
                                BN = BN,
                                Txn_Details = details,
                                payout_ammount = ammount,
                                Charges = charge,
                                main = True,
                                binence_account = binence_accounts,
                                remarks = remarks,
                                
                            )
                            pp.save()
                            messages.info(request,"successfully withdrow request sent! wait for admin processing and confirmation!")
                            return redirect('/accounts/payout/')

                    else:
                        messages.info(request,"insuficiend funds")
                        return render(request,'BanckManagement/payout.html', context={"data":data})


            except:
                messages.info(request,"sumthing worng try again letter")
                return redirect('/accounts/payout/')
        
        else:
            messages.info(request,f'{AdminAprove_Status.sks}')
            return redirect('/accounts/payout/')





class Tradepackages(View):
    @method_decorator(login_required)
    def get(self, request):

        td_packs = TradePackeges.objects.filter(status = True).order_by('id')

        cp={
            "td_packs":td_packs,
 
        }
        return render(request, 'BanckManagement/tradepackeges.html', context=cp)




class InvestMoney(View):
    
    def get(self, request):
        user = request.user                  
        UserActivitys = UserLoginActivity.objects.filter(user = user).order_by('-login_time')[0]
        timezones = pytz.timezone(UserActivitys.timezone)
        GR = None
        INV = None
        datetoday = timezone.now()
        localized_time = datetoday.astimezone(timezones)
        localized_date = localized_time.date()

        if GetReward.objects.filter(reward_amin=user, created_at__date=localized_date).exists():
            GR = GetReward.objects.filter(reward_amin=user, created_at__date=localized_date)
        else:
            pass


        if InvastMents.objects.filter(investor = user).exists():
            INV = InvastMents.objects.filter(investor = user)
        else:
            pass



        investments = InvastMents.objects.filter(investor = user ).order_by('-created_at')
        
        cp = {
            "investments":investments,
            "GR":GR,
            "INV":INV
        }

        return render(request,'BanckManagement/investpage.html', context=cp)
    def post(self, request):
        AdminAprove_Status = DynamicControlScheduling.objects.get(id = 1)
        if AdminAprove_Status.imvest:
            US = request.user
            BN = BankAccount.objects.get(account_admin = US)
            data = request.POST
            
                   
            ammount = float(data.get("ammount")) 
        
            remarks = data.get("remarks")
            if BN.bank_balance>=ammount:
                BN.bank_balance = BN.bank_balance - ammount
                

                if InvastMents.objects.filter(investor = US).exists():
                    inv = InvastMents.objects.filter(investor = US)[0]
                    inv.inv_ammount = inv.inv_ammount+ammount
                    inv.save()
                    BN.save()


                    # Check if the user is a team_admin in any MyRefeList
                    if  MyRefeList.objects.filter(members=US).exists():
                        is_in_any_referelist= MyRefeList.objects.filter(members=US)[0]                   
                        team_admin1 = is_in_any_referelist.team_admin
                        BN1 = BankAccount.objects.get(account_admin = team_admin1)
                        bon1 = ammount * 0.05  # Calculate 5% of the amount
                        BN1.walet_balance = BN1.walet_balance+bon1
                        BN1.save()

                        title='Get Reward' 
                        messagess = f"Get reference reward {bon1} from {US.email}"
                        note = Notifications.objects.create(
                            to_user = team_admin1,
                            title = title,
                            discription =messagess
                        )
                        note.save()                                         
                        

                        if MyRefeList.objects.filter(members=team_admin1).exists():
                            is_in_any_referelist2 = MyRefeList.objects.filter(members=team_admin1)[0]
                            team_admin2 = is_in_any_referelist2.team_admin
                            BN1 = BankAccount.objects.get(account_admin = team_admin2)
                            bon2 = ammount * 0.04  # Calculate 5% of the amount
                            BN1.walet_balance = BN1.walet_balance+bon2
                            BN1.save()
                            title='Get Reward' 
                            messagess = f"Get reference reward {bon2} from {US.email}"
                            note = Notifications.objects.create(
                                to_user = team_admin2,
                                title = title,
                                discription =messagess
                            )
                            note.save()
                            
                            if MyRefeList.objects.filter(members=team_admin2).exists():
                                is_in_any_referelist3 = MyRefeList.objects.filter(members=team_admin2)[0]
                                team_admin3 = is_in_any_referelist3.team_admin
                                BN1 = BankAccount.objects.get(account_admin = team_admin3)
                                bon3 = ammount * 0.03  # Calculate 5% of the amount
                                BN1.walet_balance = BN1.walet_balance+bon3
                                BN1.save()

                                title='Get Reward' 
                                messagess = f"Get reference reward {bon3} from {US.email}"
                                note = Notifications.objects.create(
                                    to_user = team_admin1,
                                    title = title,
                                    discription =messagess
                                )
                                note.save()



                                if MyRefeList.objects.filter(members=team_admin3).exists():
                                    is_in_any_referelist4 = MyRefeList.objects.filter(members=team_admin3)[0]
                                    team_admin4 = is_in_any_referelist4.team_admin
                                    BN1 = BankAccount.objects.get(account_admin = team_admin4)
                                    bon4 = ammount * 0.02  # Calculate 5% of the amount
                                    BN1.walet_balance = BN1.walet_balance+bon4
                                    BN1.save()

                                    title='Get Reward' 
                                    messagess = f"Get reference reward {bon4} from {US.email}"
                                    note = Notifications.objects.create(
                                        to_user = team_admin4,
                                        title = title,
                                        discription =messagess
                                    )
                                    note.save()

                                    if MyRefeList.objects.filter(members=team_admin4).exists():
                                        is_in_any_referelist5 = MyRefeList.objects.filter(members=team_admin4)[0]
                                        team_admin5 = is_in_any_referelist5.team_admin
                                        BN1 = BankAccount.objects.get(account_admin = team_admin5)
                                        bon5 = ammount * 0.01  # Calculate 5% of the amount
                                        BN1.walet_balance = BN1.walet_balance+bon5
                                        BN1.save()
                                        title='Get Reward' 
                                        messagess = f"Get reference reward {bon5} from {US.email}"
                                        note = Notifications.objects.create(
                                            to_user = team_admin5,
                                            title = title,
                                            discription =messagess
                                        )
                                        note.save() 


                    
                else:
                    E = InvastMents.objects.create(
                        investor = US,
                        inv_ammount = ammount,
                        remarks = remarks,
                        aproved_status = True
                    )
                    E.save()
                    BN.save()

                    # Check if the user is a team_admin in any MyRefeList
                    if  MyRefeList.objects.filter(members=US).exists():
                        is_in_any_referelist= MyRefeList.objects.filter(members=US)[0]                   
                        team_admin1 = is_in_any_referelist.team_admin
                        BN1 = BankAccount.objects.get(account_admin = team_admin1)
                        bon1 = ammount * 0.05  # Calculate 5% of the amount
                        BN1.walet_balance = BN1.walet_balance+bon1
                        BN1.save()

                        title='Get Reward' 
                        messagess = f"Get reference reward {bon1} from {US.email}"
                        note = Notifications.objects.create(
                            to_user = team_admin1,
                            title = title,
                            discription =messagess
                        )
                        note.save()                                         
                        

                        if MyRefeList.objects.filter(members=team_admin1).exists():
                            is_in_any_referelist2 = MyRefeList.objects.filter(members=team_admin1)[0]
                            team_admin2 = is_in_any_referelist2.team_admin
                            BN1 = BankAccount.objects.get(account_admin = team_admin2)
                            bon2 = ammount * 0.04  # Calculate 5% of the amount
                            BN1.walet_balance = BN1.walet_balance+bon2
                            BN1.save()
                            title='Get Reward' 
                            messagess = f"Get reference reward {bon2} from {US.email}"
                            note = Notifications.objects.create(
                                to_user = team_admin2,
                                title = title,
                                discription =messagess
                            )
                            note.save()
                            
                            if MyRefeList.objects.filter(members=team_admin2).exists():
                                is_in_any_referelist3 = MyRefeList.objects.filter(members=team_admin2)[0]
                                team_admin3 = is_in_any_referelist3.team_admin
                                BN1 = BankAccount.objects.get(account_admin = team_admin3)
                                bon3 = ammount * 0.03  # Calculate 5% of the amount
                                BN1.walet_balance = BN1.walet_balance+bon3
                                BN1.save()

                                title='Get Reward' 
                                messagess = f"Get reference reward {bon3} from {US.email}"
                                note = Notifications.objects.create(
                                    to_user = team_admin1,
                                    title = title,
                                    discription =messagess
                                )
                                note.save()



                                if MyRefeList.objects.filter(members=team_admin3).exists():
                                    is_in_any_referelist4 = MyRefeList.objects.filter(members=team_admin3)[0]
                                    team_admin4 = is_in_any_referelist4.team_admin
                                    BN1 = BankAccount.objects.get(account_admin = team_admin4)
                                    bon4 = ammount * 0.02  # Calculate 5% of the amount
                                    BN1.walet_balance = BN1.walet_balance+bon4
                                    BN1.save()

                                    title='Get Reward' 
                                    messagess = f"Get reference reward {bon4} from {US.email}"
                                    note = Notifications.objects.create(
                                        to_user = team_admin4,
                                        title = title,
                                        discription =messagess
                                    )
                                    note.save()

                                    if MyRefeList.objects.filter(members=team_admin4).exists():
                                        is_in_any_referelist5 = MyRefeList.objects.filter(members=team_admin4)[0]
                                        team_admin5 = is_in_any_referelist5.team_admin
                                        BN1 = BankAccount.objects.get(account_admin = team_admin5)
                                        bon5 = ammount * 0.01  # Calculate 5% of the amount
                                        BN1.walet_balance = BN1.walet_balance+bon5
                                        BN1.save()
                                        title='Get Reward' 
                                        messagess = f"Get reference reward {bon5} from {US.email}"
                                        note = Notifications.objects.create(
                                            to_user = team_admin5,
                                            title = title,
                                            discription =messagess
                                        )
                                        note.save() 



                
                title = f'Successfully invest {ammount}$ from your main bank balence'
                disc = 'You Have Successfully Invest into QuickTrade thank you for your investment you will get reward per day from your invest ment!'
                N = Notifications.objects.create(
                    to_user = US,
                    title = title,
                    discription = disc
                )
                N.save()
                messages.info(request,"Successfully Invested!")
                return redirect('/accounts/investmoney/') 
            else:    

                return redirect('/accounts/investmoney/')

        else:
            messages.info(request,f'{AdminAprove_Status.sks}')
            return redirect('/accounts/investmoney/')





            
class DepositeFunds(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        paymentmethods = PaymentMethod.objects.filter(status = True).order_by('created_at')
        
        deposite_record = Deposite.objects.filter(admin_take = user ).order_by('-created_at')

        cp = {
            "paymentmethods":paymentmethods,
            'deposite_record':deposite_record,
        }
        return render(request,"BanckManagement/paymentsdeposite.html", context=cp)
    
    @method_decorator(login_required)
    def post(self, request):
        AdminAprove_Status = DynamicControlScheduling.objects.get(id = 1)
        if AdminAprove_Status.diposite:


            user= request.user

            data = request.POST
            tnx_address = data.get("tnx_address")       
            amount = data.get("amount")
            details = data.get("details")
            remarks = data.get('remarks')
            payadmin = PaymentMethod.objects.get(id =tnx_address )
            

            DP = Deposite.objects.create(

                    admin_take = user,

                    payadmin = payadmin,

                    Txn_Details = details,
                
                    deposite_ammount = amount,


                    remarks = remarks



            )
            DP.save()
            messages.info(request,"successfully request sent!")        

        
            return redirect('/accounts/deposite-funds/')

        messages.info(request,f'{AdminAprove_Status.sks}')
        return redirect('/accounts/deposite-funds/')














# HIGHLY SECURE##########################ADMIN WORK########## HIGHLY SECURE #







class AdminPayoutRequests(View):
    @method_decorator(login_required)
    def get(self, request):
        AdminAprove_Status = DynamicControlScheduling.objects.get(id = 1)
        if AdminAprove_Status.payout:
            user = request.user
            if user.is_superuser:

                where_i_manage = PayOut.objects.all().order_by('-created_at')
                
                cp = {
                    'where_i_manage':where_i_manage

                }

                return render(request, 'BanckManagement/admin/payoutrequests.html', context=cp)
            else:
                logout(request)
                return redirect('/')
        else:
            messages.info(request,f'{AdminAprove_Status.sks}')
            return redirect('/user/deshboard/')   
    @method_decorator(login_required)
    def post(self, request):
        AdminAprove_Status = DynamicControlScheduling.objects.get(id = 1)
        if AdminAprove_Status.payout:
            user = request.user
            if user.is_superuser:
                data = request.POST
                request_model = PayOut.objects.get(id = data.get('request_id'))
                user = request_model.admin_take
                BN = BankAccount.objects.get(account_admin = user)

                if request_model.main:
                    if BN.bank_balance>= request_model.payout_ammount + request_model.Charges:
                        BN.bank_balance = BN.bank_balance - (request_model.payout_ammount + request_model.Charges)
                        request_model.aproved_status = True
                        request_model.txn_id_binenc = data.get('tnx_id')
                        BN.save()
                        request_model.save()
                        title = 'payout successfull'
                        discripthon = f'your payout request procced {request_model.payout_ammount + request_model.Charges}$ Transfrom from your account. and you got money in binence account ac no:{request_model.binence_account} tnx id {request_model.txn_id_binenc} thanks you to trade with us! you payout from your Account'

                        n = Notifications.objects.create(
                                to_user = request_model.admin_take,
                                title = title,
                                discription = discripthon
                        )
                        n.save()
                        messages.info(request,"Successfylly Payed!")
                        return redirect('/accounts/processpayout/')
                    else:
                        messages.info(request,'insuficent fund!')
                        return redirect('/accounts/processpayout/')
                    
                

                else:
                    if BN.walet_balance>= request_model.payout_ammount + request_model.Charges:
                        BN.walet_balance = BN.walet_balance - (request_model.payout_ammount + request_model.Charges)
                        request_model.aproved_status = True
                        request_model.txn_id_binenc = data.get('tnx_id')
                        BN.save()
                        request_model.save()

                        title = 'payout successfull'
                        discripthon = f'your payout request procced {request_model.payout_ammount + request_model.Charges}$ Transfrom from your account. and you got money in binence account ac no:{request_model.binence_account} tnx id {request_model.txn_id_binenc} thanks you to trade with us! you payout from your wallet'

                        n = Notifications.objects.create(
                                to_user = request_model.admin_take,
                                title = title,
                                discription = discripthon
                        )
                        n.save()
                        messages.info(request,"Successfylly Payed!")
                        return redirect('/accounts/processpayout/')
                    else:
                        messages.info(request,'insuficent fund!')
                        return redirect(request,'/accounts/processpayout/')
            
            else:
                logout(request)
                return redirect(request,'/user/deshboard/')

        else:
            messages.info(request,f'{AdminAprove_Status.sks}')
            return redirect('/accounts/deposite-funds/')         




class AdminDepositeRequest(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        if user.is_superuser:
            deposite = Deposite.objects.filter(seenstatus = False).order_by('-created_at')

            cp = {
                'deposite':deposite
            }
            return render(request, 'BanckManagement/admin/depositerequest.html', context=cp)
        else:
            logout(request)
            return redirect('/')



    @method_decorator(login_required)
    def read(self, request, id):
           
        users = request.user
        if users.is_superuser:            

            try:
                depositeobj = Deposite.objects.get(id = id)
                depositeobj.seenstatus=True
                depositeobj.save()
                messages.info(request,"Succcessfully readed !")
                
                return redirect("/accounts/processeddeposite/")
            
            except:
                messages.info(request,"Somthing want to be worng")
                return redirect("/accounts/processeddeposite/")
        else:
            logout(request)
            return redirect("/")

        

    @method_decorator(login_required)
    def aproved(self, request, id):
        # Handle DELETE request logic here 
        users = request.user
        users = request.user
        if users.is_superuser:             

            try:
                depositeobj = Deposite.objects.get(id = id)
                admin =  depositeobj.admin_take
                depositeobj_amount = depositeobj.deposite_ammount
                BNs = BankAccount.objects.get(account_admin = admin)
                BNs.bank_balance = BNs.bank_balance+depositeobj_amount 
                BNs.save()
                depositeobj.aproved_status = True
                depositeobj.seenstatus=True
                depositeobj.save()
                messages.info(request,"Succcessfully acpected !")
                
                return redirect("/accounts/processeddeposite/")
            
            except:
                messages.info(request,"Somthing want to be worng")
                return redirect("/accounts/processeddeposite/")
        else:
            logout(request)
            return redirect("/")

        
    @method_decorator(login_required)
    def post(self, request,id):
        AdminAprove_Status = DynamicControlScheduling.objects.get(id = 1)
        if AdminAprove_Status.diposite:
            users = request.user
            if users.is_superuser:
                method = request.POST.get('_method', '').upper()
                if method == 'ACCEPT':
                    return self.aproved(request, id)
                elif method == "READ":
                    return self.read(request, id)
                else:
                    pass            


                return render(request, 'BanckManagement/admin/depositerequest.html')
                
            else:
                logout(request)
                return redirect(request,'/user/deshboard/')
        else:    
            messages.info(request,f'{AdminAprove_Status.sks}')
            return redirect('/accounts/processeddeposite/') 

##############################################################################

# class SentReward(View):
#     def get(self, request, sk):
#         sks = DynamicControlScheduling.objects.get(id = 1)
#         SecretKey = sks.sks
#         if sk == SecretKey:
#             min_wallet_balance = 25.00
#             # Query accounts with a wallet balance greater than or equal to the minimum
#             eligible_accounts = BankAccount.objects.filter(walet_balance__gte=min_wallet_balance)

#             tradepackeges = TradePackeges.objects.all()

#             # Loop through each eligible account
            
#             for account in eligible_accounts:
#                 daily_reward_amount = None

#                 for tpack in tradepackeges:
#                     if (account.walet_balance >= tpack.Plan_start) and (account.walet_balance <= tpack.Plan_end):
#                         daily_reward_amount = account.walet_balance*(((tpack.range_start+tpack.range_end)/2)/100)
#                         break
#                     else:
#                         pass
                        
#                 account.income_balance = F('income_balance') + daily_reward_amount
#                 account.walet_balance = F('walet_balance') + daily_reward_amount
#                 account.save()

#                 TIT = MytodaysIncome.objects.get(income_admin = account.account_admin)
#                 TIT.incomefee = daily_reward_amount
#                 TIT.save()

#                 G = GetReward.objects.create(
#                         reward_amin = account.account_admin,
#                         title = "Daily Reward",
#                         ammount = daily_reward_amount,
#                 )
               

#                         # Send a notification to the account admin
#                 subject = 'Daily Reward Notification'
#                 message = f'Dear {account.account_admin.email},\n\nYou have received a daily reward of {daily_reward_amount:.2f}.\n\nBest regards, QuickTrade'
                    
#                 N = Notifications.objects.create(
#                     to_user=account.account_admin,
#                     title=subject,
#                     discription= message
#                 )

                
                
            
#         else:
#             return redirect('/')
        
#         return redirect('/')






# class RefReward(View):
#     def get(self, request, sks):
#         sks = DynamicControlScheduling.objects.get(id = 1)
#         if sks == sks.sks:
#             user_accounts = CustomUser.objects.filter().order_by('-created_at')

#             for accounts in user_accounts:
#                 ref_list = MyRefeList.objects.get(team_admin = accounts)
#                 members = ref_list.members.all()
#                 if members:
#                     REFREWARD = 0.00
#                     for m in members:
#                         TI = MytodaysIncome.objects.get(income_admin = m)
#                         get_interest = (TI.incomefee * (5/100))

#                         REFREWARD = REFREWARD+get_interest
#                         print(REFREWARD)
                    
#                     UBN = BankAccount.objects.get(account_admin = accounts)
#                     UBN.walet_balance = UBN.walet_balance+REFREWARD
#                     UBN.income_balance = UBN.income_balance+REFREWARD
#                     MTI = MytodaysIncome.objects.get(income_admin = accounts)
#                     MTI.incomefee = MTI.incomefee + REFREWARD
#                     UBN.save()
#                     MTI.save()
#                     #print(REFREWARD)
#                     REFREWARD = 0.00
#                 else:
#                     pass




#         return redirect('/')

