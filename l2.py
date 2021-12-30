import boto3
import time 
import pandas as pd
import os
import openpyxl 
import boto3 
import json
client=boto3.client('lambda')

def lambda_handler(event, context):
    
    loc = ("s3://courserecommender/Coursedata.xlsx")
    df=pd.read_excel('s3://courserecommender/Coursedata.xlsx', engine='openpyxl') 
    k=json.loads(df.to_json(orient="records"))
    d={"names":event} 
    k.insert(0,d)
    
      
    
    response=client.invoke(
        FunctionName="arn:aws:lambda:us-west-2:224019584573:function:web",
        InvocationType="RequestResponse",
    Payload=json.dumps(k))
       
    
    rd=json.load(response["Payload"])   
    return rd
