from flask import Flask, render_template , request,flash,redirect, session
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

from sqlalchemy.orm import sessionmaker,declarative_base

import sqlalchemy.orm


e=create_engine('sqlite:///sers.db')
sess=sessionmaker(bind=e)
ses=sess()
meta=MetaData()
base=declarative_base()

class users(base):

    def __init__(self,email,fname,lname,passwd):
        self.email=email
        self.fname=fname
        self.lname=lname
        self.passwd=passwd
    __tablename__="users"
    email = Column(String(50),primary_key=True)
    fname = Column(String(20))
    lname = Column(String(20))
    passwd = Column(String(40))
    
      



obj=users('s','s','s','s')
print(obj)

app = Flask(__name__,static_url_path='/Static')


app.config['SECRET_KEY']='%lkyg((t5*65UYf^jGF7$b7HJg4fk2Y22f'


@app.route('/')
def hello_world():
    return render_template("index.html")





@app.route('/about')
def about():
    return (render_template('about.html'))







@app.route('/calculator',methods=["GET","POST"])
def calculator():
    try:
        print('=========head======',"\n")
        print(request.method)
        if request.method=='POST':
            btn=request.form['btn']
            if btn=='clrbtn':
                return (render_template("calculator.html",ans=''))
            num1=(request.form['num1'])
            num2=request.form['num2']
            if num1 != '' and num2 !='':
                num1=int(num1)
                num2=int(num2)
                if btn=="addbtn":
                    ans=num1+num2
                elif btn=='subbtn':
                    ans=num1-num2
                elif btn=='mulbtn':
                    ans=num1*num2
                elif btn=='divbtn':
                    ans=num1/num2     
                ans=str(ans)
                print(request.form)
                return (render_template("calculator.html",ans=ans))
            else:
                print(request.form)
                return (render_template("calculator.html",ans=request.form['output']))     
        else:
            print(request.form) 
            return (render_template("calculator.html",ans=''))
    except:
            return (render_template("calculator.html",ans='ERROR'))        







@app.route('/jee')
def jee():
    return(render_template('jee.html'))


@app.route('/register',methods=["GET","POST"])
def resgiter():
    if request.method=='GET':
        return(render_template('register.html',alert_text=""))
    elif request.method=="POST":
        try:
            fname=str(request.form['f_name'].strip())
            lname=str(request.form['l_name'].strip())
            email=str(request.form['email'].strip())
            passwd1=str(request.form['passwd1'].strip())
            passwd2=str(request.form['passwd2'].strip())
            print(fname,lname,email,passwd1,passwd2)
            
            if fname=="" or lname=="" or email=='' or passwd1=='' or passwd2=='':
                return(render_template('register.html',alert_text="Fields Can Not Be Empty!!"))
            else:    
                if passwd1==passwd2:
                    ses.rollback()
                    entry_obj=users(email=email,fname=fname,lname=lname,passwd=passwd1)
                    ses.add(entry_obj)
                    ses.commit()
                    return(render_template('register.html',alert_text="Account created succesfully!"))
                else:
                    return(render_template('register.html',alert_text="Passwords didn't match !!"))

        except:
            return(render_template('register.html',alert_text="User Already exists"))

        
    else:
        return ("ERROR")        







@app.route('/user')
def user():
    
    if 'logging_status' in session:
        if session['logging_status']:
            return("Logged IN")
        else:
            return ("Logged out")
    else:
        return("LOGIN FIRST")

 
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=="GET":
        return(render_template('login.html',alert_text=""))
    elif request.method=="POST":
        print(request.form)
        email=request.form['email'].strip()
        passwd=request.form['passwd'].strip()
        
        for entry_obj in ses.query(users).all():
            if entry_obj.email==email:
                if(entry_obj.passwd==passwd):
                    session['logging_status']=True
                    return(redirect('/user'))
                else:
                    return(render_template('login.html',alert_text="Wrong password")) 
            else:
                return(render_template('login.html',alert_text="User Doesn't Exist!"))
        
        

    else:
        return("ERROR")




@app.route('/expt')
def expt():
    return(render_template('experiments.html'))





@app.route('/dashboard')
def dash():
    return(render_template('dashboard.html'))

@app.route('/dashboard/profile')
def dash_profile():
    return(render_template('dashboard_profile.html'))

@app.route('/dashboard/assignments')
def dash_assign():
    return(render_template('dashboard_assignments.html'))

@app.route('/dashboard/results')
def dash_result():
    return(render_template('dashboard_results.html'))


# if __name__=="__main__":
    

#     app.run(debug=True)

