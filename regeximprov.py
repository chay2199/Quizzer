import pyscreenshot as ImageGrab

if __name__ == "__main__":
    # part of the screen
    im=ImageGrab.grab(bbox=(19,450,550,1000)) # X1,Y1,X2,Y2
#-#

from PIL import Image
import re
import pytesseract
import json
text = pytesseract.image_to_string(im,lang='eng' ,)

optionA = ''
optionB = ''
optionC = ''
question = ''
optionsList = ''
for i in text:
    if(ord(i)!=63):
        question = question + i
    elif(ord(i)==63):
        break
options = text[len(question):]
for i in options:
    if(ord(i)!=63):
        optionsList = optionsList + i
newline = ''
for i in optionsList:
    if(ord(i)==10):
        newline = newline + i
    elif(ord(i)!=10):
        break
optionsList = optionsList[len(newline):]
for i in optionsList:
    if(ord(i)!=10):
        optionA = optionA + i
    elif(ord(i)==10):
        break
optionsList = optionsList[len(optionA):]
#print(optionsList)
newline = ''
for i in optionsList:
    if(ord(i)==10):
        newline = newline + i
    elif(ord(i)!=10):
        break
optionsList = optionsList[len(newline):]
#print(optionsList)
for i in optionsList:
    if(ord(i)!=10):
        optionB = optionB + i
    elif(ord(i)==10):
        break
optionsList = optionsList[len(optionB):]
newline = ''
for i in optionsList:
    if(ord(i)==10):
        newline = newline + i
    elif(ord(i)!=10):
        break
optionsList = optionsList[len(newline):]
#print(optionsList)
for i in optionsList:
    if(ord(i)!=10):
        optionC = optionC + i
    elif(ord(i)==10):
        break

from googleapiclient.discovery import build

my_api_key = "AIzaSyA5-NFyxzFTX6yUd77cxqR40Fcea8dW0mE"
my_cse_id = "015741789419081488682:dxypydvjxpg"

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

results = google_search(question , my_api_key, my_cse_id, num=10)
answers = json.dumps(results)
jsonData = json.loads(answers)
finalAnswer = ''
for er in jsonData:
    title = er['htmlSnippet']
    snippet = er['snippet']
    finalAnswer = finalAnswer + title + snippet

countA = 0
countB = 0
countC = 0
optionAList = optionA.split(sep=' ')
optionBList = optionB.split(sep=' ')
optionCList = optionC.split(sep=' ')

for i in optionAList:
    re_str1A = r'\S'
    re_str2A = i[2:]
    re_str3A = r'.'
    re_patternA = re.compile(re_str1A + re_str2A + re_str3A)
    matchA = re_patternA.findall(finalAnswer)
    countA = countA + len(matchA)

for i in optionBList:
    re_str1B = r'\S'
    re_str2B = i[2:]
    re_str3B = r'.'
    re_patternB = re.compile(re_str1B + re_str2B + re_str3B)
    matchB = re_patternB.findall(finalAnswer)
    countB = countB + len(matchB)

for i in optionCList:
    re_str1C = r'\S'
    re_str2C = i[2:]
    re_str3C = r'.'
    re_patternC = re.compile(re_str1A + re_str2A + re_str3A)
    matchC = re_patternC.findall(finalAnswer)
    countC = countC + len(matchC)

print(text)
print(optionA,countA,optionB,countB,optionC,countC)
