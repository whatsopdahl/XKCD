#! /usr/bin/python
import random
from flask import Flask, request, render_template
from forms.py import ParamForm

app = Flask(__name__)

def checkSearch():
		if (len(request.args) == 0) :
			return 1
		else :
			return 0

def scoreWords(wordlist):
	LH = ['q','a','z','w','s','x','e','d','c','r','f','v','t','g']
	RH = ['b','y','h','n','u','j','m','i','k','o','l','p']
	prev=''
	dict= {}
	for aword in wordlist:
		score=0
		for ch in aword:
			if prev == ch:
				score+=2
			if (prev in LH and ch in RH) :
				score+=1
			elif (prev in RH and ch in LH) :
				score+=1
			prev = ch
		if score not in dict.keys():
			dict[score] = []
		dict[score].append(aword)
			
	return dict
			
def chooseOptWords(options, wordDict):
	topTen = []
	minWL = int(options['minWL'])
	maxWL = int(options['maxWL'])
	maxPswd = int(options['maxPSWD'])
	changeE=False
	changeO=False
	changeL=False
	if 'e' in options.keys():
		changeE=True
	if 'o' in options.keys():
		changeO=True
	if 'l' in options.keys():
		changeL=True
	topTen = tryOptWords(minWL, maxWL, maxPswd, wordDict)
	for index in range(len(topTen)):
		words = topTen[index]
		pswd=''
		if 'firstword' in options.keys():
			words[0]=words[0].title();
		if 'secondword' in options.keys():
			words[1]= words[1].title();
		if 'thirdword' in options.keys():
			words[2]= words[2].title();
		if 'fourthword' in options.keys():
			words[3]= words[3].title();
		for wordindex in range(4):
			if changeE:
				words[wordindex] =replace(words[wordindex], 'e', '3')
				words[wordindex] =replace(words[wordindex], 'E', '3')
			if changeO:
				words[wordindex] =replace(words[wordindex],'o', '0')
				words[wordindex] =replace(words[wordindex],'O', '0')
			if changeL:
				words[wordindex] =replace(words[wordindex],'l', '1')
				words[wordindex] =replace(words[wordindex], 'L', '1')
			pswd+=words[wordindex]
		topTen[index]=pswd
	return topTen

def tryOptWords(minWL, maxWL, maxPswd, wordDict):
	scores=wordDict.keys()
	scores.sort()
	topTen =[]
	i = len(scores)-1
	while len(topTen) < 10 and i > -1:
		words = []
		tried = 0
		length = 0
		myList = wordDict.get(scores[i]) 
		while len(words) < 4 and tried < len(myList):
			index = random.randint(-1, len(myList)-1)
			aword = myList[index]
			tried += 1
			if len(aword) >= minWL and len(aword) <=maxWL:
				if aword not in words:
					words.append(aword)
					length += len(aword)
		if len(words) == 4:
			if length <= maxPswd:
				if words not in topTen:
					topTen.append(words)
		else:
			i-=1
	return topTen
	
def chooseWords(options, wordList):
	minWL = int(options['minWL'])
	maxWL = int(options['maxWL'])
	maxPswd = int(options['maxPSWD'])
	changeE=False
	changeO=False
	changeL=False
	if 'e' in options.keys():
		changeE=True
	if 'o' in options.keys():
		changeO=True
	if 'l' in options.keys():
		changeL=True
	words, length = tryWords(minWL, maxWL, wordList)
	while length > maxPswd:
		words, length = tryWords(minWL, maxWL, wordList)
	if 'firstword' in options.keys():
		words[0]=words[0].title();
	if 'secondword' in options.keys():
		words[1]= words[1].title();
	if 'thirdword' in options.keys():
		words[2]= words[2].title();
	if 'fourthword' in options.keys():
		words[3]= words[3].title();
	for wordindex in range(4):
		if changeE:
			words[wordindex] = replace(words[wordindex], 'e', '3')
			words[wordindex] =replace(words[wordindex], 'E', '3')
		if changeO:
			words[wordindex] =replace(words[wordindex],'o', '0')
			words[wordindex] =replace(words[wordindex],'O', '0')
		if changeL:
			words[wordindex] =replace(words[wordindex],'l', '1')
			words[wordindex] =replace(words[wordindex], 'L', '1')
	Pswd = ''
	for i in range(len(words)):
		Pswd+=words[i]
	return Pswd

def replace(word, ch, newch):
	index = word.find(ch)
	while index != -1:
		word = word[:index] +newch + word[index+1:]
		index =word.find(ch, index)
	return word

def tryWords(minWL, maxWL, wordList):
	words=[]
	length=0
	checked = [] 
	while len(words) < 4 and len(checked) < len(wordList):
		aword= wordList[random.randint(-1, len(wordList)-1)]
		checked.append(aword)
		if len(aword) >= minWL and len(aword) <= maxWL and aword not in words:
			words.append(aword)
			length+=len(aword)
	return words, length
	
def selectOptions():
	varDict=request.args
	return varDict
	
def checkLimits(options):
	OK = True
	if int(options['minWL']) >= int(options['maxWL']):
		OK =False
	if int(options['maxPSWD']) <= int(options['maxWL']):
		OK = False
	if (int(options['maxPSWD']) < (4*int(options['minWL']))):
		OK=False
	if int(options['maxPSWD']) < (3 * int(options['maxWL'])):
		OK=False
	return OK

@app.route('/')
def main():
	myform = ParamForm(csrf_enabled=False)
	commonWords = open("top5000.txt", "r")
	wordList = []
	for word in commonWords:
		wordList.append(word)
		
	if (checkSearch() == 1):
		return render_template("form.html", err = '', form = myform)
	else:
		options = selectOptions()
		if not checkLimits(options):
			errormsg= "Error: Invalid Word Limits (increase Password length and/or endure min word length < max word length)"
			return render_template("form.html", err = errormsg, form = myform)
		else:
			if 'optimization' in options.keys() :
				wordDict= scoreWords(wordList)
				passwordList = chooseOptWords(options, wordDict)
			else:
				passwordList = []
				for i in range(10):
					pswd = chooseWords(options, wordList)
					passwordList.append(pswd)
			if not passwordList: 
				return render_template("form.html", err="Unable to generate passwords. Please reload page and select different Limits", form = myform)
			else:
				return render_template("pswdTable.html", passwordList = passwordList)

if __name__ == "__main__":
	app.run(debug=True)