import pyautogui as h
import cv2
import pytesseract as py
import time

#Define things? (idk what this does)
py.pytesseract.tesseract_cmd = r'D:\Queens Univeristy\CISC121\Code\ShopProgram\Tesseract\tesseract.exe'
h.PAUSE = 0.14
h.FAILSAFE = True

#TIME SUMMARY
#Total Pausetime - 2.38s (0.14  x17)
#Total Sleeptime - 0.7s (0.4+0.1+0.1+0.1)
#Total Intervaltime ~2.24s (longest entryx0.07 + 10mx0.07)
#Total Time Per Entry - 5.32s 
#Total Time Per Scratch(~50items) - 266s or 4min 28s

#Key Locations Campus Setup
#Shop Seach Box - 546, 345
#Search By Price - 1076, 1677
#Price Top Left - 964, 638
#Price bot right - 1185, 690

#Backup Price Top Left - (x=965, y=842)
#Backup Price Bot Right - (x=1184, y=891)


#Key Locations Home
#Shop Seach Box - Point(x=616, y=242)
#Search By Price - Point(x=775, y=1192)
#Price Top Left - Point(x=716, y=459)
#Difference - (147, 31)
#Price Bot Right - Point(x=846, y=496)

#Backup Price Top Left - Point(x=704, y=605)
#Backup Price Bot Right - Point(x=847, y=634)

def searchitem(itemname):
    '''searches shop for item in product search window

        parameter:
            itemname - string pulled from list of item name used to search

        return
            itemprice - item price in string format
    '''
    price = ""


    h.moveTo(749, 316)
    time.sleep(0.1)
    h.click()

    #Clear Textbox
    h.hotkey('ctrl','a')
    h.press('backspace')

    #Search Item
    h.write(itemname, interval=0.006)

    #Search
    h.moveTo(1002, 1557)
    time.sleep(0.1)
    h.click()


    #Screenshot
    time.sleep(0.8)
    h.screenshot('temp.png',region=(640, 425 ,150, 40))
    h.screenshot('deb.png',region=(640, 560 ,150, 40))
    h.screenshot('backup.png', region=(640, 625 ,150, 40))
    price = imageread()

    #Reset
    h.press('esc')

    return price


def imageread():
    ''' takes image and grabs text as string
    '''
    imgarray = cv2.imread('temp.png', cv2.IMREAD_GRAYSCALE)

    thresh = 128
    imgarray = cv2.threshold(imgarray, thresh, 255, cv2.THRESH_BINARY)[1]
    cv2.imwrite('temp.png',imgarray)

    text = py.image_to_string(imgarray,lang='eng', config='-c page_separator= --psm 6')
    return text

def windowsetup():
    with h.hold('alt'):
        h.press(['tab', 'tab'])
    with h.hold('alt'):
        h.press(['tab', 'tab'])

#Enter Spread Sheet
def addtosheet(price):
    price = price.strip('\n')
    h.hotkey('alt', 'tab')
    time.sleep(0.1)
    h.write(price, interval=0.07)
    h.press('enter')
    h.hotkey('alt', 'tab')

def backupimage():
    imgarray = cv2.imread('backup.png', cv2.IMREAD_GRAYSCALE)

    thresh = 128
    imgarray = cv2.threshold(imgarray, thresh, 255, cv2.THRESH_BINARY)[1]
    cv2.imwrite('backup.png',imgarray)

    text = py.image_to_string(imgarray,lang='eng', config='-c page_separator= --psm 6')
    if (text == ""):
        return "FILLER"
    else:
        return text

def generatelist(scratchname):
    templist = []
    file = open(scratchname + '.txt', 'r')
    for line in file:
        templist.append(line.strip('\n'))
    return templist

def switchtab(tabnumber):
        h.hotkey('alt', 'tab')
        time.sleep(0.5)
        h.hotkey('ctrl', str(tabnumber))
        h.hotkey('alt', 'tab')
#MAIN
bannerlist = ["MysticalReverie", "MercenaryStyle","FrozenWorld"]
counter = 3
windowsetup()
for scratch in bannerlist:
    scratchlist = generatelist(scratch)
    for scratchitem in scratchlist:
        price = searchitem(scratchitem)
        if price == "":
            print("P2S Error at " + scratchitem)
            addtosheet(backupimage())

        elif(price.upper().isupper() == True):
            print("Image Detection Error at "+ scratchitem)
            addtosheet("Tess Error")
        else:
            addtosheet(price)
    switchtab(counter)
    counter += 1