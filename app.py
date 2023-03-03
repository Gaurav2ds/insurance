from flask import Flask,render_template,request
import pickle
import numpy as np
from flask_mysqldb import MySQL
import pandas as pd

app=Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Mysql@27'
app.config['MYSQL_DB'] = 'flask'
mysql=MySQL(app)


with open('model.pkl','rb')as f:
    model=pickle.load(f)


@app.route('/')
def index():
    return render_template('index.html')




@app.route('/invest',methods=['POST','GET'])
def invest():
    sex=0
    region=0
    smoker=0
    age=int(request.form["age"])
    sex1=request.form['sex'].lower()
    bmi=int(request.form['bmi'])
    children=int(request.form['children'])
    smoker1=request.form['smoker'].lower()
    region1=request.form['region'].lower()


    if sex1 =='male':
        sex =1
    elif  sex1 =='female':
        sex=0


    if smoker1 =='yes':
        smoker=1
    elif smoker1=='no':
        smoker=0

    if region1 =='southeast':
        region=3
    elif region1 =='northwest':
        region=2
    elif region1 =='southwest':
        region=1
    elif region1 =='northeast':
        region=0
    charges=model.predict([[age,sex,bmi,children,smoker,region]])
    ch=np.round(charges,2)[0].astype(int)
    cursor = mysql.connection.cursor()
    query = 'CREATE TABLE IF NOT EXISTS Insurance(Age int,Gender VARCHAR(10),BMI int,children int,smoker VARCHAR(10),region VARCHAR(100), charges int )'
    cursor.execute(query)
    cursor.execute('INSERT INTO Insurance(Age,Gender,BMI,children,smoker,region,charges) VALUES(%s,%s,%s,%s,%s,%s,%s)',(age,sex1,bmi,children,smoker1,region1,ch))
    cursor.execute('SELECT * FROM Insurance ')
    data=cursor.fetchall()
    df=pd.read_csv(r"C:\Users\chordiyg\Downloads\SVM\insurance.csv")
    df1=pd.DataFrame(data,columns=df.columns)
    print(df1)



    
    
    df1.to_csv('insurance.csv',mode='a',index=False,header=False)
    mysql.connection.commit()
    cursor.close()












    return render_template('index.html',output=np.round(charges[0],2))


if __name__ == "__main__":
    app.run(host = '127.0.0.100',debug=True)