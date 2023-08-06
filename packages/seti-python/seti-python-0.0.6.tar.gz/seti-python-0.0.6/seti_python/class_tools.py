class BasicResponse:
    msg:str
    res:int
    
    
class ResponseCreateTransactionData:
    transaction_id:str
    def __init__(self,data:dict):
        try:
            self.transaction_id =data['transactionId']
        except Exception:
            return
                
class ResponseCreateTransaction(BasicResponse):
    data: ResponseCreateTransactionData
    def __init__(self,data:dict):
        self.msg=data['msg']
        self.res=data['res']
        self.data = ResponseCreateTransactionData(data['data'])