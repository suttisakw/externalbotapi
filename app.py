from flask import Flask ,request
import requests
import json
# from gevent.pywsgi import WSGIServer
app = Flask(__name__)
#  Init data
Authorization = 'Bearer mxqX1kndysCJludZ+/QYPOq/LIepFlHux/JB3mI8A+WmHK4nqC5/0ekwWn2ZlAXtHD8Eiu67VZV5Rl1+S9cFLqJIZbDsdTBwmvhDU4cIhNnrDUubXYSDd955LPEat2QZGB8PBz0W7EFfgiFhlQamagdB04t89/1O/w1cDnyilFU=' # ใส่ ENTER_ACCESS_TOKEN เข้าไป

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/callback', methods=['POST'])
def callback():
    json_line = request.get_json()
    json_line = json.dumps(json_line)
    decoded = json.loads(json_line)
    # print(decoded)
    user = decoded["events"][0]['replyToken']
    userID = decoded["destination"]
    if 'postback' in json_line:
        print('postback ' ,userID)

        data_in = decoded["events"][0]['postback']['data']
        print("poast_back " ,data_in)
        sendData = get_data_from_vesselname(data_in)
        # sendText(userID,sendData)
        # sendData = flexmessage()

    else:
        textMessage = decoded["events"][0]['message']['text']
        # print("ผู้ใช้：",user)
        textReplay= {
            'type':'text',
            'text':textMessage
        }
        if textMessage == 'Tracking Status':
            sendData = getboat()
        else:
            sendData = textReplay
    replyText(user,sendData) # Send message
    return '',200

def replyText(user, text):
    url = "https://api.line.me/v2/bot/message/reply"

    headers = {
    'Content-Type': 'application/json',
    'Authorization': Authorization
    }
    payload = json.dumps({
    "replyToken": user,
    "messages":  [text] })
    print(payload)
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

def sendText(user, text):
    url = "https://api.line.me/v2/bot/message/push"
    payload = json.dumps({
    "to": user,
    "messages": [ text  ] })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': Authorization
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


acction_VESSELNAME = {
  "type": "template",
  "altText": "this is a carousel template",
  "template": {
            "text": "โปรดเลือกรายชื่อเรือดังต่อไปนี้",
            "actions": [
              {
                "uri": "https://liff.line.me/1654368345-NEP1RlqX",
                "type": "uri",
                "label": "เลือกรายชื่อเรือ"
              }
            ],
            "type": "buttons",
            "title": "Tracking Status"
          },
          "altText": "this is a buttons template",
          "type": "template"
        }

