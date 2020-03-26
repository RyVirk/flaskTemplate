import pymysql
from baseObject import baseObject
class customerList(baseObject):
    #this is the assignment
    def __init__(self):
        self.setupObject('customers')
        
    def verifyNew(self,n=0):
        self.errorList = []
        
        if len(self.data[n]['fname']) == 0:
            self.errorList.append("First name cannot be blank.")
        if len(self.data[n]['lname']) == 0:
            self.errorList.append("Last name cannot be blank.")    
        if len(self.data[n]['email']) == 0:
            self.errorList.append("Email cannot be blank.")
        if len(self.data[n]['password']) == 0:
            self.errorList.append("Password cannot be blank.")    
        elif len(self.data[n]['password']) < 4:
            self.errorList.append("Password cannot be shorter than 4 characters.")      
        if len(self.data[n]['subscribed']) == 0:
            self.errorList.append("Subscribed cannot be blank.")   
#email must haves
        if "." not in self.data[n]['email']:
            self.errorList.append("Email must include a period.")
        elif "@" not in self.data[n]['email']:
            self.errorList.append("Email must include @ symbol.")
#not sure on subscribed boolean
        if not ((self.data[n]['subscribed'] == "True") or (self.data[n]['subscribed'] == "False")):
            self.errorList.append("Subscribed must be True or False")
            
            
            
    def tryLogin(self,email,pw):
        sql = 'SELECT * FROM `' + self.tn + '` WHERE `email` = %s AND `password` = %s;'
        tokens = (email,pw)
        self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        #print(sql)
        #print(tokens)
        cur.execute(sql,tokens)
        self.data = []
        n=0
        for row in cur:
            self.data.append(row)
            n+=1
        if n > 0:
            return True
        else:
            return False
    
    
    
    
    
    
    
    
        