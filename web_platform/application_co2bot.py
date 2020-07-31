# -*- coding: utf-8 -*-
import flask
from flask import *
from flask import Flask
from flask import request
from flask import jsonify
import sys
import json
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from urllib import parse
import urllib.request
import pandas as pd

from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity

#jwt 인증
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)

import pymysql
hoststr = "localhost"
usrstr = "root"
passwordstr = "co2bot2020!"
dbstr = "Chatbot"

application = Flask("co2bot")
application.config['JWT_TOKEN_LOCATION'] = ['cookies']
application.config['JWT_ACCESS_COOKIE_PATH'] = '/api'
application.config['JWT_REFRESH_COOKIE_PATH'] = '/'
application.config['JWT_COOKIE_CSRF_PROTECT'] = False
application.config['JWT_SECRET_KEY'] = 'co2bot' 
application.config['SESSION_COOKIE_HTTPONLY'] = False 
application.config['CSFR_COOKIE_HTTPONLY'] = False

#application.config['JWT_COOKIE_SECURE'] = False
#application.config['PERMANENT_SESSION_LIFETIME'] = 2678400
#application.config.update(SESSION_COOKIE_SECURE=False,SESSION_COOKIE_HTTPONLY=False,)

api = Api(application)

jwt = JWTManager(application)

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    conn = pymysql.connect(host=hoststr, user=usrstr, password=passwordstr, db=dbstr, charset='utf8')
    username = ""
    usertype = ""
    
    try:
        cursor = conn.cursor()
        sql = " select UserName, UserType from USER_INFO  "
        sql +=" where UserID = '"+identity+"'  "
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        returnValue = 0
        for data in result:
            username = data[0]
            usertype = data[1]
            print(username)
            print(usertype)
            
    finally:
        conn.close()   
            
    return {
        'username': username,
        'usertype': usertype
        }

