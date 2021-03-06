from flask import Flask
from flask import render_template
from flask import request,session, redirect, url_for, escape,send_from_directory,make_response 

from customer import customerList

import pymysql 
import json
import time

from flask_session import Session  #serverside sessions

app = Flask(__name__,static_url_path='')
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

@app.route('/set')
def set():
    session['time'] = time.time()
    return 'set'

@app.route('/get')
def get():
    return str(session['time'])
    
@app.route('/login',methods = ['GET','POST'])
def login():
    '''
    -check login
    -set session
    -redirect menu
    --check session on login page
    '''    
    if request.form.get('email') is not None and request.form.get('password') is not None:
        c = customerList()
        if c.tryLogin(request.form.get('email'),request.form.get('password')):
            print('login ok')
            session['user'] = c.data[0]
            session['active'] = time.time()
            
            return redirect('main')
        else:
            print('login failed')
            return render_template('login.html', title='Login', msg='Incorrect username or password')     
    else:
        if 'msg' not in session.keys() or session['msg'] is None:
            m = 'Type your email and password to continue.'
        else: 
            m = session['msg']
            session['msg'] = None    
        return render_template('login.html', title='Login', msg=m)    

@app.route('/logout',methods = ['GET','POST'])
def logout():
    del session['user']
    del session['active'] 
    return render_template('login.html', title='Login', msg='You have logged out.') 

@app.route('/basichttp')
def basichttp():
    if request.args.get('myvar') is not None:
        return 'your var:' + request.args.get('myvar')
    else:
        return 'myvar not set' 

@app.route('/')
def home():
    return render_template('test.html', title='Test', msg='Welcome!')

@app.route('/index')
def index():
    user = {'username': 'Tyler'}
        
    
    items = [
        {'name':'Apple','price':2.34},
        {'name':'Orange','price':4.88},
        {'name':'Grape','price':2.44}
    ]
    return render_template('index.html', title='Home', user=user, items=items)

@app.route('/customers')
def customers():
    c = customerList()
    c.getAll()
    
    print(c.data)
    #return ''
    return render_template('customers.html', title='Customer List', customers=c.data)


@app.route('/customer')
def customer():
    c = customerList()
    if request.args.get(c.pk) is None:
       return render_template('error.html', msg='No customer id given')

    
    c.getById(request.args.get(c.pk))
    if len(c.data) <= 0:
        return render_template('error.html', msg='Customer not found')
            
    
    print(c.data)
    #return ''
    return render_template('customer.html', title='Customer', customer=c.data[0])

@app.route('/newcustomer',methods = ['GET','POST'])
def newcustomer():
    if request.form.get('fname') is None:
        c = customerList()
        c.set('fname','')
        c.set('lname','')
        c.set('email','')
        c.set('password','')
        c.set('subscribed','')
        c.add()      
        return render_template('newcustomer.html', title='New Customer', customer=c.data[0]) 
    else:
        c = customerList()
        c.set('fname',request.form.get('fname'))
        c.set('lname',request.form.get('lname'))
        c.set('email',request.form.get('email'))
        c.set('password',request.form.get('password'))
        c.set('subscribed',request.form.get('subscribed'))
        c.add()  
        if c.verifyNew():     
            c.insert()
            print(c.data)
            return render_template('savedcustomer.html', title='Customer Saved', 
            customer=c.data[0])
        else:    
            return render_template('newcustomer.html', title='Customer Not Saved', 
            customer=c.data[0],msg=c.errorList)
        
@app.route('/savecustomer',methods = ['GET','POST'])
def savecustomer():
        c = customerList()
        c.set('id',request.form.get('id'))
        c.set('fname',request.form.get('fname'))
        c.set('lname',request.form.get('lname'))
        c.set('email',request.form.get('email'))
        c.set('password',request.form.get('password'))
        c.set('subscribed',request.form.get('subscribed'))
        c.add()  
        c.update()
        print(c.data)
        #return ''
        return render_template('savedcustomer.html', title='Customer Saved', customer=c.data[0])        

@app.route('/main')
def main():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    userinfo = 'Hello, ' + session['user']['fname']
    return render_template('main.html', title='Main Menu',msg = userinfo)
    
def checkSession():
    if 'active' in session.keys():    
        timeSinceActivity = time.time() - session['active']
        print(timeSinceActivity)
        if timeSinceActivity > 500:
            session['msg'] = 'Your session has timed out.'
            return False
        else:    
            session['active'] = time.time()
            return True
    else:
        return False

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
   app.secret_key = '1234'
   app.run(host='127.0.0.1',debug=True)