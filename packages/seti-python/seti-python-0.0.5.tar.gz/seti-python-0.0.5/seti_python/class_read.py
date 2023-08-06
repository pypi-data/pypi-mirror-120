
from seti_python.class_tools import BasicResponse

class Commissions:
    fixed:int
    percentage:int
    def  __init__(self,data):
        self.fixed=data["fixed"]
        self.percentage=data["percentage"]
        
class Taxes:
    ICA: 0
    FTE: 0
    IVA: 0
    def  __init__(self,data):
        self.ICA=data["ICA"]
        self.FTE=data["FTE"]
        self.IVA=data["IVA"]
    
        

# Read Payment
class ResponseReadPaymentData:
    commission :str
    currency:str
    description:str
    payer_email:str
    payer_name:str
    payment_id:str
    payment_method_type:str
    payment_status:str
    redirect_url:str
    reference:str
    timestamp:dict
    url :str
    value :int
    taxes : Taxes
    commission:Commissions
    def __init__(self,data:dict):
        try:
            self.commission =data['commission']
            self.currency= data["currency"],
            self.description= data["description"],
            self.payer_email=data["payerEmail"],
            self.payer_name= data["payerName"],
            self.payment_id= data["paymentId"],
            self.payment_method_type= data["paymentMethodType"],
            self.payment_status= data["paymentStatus"],
            self.redirect_url=data["redirectUrl"],
            self.reference= data["reference"],
            self.timestamp= data["timestamp"],
            self.url = data["url"]
            self.value = data["value"]
            self.taxes = Taxes(data['taxes'])
            self.commission= Commissions(data['commission'])
        except Exception:
            return
                
class ResponseReadPayment(BasicResponse):
    data: ResponseReadPaymentData
    def __init__(self,data:dict):
        self.msg=data['msg']
        self.res=data['res']
        self.data = ResponseReadPaymentData(data['data'])


# Read Cash

class ResponseReadCashData:
    balance:int
    currency:str
    currency_name:str
    def __init__(self,data:dict):
        self.balance = data['balance']
        self.currency =  data['currency']
        self.currency_name = data['currencyName']
        
class ResponseReadCash(BasicResponse):
    data: ResponseReadPaymentData
    def __init__(self,data:dict):
        self.msg=data['msg']
        self.res=data['res']
        self.data = ResponseReadPaymentData(data['data'])
        
        
# Read total CashOUts

class ResponseReadCashOutData:
    total_cashout:int
    currency:str
    currency_name:str
    def __init__(self,data:dict):
        self.total_cashout = data['totalCashout']
        self.currency =  data['currency']
        self.currency_name = data['currencyName']
        
class ResponseReadCashOut(BasicResponse):
    data: ResponseReadCashOutData
    def __init__(self,data:dict):
        self.msg=data['msg']
        self.res=data['res']
        self.data = ResponseReadCashOutData(data['data'])


# Read transactions

class Transaction:
    currency_id:str
    from_nusiness_id:str
    cash_out_id:str
    currency_id:str
    value:int
    to_wallet_id:str
    from_wallet_id:str
    timestamp:dict
    to_business_id:str
    payment_id:str
    transaction_iype:str
    id:str
    def  __init__(self,data):
        self.currency_id=data["currencyId"]
        self.from_nusiness_id=data["fromBusinessId"]
        self.cash_out_id=data["cashOutId"]
        self.currency_id=data["currencyId"]
        self.value=data["value"]
        self.to_wallet_id=data["toWalletId"]
        self.from_wallet_id=data["fromWalletId"]
        self.timestamp=data["timestamp"]
        self.to_business_id=data["toBusinessId"]
        self.payment_id=data["paymentId"]
        self.transaction_iype=data["transactionType"]
        self.id=data["id"]
  
class ResponseReadTransactionsData:
    def __init__(self,data:dict):
        self.incoming = list(map(Transaction,data['incoming']))
        self.outgoing =  list(map(Transaction,data['outgoing']))
        
class ResponseReadTransactions(BasicResponse):
    data: ResponseReadTransactionsData
    def __init__(self,data:dict):
        self.msg=data['msg']
        self.res=data['res']
        self.data = ResponseReadTransactionsData(data['data'])
   