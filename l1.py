import requests
import json
import boto3
client=boto3.client('lambda')
def lambda_handler(event, context):
  
  ro=[]
  def b(l):
    global ro
    ro=l
    print(ro)
    ss=''''''
    for iii in l:
      ss+=iii+','
    dialogAction = {
                  "type": "Close",
                  "fulfillmentState": "Fulfilled",
                  "message": {
                      "contentType": "PlainText",
                      "content": "These are the courses which are available here \n"+ss+"\n"+"Enter the courses which you have taken below"
                  }
    }
    return {"dialogAction": dialogAction}
  def a(uu,uu1,uu2):
    print(uu)
    print(uu1)
    print(uu2)
    print(ro)
    print(l)
    l.remove(uu)
    l.remove(uu1)
    l.remove(uu2)
    sk=""""""
    for ii in l:
      sk+=ii
    dialogAction = {
                  "type": "Close",
                  "fulfillmentState": "Fulfilled",
                  "message": {
                      "contentType": "PlainText",
                      "content": "These are the courses which you can take based on your intrests: \n"+sk+"\n"
                  }
    }
    return {"dialogAction": dialogAction}
  
  l=[]  
      
  if event['currentIntent']['name'] == 'branchschool':
    c=event['currentIntent']['slots']['branch']
    cc=event['currentIntent']['slots']['school']
      
    res = requests.get(f'https://schedge.a1liu.com/2022/SP/{cc}/{c}')
      
    for i in res.json():
      l.append(i["name"])
        
    return b(l)
  if event['currentIntent']['name'] == 'coursses':
    mm=[]
    print(event)
    uu=event['currentIntent']['slots']['fc']
    uu1=event['currentIntent']['slots']['sc']
    uu2=event['currentIntent']['slots']['tc']
    mm.append(uu)
    mm.append(uu1)
    mm.append(uu2)
    if len(mm)!=len(set(mm)):
      dialogAction = {
                  "type": "Close",
                  "fulfillmentState": "Fulfilled",
                  "message": {
                      "contentType": "PlainText",
                      "content": "You Cannot enter the same course multiple times"
                  }
      }
    
      return {"dialogAction": dialogAction}
    bingo=[]
    for kkk in mm:
      response=client.invoke(
        FunctionName="arn:aws:lambda:us-west-2:224019584573:function:courserecommender",
        InvocationType="RequestResponse",
      Payload=json.dumps(kkk))
      
      rd=json.load(response["Payload"]) 
      bingo.append(rd)
    print(type(bingo))
    kkl=[]
    kkls=[]
    kkm=[]
    kkms=[]
    print(bingo)
    for iim in bingo:
      kkl.append(eval(iim)[0]["Name"])
      kkls.append(eval(iim)[0]["similarity_scores"])
      kkm.append(eval(iim)[1]["Name"])
      kkms.append(eval(iim)[1]["similarity_scores"])
    
    fl=kkl+kkm 
    fln=kkls+kkms
    sda=sorted(set(fl), key=fl.index)
    sdas=sorted(set(fln), key=fln.index)
    if fl!=sorted(set(fl), key=fl.index):
      bingo=[]
      bingo1=[]
      c=0
      for ite,ite1 in zip(fl,sorted(set(fl), key=fl.index)):
        c+=1
        if ite==ite1:
          bingo.append(ite)
          bingo1.append(fln[c])
        else:
          bingo.append(sda[-c])
          bingo1.append(sdas[-c])
        if c==3:
          break
    else:
    
      if fl[:3]!=sorted(set(fl[:3]), key=fl.index):
        c=0
        bingo=[]
        bingo1=[]
        for ine,ine1 in zip(fl[:3],sorted(set(fl[:3]), key=fl.index)):
          c+=1
          if ine!=ine1:
            bingo.append(sda[-c])
            bingo1.append(sdas[-c])
          else:
            bingo.append(ine)
            bingo.append(fln[c])
          if c==3:
            break  
      else:
        
        bingo=fl[:3]
        bingo1=fln[:3]
        if len(fl[:3])!=len(list(set(bingo))):
          c=0
          for uyt,uyt1 in zip(fl[:3],sorted(set(bingo),key=bingo.index)):
            c+=1
            bingo=[]
            bingo1=[]
            if uyt!=uyt1:
              bingo.append(sda[-c])
              bingo1.append(sdas[-c])
            else:
              bingo.append(uyt)
              bingo1.append(fln[c])
            if c==3:
              break
    cc=0
    sdaw=bingo
    llp=[]
    llp1=[]
    print(mm)
    print(sdaw)
    for iuq in sdaw:
      cc+=1
      if iuq in mm:
        print("success")
        llp.append(sda[-cc])
        llp1.append(sdas[-cc])
      else:
        print('ok')
        llp.append(iuq)
        llp1.append(fln[cc])
      if cc==3:
        break
    bingo=llp 
    bingo1=llp1
    kko=bingo 
    skde=bingo1
    bingo=''
    bingo1=''
    for sjad,sdfq in zip(kko,skde):
      bingo+=sjad+","
      bingo1+=str(sdfq)+","
      
    dialogAction = {
                  "type": "Close",
                  "fulfillmentState": "Fulfilled",
                  "message": {
                      "contentType": "PlainText",
                      "content": "These are the courses which you can take based on your intrests: \n"+bingo+" "+"and their similarity score are"+" "+bingo1+" "+"respectively."+"\n"
                  }
    }
    
    return {"dialogAction": dialogAction} 
    #return a(uu,uu1,uu2)
    
  if event['currentIntent']['name'] == 'notification':
    print(event)
    cou2=event['currentIntent']['slots']['coursesss']
    cou3=event['currentIntent']['slots']['phno']
    cou4=event['currentIntent']['slots']['name']
    lof=event['currentIntent']['slots']['email']

    table = boto3.resource('dynamodb').Table('login')

    table.put_item(Item={'name': cou4,'course':cou2,'phonenumber':cou3,'login':lof})  
    dialogAction = {
                  "type": "Close",
                  "fulfillmentState": "Fulfilled",
                  "message": {
                      "contentType": "PlainText",
                      "content": "Thank you will recieve an update is there is any change in the status"
                  }
    }
    
    return {"dialogAction": dialogAction}
