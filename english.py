# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 20:34:26 2023

@author: Vénon
"""

import requests
import os
import json
from wrpy import get_available_dicts,WordReference
import deepl 
import win32com.client as win32
import ast
import time
import random

"""
Todo :
    -Chose the translation language + the languages of the words to translate
"""

#Create the application : 
#pyinstaller --onefile ../english.py --add-data "C:\Users\esto5\anaconda3\envs\PIP\Lib\site-packages\user_agent;./user_agent/" --add-data "D:\Folders\Code\Python\English\data.txt;./" --add-data "D:\Folders\Code\Python\English\WordListTranslate.txt;./" --add-data "D:\Folders\Code\Python\English\WordList.txt;./"

    
#API WORDS

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

def choiceAPI(choice,dico,n):
    if choice == 0:
        return NinjaRandoms(dico["ninjas"],n)
    elif choice == 1:
        return RDARandoms(n)
    else:
        raise ValueError("Choice API words not good")
        return -1
    
#API TRANSLATION
    
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

def WordReferencesTxt(result,dico):
    content=""
    for word in result:
        if result[word]!=-1:
            content+="<b>"+word+" : </b><br><br>"
            count = 0
            for item in result[word]["translations"][0]["entries"]:
                #for item in items["entries"]:
                for to_word in item["to_word"]:
                    content+="&emsp;"+to_word["meaning"]+"<br>"
                if isinstance(item["from_example"], list):
                    for from_example in item["from_example"]:
                        content+="&emsp;&emsp;<i>"+from_example+"</i><br>"
                elif  isinstance(item["from_example"], str):
                    content+="&emsp;&emsp;<i>"+item["from_example"]+"</i><br>"
                    
                if isinstance(item["to_example"], list):
                    for to_example in item["to_example"]:
                        content+="&emsp;&emsp;<i>"+to_example+"</i><br><br>"
                elif isinstance(item["to_example"], str):
                    content+="&emsp;&emsp;<i>"+item["to_example"]+"</i><br><br>"
                    
                count += 1
                if count == dico["wordreferencemaxexemples"]:
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
        content+=result + " = " + results[result] + "<br><br>"
    return content

def choiceTranslator(choice,dico,words):
    if choice == 0:
        return WordReferencesTxt(WordReferences(words),dico)
    elif choice == 1:
        return DeepLsTxt(DeepLs(words,dico["deepl"]))
    else:
        raise ValueError("Choice Translator not good")
        return -1

#EMAIL

def sendOutlookEmail(to, subject, body):
    outlook = win32.Dispatch('outlook.application')
    
    mail = outlook.CreateItem(0)
    mail.To = to
    mail.Subject = subject
    mail.HTMLBody = body
    
    mail.Send()
    
    del mail  
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

#DATA FILES
def wordApiTxt(dico):
    words = choiceAPI(int(dico["choiceapi"]),dico,int(dico["wordnumber"]))
    content = choiceTranslator(int(dico["choicetranslator"]),dico,words)
    content = deeplCompletation(dico,content,words)
    
    sendEmails(ast.literal_eval(dico["emails"]),content)
    
    return True

def wordListTxt(dico):
    with open("wordlist.txt", 'r') as file:
        words_array = ast.literal_eval(file.read())
        words=[]
        size = len(words_array)
        
        i=0
        while i< int(dico["wordnumber"]):
            n=random.randint(0,size-1)
            if words_array[n] not in words:
                words.append(words_array[n])
                i+=1
                
        content = choiceTranslator(int(dico["choicetranslator"]),dico,words)
        content = deeplCompletation(dico,content,words)
        
        sendEmails(ast.literal_eval(dico["emails"]),content)
        
        return True
            
def wordListTranslateTxt(dico):
    with open("wordlisttranslate.txt", 'r') as file:
        words_dico =json.loads(file.read())
        words=[]
        
        i=0
        while i< int(dico["wordnumber"]):
            word = random.choice(list(words_dico.keys()))
            if word not in words:
                words.append(word)
                i+=1
        
        content=""
        for word in words:
            content+=word + " = " + words_dico[word] + "<br><br>"
        
        sendEmails(ast.literal_eval(dico["emails"]),content)
        
        return True

def choiceData(choice,dico):
    if choice == 0:
        return  wordApiTxt(dico)
    elif choice == 1:
        return wordListTxt(dico)
    elif choice == 2:
        return wordListTranslateTxt(dico)
    else:
        raise ValueError("Choice Translator not good")
        return -1

#GENERAL

def deeplCompletation(dico,content,words):
    if dico["deepl"]!="":
        retry=[]
        for word in words:
            if isinstance(word, int):
                retry.append(word)
              
        if len(retry)>0:
            content+=DeepLs(retry,dico["deepl"])
    return content

def loadData(path):
    dico={}
    first=True
    separator=None
    with open(path, 'r') as file:
        for line in file.readlines():
            line=line.strip()
            if first:
                if line=='':
                    raise AttributeError("No separator at the start of the file.")
                separator=line
                first=False
            if line!='':
                line=line.split(separator)
                dico[line[0].lower()]=line[1]
    return dico, separator
    api_keys={}
    ok=False
    for part in dico:
        if part=="api key":
            ok=True
        if ok == True:
            api_keys[part]=dico[part]
    return api_keys
    
def main():
    dico, separator = loadData("data.txt")
    data = choiceData(int(dico["choicedata"]),dico)

if __name__ == "__main__":
    main()