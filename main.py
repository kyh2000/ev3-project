#!/usr/bin/env python3
from ev3dev2.sound import Sound #ev3 사운드를 이용하기 위하여 선언
from ev3dev2.sensor import INPUT_2
from ev3dev2.sensor import INPUT_3
from ev3dev2.motor import Motor, OUTPUT_A
from ev3dev2.motor import Motor, OUTPUT_D
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor import INPUT_4
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import UltrasonicSensor
import wiotp.sdk.device #iot 정보 받기 위하여 선언
sound=Sound() 
motorA = Motor(OUTPUT_A)
motorD = Motor(OUTPUT_D)
sensor1 = UltrasonicSensor(INPUT_1) 
touch1 = TouchSensor(INPUT_2)
touch2 = TouchSensor(INPUT_3)
color = ColorSensor(INPUT_4)
warning=0
myConfig = { #iot이용 위해 정보 입력
"identity": {
"orgId": "2019312005", #your orgId
"typeId": "EV3", #your typeId
"deviceId": "EV3_2019312005" #your deviceId
},
"auth": {
"token": "n55Idx&zE?zkMLQehP"
}
}
myData={'name' : 'foo', 'status' :' ' } #보낼 메세지
client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)
while True:
    motorA.stop()
    motorD.stop()
    client.connect() #iot에 연결
    while color.color==1: #모터 2개의 이동 방향을 다르게 하여 좌회전 수행
        myData={'name' : 'foo', 'status' :'going left' }
        client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
        motorA.on(15)
        motorD.on(-15)
        if touch1.is_pressed==True and touch2.is_pressed==True:#긴급상황표시,모터 정지
            motorA.stop()
            motorD.stop()
            warning=1
            break
        
        while sensor1.distance_centimeters < 10 :#가까이가면 후진
            myData={'name' : 'foo', 'status' :'go backward' }
            client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
            motorA.on(-7)
            motorD.on(-7)
    
    while color.color==5: #모터 2개의 이동 방향을 다르게 하여 우회전 수행
        myData={'name' : 'foo', 'status' :'going right' }
        client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
        motorA.on(-15)
        motorD.on(15)
        if touch1.is_pressed==True and touch2.is_pressed==True:#긴급상황표시,모터 정지
            motorA.stop()
            motorD.stop()
            warning=1
            break
        
        while sensor1.distance_centimeters < 10 :#가까이가면 후진
            myData={'name' : 'foo', 'status' :'going backward' }
            client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
            motorA.on(-7)
            motorD.on(-7)
       

    
    while sensor1.distance_centimeters < 10 :#가까이가면 후진
        myData={'name' : 'foo', 'status' :'going backward' }
        client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
        motorA.on(-7)
        motorD.on(-7)    
        
    if touch1.is_pressed==True and touch2.is_pressed==True:#긴급상황표시,모터 정지
        motorA.stop()
        motorD.stop()
        warning=1

    while touch1.is_pressed==True:#뒤로이동
        myData={'name' : 'foo', 'status' :'going backward' }
        client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
        motorA.on(-7)
        motorD.on(-7)
     

    while touch2.is_pressed==True:#이동
        myData={'name' : 'foo', 'status' :'go forward' }
        client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
        motorA.on(15) #모터회전,이동중 표시
        motorD.on(15)


        while sensor1.distance_centimeters < 10 :#가까이가면 후진
            myData={'name' : 'foo', 'status' :'going backward' }
            client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
            motorA.on(-7)
            motorD.on(-7)
       

    if warning==1:# 위험상황이 1로 될시 해당 동작 반복, 위험음을 내며 iot 이용하여 위험하다는 신호를 보냄
        while True:
            myData={'name' : 'foo', 'status' :'warning!!!' }
            client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
            motorA.stop()
            motorD.stop()
            sound.play_tone(880,350,100)