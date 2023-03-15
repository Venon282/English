# Learn English each days

## Description :

This application aims to help you learn English vocabulary (will evolve for several different languages) daily by sending you an email.

## Possibilities : 

The application provides different APIs for words and for translations. You can choose to leave the choice of words and translation to the application. You can choose to leave only the translation to the application and thus define your own word lists. Or you can define your own word list with your own translations.

## Words API
You can currently choose between two APIs :
- random-word-api : a large set of words but they can be conjugated so if you choose the WordReference translation, they can't all be translated. DeepL if the api key is entered will allow you to translate the rest of the words.
- Ninjas : a good api 

## Translator API
- WordReference : The best at translating a single word. Provides several translations with examples of use.
- DeepL : The classic deepL

## Files
You have differents files.
- data.txt : The file to set up the application, put your api keys, define the type of translations, etc. The first line defines the separator. Adapt the file according to.
- wordlist.txt : A list of untranslated words based on the words used for languaskill
	- https://www.cambridgeenglish.org/Images/22099-vocabulary-list.pdf
- English/WordListTranslate.txt : A dictionary of words with their translations. Perfect for revising in time

## How use it ?

First you have to complete the data.txt in English application or put them in the dist if you use the application, in the current folder if the .pyy. Enter your email(s) and your api keys

To send an email with the number of random words chosen in the data.txt file, simply run the application.

There are several ways to run the application daily without having to worry about it. 
- Put it on a server 
- Use the windows task scheduler
	- Create a simple task
	- Enter the name of the task -> next
	- Enter the frenquency -> next
	- Put Start a program -> next
	- Enter the exe path -> next -> Terminate
