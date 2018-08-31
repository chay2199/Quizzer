import pyscreenshot as ImageGrab
import re
import json
import cv2
import numpy as np
from PIL import Image
import pytesseract




if __name__ == "__main__":
    # part of the screen
    im = ImageGrab.grab(bbox=(19,300,550,800)) # X1,Y1,X2,Y2
    im.save('grab.png')

# Path of working folder on Disk
src_path = "/home/chaitanya/PycharmProjects/tess"

def get_string(img_path):
    # Read image with opencv
    img = cv2.imread(img_path)

    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    # Write image after removed noise
    cv2.imwrite(src_path + "removed_noise.png", img)

    #  Apply threshold to get image with only black and white
    #img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # Write the image after apply opencv to do some ...
    cv2.imwrite(src_path + "thres.png", img)

    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(Image.open(src_path + "thres.png"))

    # Remove template file
    #os.remove(temp)

    return result

text = get_string('grab.png')

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
re_str1C = r'\S'
re_str2C = optionC[2:]
re_str3C = r'.'

re_patternC = re.compile(re_str1C + re_str2C + re_str3C)
matchC = re_patternC.findall(finalAnswer)
countC = len(matchC)

re_str1A = r'\S'
re_str2A = optionA[2:]
re_str3A = r'.'
re_patternA = re.compile(re_str1A + re_str2A + re_str3A)
matchA = re_patternA.findall(finalAnswer)
countA = len(matchA)

re_str1B = r'\S'
re_str2B = optionB[2:]
re_str3B = r'.'
re_patternB = re.compile(re_str1B + re_str2B + re_str3B)
matchB = re_patternB.findall(finalAnswer)
countB = len(matchB)
print(text)
print((optionA,countA,optionB,countB,optionC,countC))
if(countA==countB and countB==countC):
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
    print(optionA, countA, optionB, countB, optionC, countC)