def get_data_from_vesselname(ves_name):
    url = "https://scglmwazprd.scglogistics.co.th/api/1/rest/feed-master/queue/SCG/CBM_SCGL/SCG_Logistics_RPA/RPA_parents_Coal_get_status%20Task"
    payload = json.dumps( {"control" : "getqueue","VESSELNAME" : ves_name })
    headers = {
    'Authorization': 'Bearer iNWu3jwLrK0Ee0BE5tkCJhxZx5NDvziv',
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    infoData = json.dumps(response.json())
    infoData = json.loads(infoData)
    infoData = flexmessage(infoData)
    return infoData


def getboat():
    url = "https://scglmwazprd.scglogistics.co.th/api/1/rest/feed-master/queue/SCG/CBM_SCGL/SCG_Logistics_RPA/RPA_parents_Coal_get_status%20Task"
    payload = json.dumps({
    "control": "getboat"
    })
    headers = {
    'Authorization': 'Bearer iNWu3jwLrK0Ee0BE5tkCJhxZx5NDvziv',
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    boatData = json.dumps(response.json())
    # print(boatData)
    boatData = json.loads(boatData)
    items = []
    for data in  boatData["boat"]:
        item = {
            "type": "action",
            "action": {
              "type": "postback",
              "label":data['VESSELNAME'],
              "data": data['VESSELNAME'],
              "displayText": 'ข้อมูล: '+ data['VESSELNAME']
            }
            }
        items.append(item)
    # print(items)
    posttext = {
      "type": "text",
      "text": "โปรดเลือกรายชื่อเรือ",
      "quickReply": {
        "items": items
      }
    }
    return posttext


def flexmessage(infoData):
    print("data_in",infoData)
    MATERIALNAME = str(infoData['MATERIALNAME'])
    CS_Group = str(infoData['CS_Group'])
    BOOKINGQUEUE = infoData['BOOKINGQUEUE']
    CALLQUEUE = infoData['CALLQUEUE']
    INSHIPPINGPOINT =  infoData['INSHIPPINGPOINT']
    OUTSHIPPINGPOINT =  infoData['OUTSHIPPINGPOINT']
    inshippointItems = []
    for inship_items in INSHIPPINGPOINT:
        dd ={
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": str(inship_items['MATERIAL'])
                                    },
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text":  str(inship_items['SP_NAME'])
                                            }
                                            ]
                                        },
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [
                                            {
                                                "type": "text",
                                                "text": str(inship_items['TOTAL']),
                                                "align": "center"
                                            }
                                            ]
                                        }
                                        ]
                                    }
                                    ]
                }
        inshippointItems.append(dd)
    outshippointItems =[]
    for outship_items in OUTSHIPPINGPOINT:
        dd = {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": str(outship_items['MATERIAL'])
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                        {
                                            "type": "box",
                                            "layout": "horizontal",
                                            "contents": [
                                            {
                                                "type": "box",
                                                "layout": "horizontal",
                                                "contents": [
                                                {
                                                    "type": "text",
                                                    "text": str(outship_items['SHIPTONAME']),
                                                    "size": "md"
                                                },
                                                {
                                                    "type": "text",
                                                    "text": str(outship_items['SP_NAME'])
                                                },
                                                {
                                                    "type": "box",
                                                    "layout": "horizontal",
                                                    "contents": [
                                                    {
                                                        "type": "box",
                                                        "layout": "vertical",
                                                        "contents": [
                                                        {
                                                            "type": "text",
                                                            "text": str(outship_items['TOTAL']),
                                                            "align": "center"
                                                        },
                                                        {
                                                            "type": "text",
                                                            "text": str(outship_items['ONETWEIGHT']),
                                                            "align": "center"
                                                        }
                                                        ]
                                                    }
                                                    ]
                                                }
                                                ]
                                            }
                                            ]
                                        },
                                        {
                                            "type": "separator",
                                            "color": "#808080"
                                        }
                                        ]
                                    }
                                    ]
                                }
        outshippointItems.append(dd)
    MsgFlag =      {
      "type": "flex",
      "altText": "This is a Flex Message",
      "contents": {
                    "type": "bubble",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": infoData['original']['content']['VESSELNAME'],
                            "weight": "bold",
                            "color": "#FFFFFFFF",
                            "position": "relative",
                            "align": "center"
                        }
                        ],
                        "backgroundColor": "#6495ED"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": CS_Group,
                                "align": "center",
                                "contents": [],
                                "weight": "bold"
                            }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": MATERIALNAME,
                                "align": "center",
                                "weight": "bold"
                            }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "text",
                                "text": "จองคิว",
                                "align": "start"
                            },
                            {
                                "type": "text",
                                "text": str(BOOKINGQUEUE),
                                "align": "center"
                            }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "text",
                                "text": "เรียกคิว"
                            },
                            {
                                "type": "text",
                                "text": str(CALLQUEUE),
                                "align": "center"
                            }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "separator",
                                "margin": "sm",
                                "color": "#CCCCFF"
                            },
                            {
                                "type": "text",
                                "text": "รอจ่ายสินค้า",
                                "align": "center",
                                "margin": "sm",
                                "weight": "bold"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents":  inshippointItems 
                            }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "separator",
                                "color": "#CCCCFF",
                                "margin": "sm"
                            },
                            {
                                "type": "text",
                                "text": "ชั่งออก",
                                "margin": "sm",
                                "weight": "bold",
                                "align": "center"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents":  outshippointItems                              
                                
                                
                            }
                            ]
                        }
                        ]
                    }
                    }
                }
    
  
    print(json.dumps(MsgFlag))
    return MsgFlag



if __name__ == "__main__":
    app.run(debug=True)
    # http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()