@application.route('/api/user', methods=['POST', 'GET'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    
    conn = pymysql.connect(host=hoststr, user=usrstr, password=passwordstr, db=dbstr, charset='utf8')
    try:
        cursor = conn.cursor()
        sql = " select UserName from USER_INFO  "
        sql +=" where UserID = '"+email+"'  "
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        returnValue = 0
        for data in result:
            print(data[0])
            returnValue = data[0]
            
        if returnValue == 0:
            return jsonify({'login': False}), 401
    finally:
        conn.close()    
    
    KST = timezone('Asia/Seoul')
    now = datetime.utcnow()
    today_dt = utc.localize(now).astimezone(KST) 
    
    application.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
    )
    
    expires_delta = timedelta(days=1)
    access_token = create_access_token(identity=email, expires_delta=expires_delta )
    refresh_token = create_refresh_token(identity=email, expires_delta=expires_delta )

    resp = jsonify({'login': True})
    #set_access_cookies(resp, access_token) 
    #set_refresh_cookies(resp, refresh_token)
    
    resp.set_cookie(key="access_token_cookie", value=access_token, httponly=False)

    print(resp.headers)
    print(resp.json)
    print(access_token)
    
    return resp, 200

def getUserType(Userid) :
    conn = pymysql.connect(host=hoststr, user=usrstr, password=passwordstr, db=dbstr, charset='utf8')
    try:
        cursor = conn.cursor()
        sql = " select UserType from USER_INFO  "
        sql +=" where UserID = '"+Userid+"'  "
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        returnValue = 0
        for data in result:
            print(data[0])
            returnValue = data[0]

    finally:
        conn.close()  
        
    return returnValue

@application.route('/global')
def Global():
	return render_template('global.html')

@application.route('/producer')
def Producer():
	return render_template('producer.html')

@application.route("/api/public/monthhistory" , methods=['GET'])
#@jwt_required
def getCarbonEmissionPubicHistory():
    
    conn = pymysql.connect(host=hoststr, user=usrstr, password=passwordstr, db=dbstr, charset='utf8')
    df = ""
    try:
        sql = " select A.*, IFNULL(B.Remarks,'') Remarks from "
        sql +=" (select "
        sql +=" CARBON_LOG.Userid, USER_INFO.UserName, USER_INFO.UserType, Sum(Amount) as Amount, Sum(Amount*90*0.01) as Cost, DATE_FORMAT(Insert_Dt,'%Y-%m-%d') as Insert_Dt "
        sql +=" from CARBON_LOG  "
        sql +=" left join USER_INFO on CARBON_LOG.Userid = USER_INFO.Userid "
        sql +=" group by CARBON_LOG.Userid, USER_INFO.UserName, USER_INFO.UserType, DATE_FORMAT(Insert_Dt,'%Y-%m-%d') "
        sql +=" order by Insert_Dt desc, Sum(Amount) desc) A "
        sql +=" left join PENALTY_INFO B on A.Userid = B.Userid and DATE_FORMAT(A.Insert_Dt,'%Y-%m-%d') = DATE_FORMAT(B.Insert_Dt,'%Y-%m-%d') "
    
        df = pd.read_sql_query(sql,conn)
        print(df)
    finally:
        conn.close()
        
    return df.to_json(orient='records')

@application.route("/api/public/monthamount" , methods=['GET'])
#@jwt_required
def getCarbonEmissionPubicAmount():
    
    conn = pymysql.connect(host=hoststr, user=usrstr, password=passwordstr, db=dbstr, charset='utf8')
    df = ""
    try:
        sql = " select CARBON_LOG.Userid, USER_INFO.UserName, Sum(Amount) as Amount, Sum(Amount*90*0.01) as Cost from CARBON_LOG  "
        sql +=" left join USER_INFO on CARBON_LOG.Userid = USER_INFO.Userid "
        sql +=" group by CARBON_LOG.Userid, USER_INFO.UserName "
        sql +=" order by Sum(Amount) desc "
    
        df = pd.read_sql_query(sql,conn)
        print(df)
    finally:
        conn.close()
        
    return df.to_json(orient='records')

@application.route("/api/<userid>/time-amount" , methods=['GET'])
#@jwt_required
def getCarbonEmissionTimeHistory(userid):
    
    conn = pymysql.connect(host=hoststr, user=usrstr, password=passwordstr, db=dbstr, charset='utf8')
    df = ""
    try:
        sql = " select Amount, DATE_FORMAT(Insert_Dt,'%H') as Insert_Dt  from CARBON_LOG  "
        sql +=" left join USER_INFO on CARBON_LOG.Userid = USER_INFO.Userid "
        sql +=" where CARBON_LOG.UserID = '"+userid+"' and DATE_FORMAT(Insert_Dt,'%Y-%m-%d') "
        sql +=" = (select max(DATE_FORMAT(Insert_Dt,'%Y-%m-%d')) from "
        sql +=" CARBON_LOG where CARBON_LOG.UserID = '"+userid+"') "
        sql +=" order by DATE_FORMAT(Insert_Dt,'%H') "
    
        df = pd.read_sql_query(sql,conn)
        print(df)
    finally:
        conn.close()
        
    return df.to_json(orient='records')

@application.route("/api/<userid>/amount" , methods=['GET'])
#@jwt_required
def getCarbonEmissionHistory(userid):
    
    conn = pymysql.connect(host=hoststr, user=usrstr, password=passwordstr, db=dbstr, charset='utf8')
    df = ""
    try:
        sql = " select CARBON_LOG.Userid, USER_INFO.UserName, Sum(Amount) as Amount, DATE_FORMAT(Insert_Dt,'%Y-%m-%d') as Insert_Dt from CARBON_LOG  "
        sql +=" left join USER_INFO on CARBON_LOG.Userid = USER_INFO.Userid "
        sql +=" where CARBON_LOG.UserID = '"+userid+"' "
        sql +=" group by CARBON_LOG.Userid, USER_INFO.UserName, DATE_FORMAT(Insert_Dt,'%Y-%m-%d') "
        sql +=" order by Insert_Dt desc "
    
        df = pd.read_sql_query(sql,conn)
        print(df)
    finally:
        conn.close()
        
    return df.to_json(orient='records')

@application.route('/public')
def Public():
	return render_template('public.html')

@application.route('/ngo')
def Ngo():
	return render_template('ngo.html')


@application.route('/kor')
def Main():
    return render_template('home.html')


@application.route('/')
def Main_Eng():
    return render_template('home_eng.html')


@application.route("/getCarbonEmissions" , methods=['POST', 'GET'])
def getCarbonEmissions():
    pType = request.args.get('type')
    pDate = request.args.get('Date')
    print(pType)
    print(pDate)
    
    vehicleId = parse.quote("byc3230-iot-0008")
    url = "http://ithaca-klaytn.ml:9000/co2/"+vehicleId
    url_data = urllib.request.urlopen(url)
    jsonString = url_data.read().decode("utf-8")
    json_str = json.dumps(jsonString)
    resp = json.loads(jsonString)
    print(resp)
    totalUsageValue = str(resp['totalUsage'])
    return { "totalUsage" : totalUsageValue }
    
@application.route("/callNLP")
def callNLP():
    question = request.args.get('question')
    print(question)
    authenticator = IAMAuthenticator('1gR3LB1WjGbyLDWM-cvUUg5QlFDK2LSzy5Z55b9FZwaH')
    assistant = AssistantV2(version='2020-04-01', authenticator = authenticator)

    assistant.set_service_url('https://api.au-syd.assistant.watson.cloud.ibm.com/instances/45e4a82e-f647-4a5c-866b-69fae0086057') #root 의 url
    
    response = assistant.create_session(assistant_id='315b8e12-6ee1-48e4-b35c-dcc6a3172b94').get_result() #Carbon_Tax_Bot assistant ID
    
    session_real_id = response["session_id"]
    print(session_real_id)
    response = assistant.message(assistant_id='315b8e12-6ee1-48e4-b35c-dcc6a3172b94', session_id=session_real_id, input={'message_type': 'text','text': question}).get_result()

    print(json.dumps(response, indent=2))
    return response

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8080)
