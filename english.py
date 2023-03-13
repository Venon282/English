# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 20:34:26 2023

@author: esto5
"""

import requests
import os
import json
from wrpy import get_available_dicts,WordReference
import deepl 
import win32com.client as win32
import ast
import time

""""""
    
def RDARandoms(n):
    array = []
    for i in range(n):
       array.append(RDARandom()[0]) 
    return array
    
def RDARandom():
    response =  requests.get("https://random-word-api.herokuapp.com/word")
    if response.status_code == requests.codes.ok:
        return json.loads(response.text)
    return -1

def NinjaRandoms(api_key,n):
    array = []
    for i in range(n):
        array.append(NinjaRandom(api_key)["word"]) 
    return array
    
def NinjaRandom(api_key):
    api_url = 'https://api.api-ninjas.com/v1/randomword'
    response = requests.get(api_url, headers={'X-Api-Key': api_key})
    if response.status_code == requests.codes.ok:
        return json.loads(response.text)
    return -1
    
def loadData(path,operator):
    dico={}
    with open(path, 'r') as file:
        for line in file.readlines():
            line=line.strip()
            if line!='':
                line=line.split(operator)
                dico[line[0].lower()]=line[1]
    return dico

def choiceAPI(choice,api_keys,n):
    if choice == 0:
        return NinjaRandoms(api_keys["ninjas"],n)
    elif choice == 1:
        return RDARandoms(n)
    else:
        raise ValueError("Choice not good")
        return -1
    
def WordReferences(words):
    wr = WordReference('en', 'fr')
    dico={}
    for word in words:
        try:
            dico[word]=wr.translate(word)
        except NameError as e:
            print("Translation error : " + str(e))
            dico[word]=-1
    return dico

def WordReferencesTxt(result):
    content=""
    for word in result:
        if result[word]!=-1:
            content+=word+" : \n\n"
            count = 0
            for item in result[word]["translations"][0]["entries"]:
                #for item in items["entries"]:
                for to_word in item["to_word"]:
                    content+="\t"+to_word["meaning"]+"\n"
                if isinstance(item["from_example"], list):
                    for from_example in item["from_example"]:
                        content+="\t\t"+from_example+"\n"
                elif  isinstance(item["from_example"], str):
                    content+="\t\t"+item["from_example"]+"\n"
                    
                if isinstance(item["to_example"], list):
                    for to_example in item["to_example"]:
                        content+="\t\t"+to_example+"\n\n"
                elif isinstance(item["to_example"], str):
                    content+="\t\t"+item["to_example"]+"\n\n"
                    
                count += 1
                if count == 5:
                    break
    content+="\n\n"
    return content
                        

def DeepLs(words,api_key):
    translator = deepl.Translator(api_key) 
    dico={}
    for word in words:
        result = translator.translate_text(word, target_lang="FR") 
        translated_text = result.text
        dico[word]=translated_text
    return dico

def DeepLsTxt(results):
    content=""
    for result in results:
        content+=result + " = " + results[result] + "\n"
    return content

def choiceTranslator(choice,api_keys,words):
    if choice == 0:
        return WordReferencesTxt(WordReferences(words))
    elif choice == 1:
        return DeepLsTxt(DeepLs(words,api_keys["deepl"]))

def apiKeys(dico):
    api_keys={}
    ok=False
    for part in dico:
        if part=="api key":
            ok=True
        if ok == True:
            api_keys[part]=dico[part]
    return api_keys

def sendOutlookEmail(to, subject, body):
    #killOutlook()
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = to
    mail.Subject = subject
    mail.Body = body
    mail.Send()
    time.sleep(10)
    
    killOutlook()
    
def sendEmails(tos,content):
    for to in tos:
        sendOutlookEmail(to,"English Vocabulary",content)
        
def killOutlook():
    os.system('taskkill /im outlook.exe /f')
    os.system('reg add HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Office\\16.0\\Outlook\\Security\\ /v ObjectModelGuard /t REG_DWORD /d 2 /f')
    os.system('taskkill /im outlook.exe /f')
    os.system('reg add HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Office\\16.0\\Outlook\\Security\\ /v ObjectModelGuard /t REG_DWORD /d 0 /f')

def main():
    dico = loadData( os.path.dirname(os.path.abspath(__file__))+"\data.txt",",")
    api_keys = apiKeys(dico)
    words = choiceAPI(int(dico["choiceapi"]),api_keys,int(dico["wordnumber"]))
    content = choiceTranslator(int(dico["choicetranslator"]),api_keys,words)

    if api_keys["deepl"]!="":
        retry=[]
        for word in words:
            if isinstance(word, int):
               retry.append(word)
          
        if len(retry)>0:
            content+=DeepLs(retry,api_keys["deepl"])

    sendEmails(ast.literal_eval(dico["emails"]),content)

if __name__ == "__main__":
    main()