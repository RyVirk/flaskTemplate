import pymysql
from baseObject import baseObject

class productList(baseObject): 
    
    def __init__(self):
        self.setupObject('products')
    
#assignment        
    def verifyNew(self,n=0):
        self.errorList = []
        
        if len(self.data[n]['sku']) == 0:
            self.errorList.append("SKU cannot be blank.")           
        if len(self.data[n]['name']) == 0:
            self.errorList.append("Name cannot be blank.")
            


        if self.data[n]['price'] == 0:
            self.errorList.append("Price cannot be 0.")    
  
        pf = None
        try:
            pf = float(self.data[n]['price'])
        except:
            self.errorList.append()
        
        if pf is not None:
            if pf > 0:
                self.data[n]['price'] = pf
            else:
                self.errorList.append("Price must be a decimal.")

       
        
        
        if len(self.errorList) > 0:
            return False
        else: 
            return True
    


#PID NO CHECK
#SKU CANT BE BLANK
#NAME CANT BE BLANK
#PRICE MUST BE A DECIMAL & GREATER THAN 0    