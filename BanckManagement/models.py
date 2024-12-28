from django.db import models
from AuthApp.models import CustomUser

# Create your models here.


class BankAccount(models.Model):
    account_admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='bankaccount')


    bank_balance = models.FloatField(default=0.00)### main balance

    walet_balance = models.FloatField(default=0.00)### main balance

    income_balance = models.FloatField(default=0.00) ## Total income

    admin_status = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.account_admin.email} {self.account_admin.nid_no}'






class InvastMents(models.Model):
    investor = models.ForeignKey(CustomUser, on_delete= models.CASCADE)

    BN = models.ForeignKey(BankAccount, on_delete=models.DO_NOTHING, null=True, blank=True)

    Payment_Method = models.CharField(max_length=100, default="USDT")

    Txn_Details = models.CharField(max_length=250, null=True, blank=True)
   
    inv_ammount = models.FloatField(default=25.00)

    Charges = models.FloatField(default=0.00, null=True, blank=True)

    aproved_status = models.BooleanField(default=False)

    remarks = models.CharField(max_length=25)

    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.investor.email} {self.investor.nid_no}'






class PayOut(models.Model):
    admin_take = models.ForeignKey(CustomUser, on_delete= models.CASCADE)

    BN = models.ForeignKey(BankAccount, on_delete=models.DO_NOTHING, null=True, blank=True)

    Payment_Method = models.CharField(max_length=100, default="USDT")

    Txn_Details = models.CharField(max_length=250)
   
    payout_ammount = models.FloatField(default=25.00)

    Charges = models.FloatField(default=0.00)

    aproved_status = models.BooleanField(default=False)
    removed_status = models.BooleanField(default=False)

    main = models.BooleanField(default=False)

    txn_id_binenc = models.CharField(max_length=150, null=True, blank=True)

    binence_account = models.CharField(max_length=50, null=True, blank=True)

    remarks = models.CharField(max_length=25)

    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.admin_take.email} {self.admin_take.nid_no}'



class WaletShate(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete= models.CASCADE)

    to_user = models.ForeignKey(CustomUser, on_delete= models.CASCADE, related_name = 'waletshare')

    Payment_Method = models.CharField(max_length=100, default="USDT")

    Txn_Details = models.CharField(max_length=250)
   
    share_ammount = models.FloatField(default=0.00)

    main_account = models.BooleanField(default=False)

    Charges = models.FloatField(default=0.00)

    aproved_status = models.BooleanField(default=False)

    txn_id_binenc = models.CharField(max_length=150, null=True, blank=True)

    remarks = models.CharField(max_length=25)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.from_user.email} {self.from_user.nid_no}'
    



class TradePackeges(models.Model):
    title = models.CharField(max_length=150)

    range_start = models.FloatField(null=True, blank=True)
    range_end = models.FloatField(null=True, blank=True)

    Plan_start = models.FloatField(null=True, blank=True)
    Plan_end = models.FloatField(null=True, blank=True)
    
    ReturnType = models.CharField(max_length=100)
    TotalEarning = models.CharField(max_length=100)

    charge = models.FloatField(null=True, blank=True)

    status = models.BooleanField(default=True)
    
    bonus = models.FloatField(default=1.5)
    def __str__(self):
        return f'{self.title}'
    


class GetReward(models.Model):
    reward_amin = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length =100, null=True, blank=True)
    ammount = models.CharField(max_length =100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.reward_amin.email}'




class PaymentMethod (models.Model):
    Payment_Name = models.CharField(max_length=100)
    PayAddress = models.CharField(max_length=250)
    Qrcode  = models.ImageField(upload_to="qrimage")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.Payment_Name}"




class Deposite(models.Model):
    admin_take = models.ForeignKey(CustomUser, on_delete= models.CASCADE)

    payadmin = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True, blank=True)

    Txn_Details = models.CharField(max_length=250)
   
    deposite_ammount = models.FloatField(default=25.00)

    Charges = models.FloatField(default=0.00)

    aproved_status = models.BooleanField(default=False)

    seenstatus = models.BooleanField(default=False)

    txn_id_binenc = models.CharField(max_length=150, null=True, blank=True)

    remarks = models.CharField(max_length=25)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.admin_take.email} {self.admin_take.nid_no}'

