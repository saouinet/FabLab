#!/usr/bin/env python
# coding: utf-8
import xml.etree.ElementTree as ET
import pandas as pd
import paho.mqtt.client as client
import os

def parseFiles(path = '.\\'):
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.XML' in file:
                yield os.path.join(r, file)


def BarcodeToOF(code):
    return "ZTP_FILE_"+"0000"+code[:8]+".XML"


def generateDict(OF):
    mappingFile = BarcodeToOF(OF)
    tree = ET.parse(mappingFile)
    root = tree.getroot()
    for idents in root.iter('IDNRK'):
        yield idents.text
    


# In[7]:

[print(f) for f in parseFiles()]

generateDict(BarcodeToOF("09462790"))


# In[ Node-red demo 0]:

#[{"id":"e4f44718.a13618","type":"tab","label":"Poste","disabled":false,"info":""},{"id":"675cd166.055c8","type":"tab","label":"Ilot","disabled":false,"info":""},{"id":"3bc86450.acc59c","type":"mqtt-broker","z":"","name":"","broker":"localhost","port":"1883","clientid":"mqtt","usetls":false,"compatmode":true,"keepalive":"60","cleansession":true,"birthTopic":"","birthQos":"0","birthPayload":"","closeTopic":"","closeQos":"0","closePayload":"","willTopic":"","willQos":"0","willPayload":""},{"id":"bc59f2c9.ddb1b","type":"ui_tab","z":"","name":"Home","icon":"dashboard","disabled":false,"hidden":false},{"id":"8caacf42.597ce","type":"ui_tab","z":"","name":"La course Bürkert","icon":"dashboard","disabled":false,"hidden":false},{"id":"78679e92.72858","type":"ui_group","z":"","name":"La Machine à Cocktail Bürkert","tab":"8caacf42.597ce","disp":true,"width":"6","collapse":false},{"id":"36ed3d92.392452","type":"ui_base","theme":{"name":"theme-light","lightTheme":{"default":"#0094CE","baseColor":"#0094CE","baseFont":"-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Oxygen-Sans,Ubuntu,Cantarell,Helvetica Neue,sans-serif","edited":true,"reset":false},"darkTheme":{"default":"#097479","baseColor":"#097479","baseFont":"-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Oxygen-Sans,Ubuntu,Cantarell,Helvetica Neue,sans-serif","edited":false},"customTheme":{"name":"Untitled Theme 1","default":"#4B7930","baseColor":"#4B7930","baseFont":"-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Oxygen-Sans,Ubuntu,Cantarell,Helvetica Neue,sans-serif"},"themeState":{"base-color":{"default":"#0094CE","value":"#0094CE","edited":false},"page-titlebar-backgroundColor":{"value":"#0094CE","edited":false},"page-backgroundColor":{"value":"#fafafa","edited":false},"page-sidebar-backgroundColor":{"value":"#ffffff","edited":false},"group-textColor":{"value":"#1bbfff","edited":false},"group-borderColor":{"value":"#ffffff","edited":false},"group-backgroundColor":{"value":"#ffffff","edited":false},"widget-textColor":{"value":"#111111","edited":false},"widget-backgroundColor":{"value":"#0094ce","edited":false},"widget-borderColor":{"value":"#ffffff","edited":false},"base-font":{"value":"-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Oxygen-Sans,Ubuntu,Cantarell,Helvetica Neue,sans-serif"}},"angularTheme":{"primary":"indigo","accents":"blue","warn":"red","background":"grey"}},"site":{"name":"Node-RED Dashboard","hideToolbar":"false","allowSwipe":"false","lockMenu":"false","allowTempTheme":"true","dateFormat":"DD/MM/YYYY","sizes":{"sx":48,"sy":48,"gx":6,"gy":6,"cx":6,"cy":6,"px":0,"py":0}}},{"id":"7ced562e.28d278","type":"mqtt in","z":"675cd166.055c8","name":"","topic":"560387","qos":"0","broker":"3bc86450.acc59c","x":200,"y":120,"wires":[["97b622ed.adaac"]]},{"id":"97b622ed.adaac","type":"debug","z":"675cd166.055c8","name":"","active":true,"tosidebar":true,"console":false,"tostatus":false,"complete":"false","x":380,"y":140,"wires":[]},{"id":"bd67704f.878c1","type":"inject","z":"e4f44718.a13618","name":"","topic":"","payload":"(100,100,100)","payloadType":"str","repeat":"","crontab":"","once":false,"onceDelay":0.1,"x":150,"y":160,"wires":[["dbe792e.929c47","bd6fb531.641438","253f3ccc.808ed4"]]},{"id":"9fefac64.d1392","type":"mqtt in","z":"675cd166.055c8","name":"","topic":"564741","qos":"0","broker":"3bc86450.acc59c","x":190,"y":180,"wires":[["97b622ed.adaac"]]},{"id":"d37eb480.c8ffd8","type":"mqtt in","z":"675cd166.055c8","name":"","topic":"564739","qos":"0","broker":"3bc86450.acc59c","x":210,"y":240,"wires":[["97b622ed.adaac"]]},{"id":"ed82f7.a6933d08","type":"mqtt in","z":"675cd166.055c8","name":"","topic":"560388","qos":"0","broker":"3bc86450.acc59c","x":190,"y":320,"wires":[["97b622ed.adaac"]]},{"id":"45379f8e.3cd06","type":"mqtt in","z":"675cd166.055c8","name":"","topic":"564740","qos":"0","broker":"3bc86450.acc59c","x":210,"y":380,"wires":[["97b622ed.adaac"]]},{"id":"dbe792e.929c47","type":"mqtt out","z":"e4f44718.a13618","name":"","topic":"564741","qos":"","retain":"","broker":"3bc86450.acc59c","x":330,"y":120,"wires":[]},{"id":"bd6fb531.641438","type":"mqtt out","z":"e4f44718.a13618","name":"","topic":"564739","qos":"","retain":"","broker":"3bc86450.acc59c","x":340,"y":160,"wires":[]},{"id":"253f3ccc.808ed4","type":"mqtt out","z":"e4f44718.a13618","name":"","topic":"560388","qos":"","retain":"","broker":"3bc86450.acc59c","x":340,"y":220,"wires":[]},{"id":"4d114c.bc5c2eb4","type":"inject","z":"e4f44718.a13618","name":"","topic":"","payload":"(0,0,0)","payloadType":"str","repeat":"","crontab":"","once":false,"onceDelay":0.1,"x":110,"y":240,"wires":[["dbe792e.929c47","bd6fb531.641438","253f3ccc.808ed4"]]}]


