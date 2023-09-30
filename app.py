from flask import Flask,flash,render_template,request,url_for,session,redirect
#pip install flask-sqlalchemy   to install sqlalchemy in your system
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from datetime import datetime

app=Flask(__name__)
               #your secret key ,it adds more security to our backend servers
app.secret_key="your_secret_key"

#create a Schema in MySQL and add the below mentioned configurations codes as per your mysql username & passwords !
                #Unique Resource Identifier                           #username#password#host#databasename
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:632765@localhost/margdarshan' 

 
# Create a SQLAlchemy instance
db = SQLAlchemy(app)
#FOR migrating database , Migrating helps to manipulate database with two comments,
migrate=Migrate(app,db)

#ORM model For Database , It will create a Db table as per our codes !
class Edtech(db.Model):
  course_id=db.Column(db.Integer,primary_key=True)
  title=db.Column(db.String(100),nullable=False)
  description=db.Column(db.String(10000),nullable=False)
  date=db.Column(db.DateTime,default=datetime.utcnow)
  #After creating DB model, include commands such as : 
 #1-    flask db init
 #2-    flask db migrate
 #3-    flask db upgrade


@app.route('/error')
def errror():
   return render_template('error.html')

@app.route('/')
@app.route('/home')
def home():
   list=Edtech.query.all()

   return render_template("home.html",list=list)

#REST API  
@app.route('/create',methods=['GET','POST'])
def create():
  if request.method=='POST':
    title=request.form['title']
    description=request.form['description']
    date=datetime.utcnow()

    new=Edtech(title=title,description=description,date=date)

    if new:
       db.session.add(new)
    #it will store details through session
       db.session.commit()
    
       return redirect('/home')
    else:
         #i created a default error page  
         return render_template('error.html')

       
  return render_template('new_course.html')

#Route for Edit course
@app.route('/edit_course/<int:course_id>',methods=['POST','GET'])
def edit(course_id):
   edit_course=Edtech.query.get_or_404(course_id)
   if request.method=='POST':
     
     edit_course.title=request.form['title']
     edit_course.description=request.form['description']

     if edit_course:
        db.session.commit()
        return redirect(url_for('home',course_id=edit_course.course_id))
     else:
          return render_template('error.html')

     
   return render_template('edit.html',edit_course=edit_course)


@app.route('/list')
def list_course():
   list=Edtech.query.all()

   if list:
     return render_template('list.html',list=list)
   else:
      return  render_template('error.html')
   
   
@app.route('/ind_course/<int:course_id>',methods=['GET','POST'])
def individual(course_id):
   ind=Edtech.query.get_or_404(course_id)

   if ind:
     db.session.commit()
     return render_template('ind_course.html',ind=ind)
   else:
      return render_template('error.html')

@app.route('/delete/<int:course_id>',methods=['GET','POST'])
def delete_course(course_id):
        #dbtabel name 
   delete=Edtech.query.get_or_404(course_id)
   if delete:
     db.session.delete(delete)
     db.session.commit()    
   #after deleting a course ,it will redirect to mentioned route !s
     return redirect(url_for('home'))
   else:
       return render_template('error.html')



if __name__ == '__main__':
    app.run(debug=True)
