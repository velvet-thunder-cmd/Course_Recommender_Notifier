import twilio
import json
import boto3
import requests
s3client = boto3.client('s3')
def lambda_handler(event, context):
    
    data = s3client.get_object(Bucket='spam-hw003buck001-178bfyk4b96fd', Key='100001/20180223/hello.txt')            
    k=''
    for line in data['Body'].iter_lines(): 
        k=line
    bb=k
        
    g=requests.get("https://schedge.a1liu.com/2022/sp/gy/cs")
    l=[]
    for i in g.json():
        d=[]
        d.append(i["name"])
        d.append(i["sections"][0]["status"])
        l.append(d)
            
        
    string = str(l)
    encoded_string = string.encode("utf-8")
        
    bucket_name = "spam-hw003buck001-178bfyk4b96fd"
    file_name = "hello.txt"
    s3_path = "100001/20180223/" + file_name
    a=encoded_string
    s3 = boto3.resource("s3")
    s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_string)
    lis=[]
    for iim,jjm in eval(bb.decode("utf8")):
        k=[]
        k.append(iim)
        k.append(jjm)
        lis.append(k)
    lly=[]
    for ii,jj in eval(a.decode("utf8")):
        kk=[]
        kk.append(ii)
        kk.append(jj)
        lly.append(kk)
    for il,jl in zip(lly,lis):
        if il==jl:
            continue
        else:
                
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('login')
            names=[]
            phonenumber=[]
            ress=[]
            res=table.scan()["Items"]
                
            for ipo in res:
                    
                if ipo['course']==il[0]:    
                    val=[]
                    val.append(ipo['phonenumber'])
                    val.append(ipo['name'])
                    ress.append(val)
                
            for num,names in ress:
                messageToSend=""
                if il[1]=="Open":
                                
                    messageToSend ="Hi"+" "+names +" "+il[0]+" "+"is open now"
                                
                    response=twilio.send_sms({
                                    "To":num,
                                    "From":"+14842554726",
                                    "Body":messageToSend
                    })