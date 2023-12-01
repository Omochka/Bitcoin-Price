import requests
import calendar
import datetime
import matplotlib.pyplot as plt
from tkinter import *
from tkcalendar import *


startDate = ""
endDate = ""

today = datetime.date.today()

def APIRequest(start='2010-07-17', end=today):
    startEndDate = {'start': start, 'end': end}
    userRequest =  requests.get("https://api.coindesk.com/v1/bpi/historical/close.json?", params = startEndDate)
    responseDictionary = userRequest.json()
    responseData = responseDictionary['bpi']
    userRequest.close()
    return responseData


def ComparePrice(res):
    biggestPrice = {}
    tempBiggestPrice = 0
    for key, value in res.items():
        if(value > tempBiggestPrice):
            tempBiggestPrice = value
            biggestPrice[key] = value        
    return list(biggestPrice.items())[-1]




def HighesBitcoinPrice():
    apiResponse = APIRequest()
    biggestPrice = ComparePrice(apiResponse)
    return biggestPrice
    
def PriceDynamic():
    resp = APIRequest()
    priceShift = 2000
    prices = {}
    for j in range(len(resp)):
        if(j+1 != len(resp)):
            summ = abs(list(resp.values())[j] - list(resp.values())[j + 1])
            if(summ > priceShift):
                print(list(resp.keys())[j] + " -> " + list(resp.keys())[j + 1] + " = " + str(int(summ)) + "(price diff)")
        
    
def PeriodDynamic():
    responseData = APIRequest()
    priceR = []
    priceF = []
    st = ""
    st1 = ""
    for j in range(len(responseData) - 1):
        if(list(responseData.values())[j] > list(responseData.values())[j + 1]):
            st+=list(responseData.keys())[j] + " "
            priceR.append(st1)
            st1 = ""
        else:
            st1+=list(responseData.keys())[j] + " "
            priceF.append(st)
            st = ""

    if(len(max(priceF, key=len)) > len(max(priceR, key=len))): 
        print("Longest sequence, where the price falls: " + max(priceF, key=len))
    else:
        print("Longest sequence, where the price rises: " + max(priceR, key=len))
        

def ShowGraph(start, end):
    if plt.fignum_exists(1):
        plt.close(1)
    responseData = APIRequest(start, end)
    keyV = []
    valueK = []
    for key, value in responseData.items():
        keyV.append(key);
        valueK.append(value)
    
    plt.xkcd()
    plt.xticks([])
    plt.tight_layout()
    plt.plot(keyV, valueK)
    plt.xlabel("Bitcoin price")
    plt.show()
    
    

def SubstractDate(choice):
    if(choice == "Last week"):
        showDate = today - datetime.timedelta(weeks=1)
    elif(choice == "Last month"):
        showDate = today - datetime.timedelta(1*365.25/12)
    elif(choice == "Last 3 months"):
        showDate = today - datetime.timedelta(3*365.25/12)
    elif(choice == "Last year"):
        showDate = today - datetime.timedelta(days=365.25)
    ShowGraph(showDate, today)
    
    
    
def ButtonEvent():
    root = Tk()
    root.title("Select period")
    root.geometry("300x200")
    root.eval('tk::PlaceWindow . center')
    
    def Selected():
        myLabel = clicked.get()
        if(myLabel == "Set period"):
            x = datetime.datetime.now()
            root = Tk()
            root.title("Set date")
            root.geometry("400x400")
            root.eval('tk::PlaceWindow . center')  
            DateEntry(root, locale='en_US',date_pattern='mm-dd-y')
            cal = Calendar(root, selectmode="day", year=x.year, month=x.month, day=x.day)
            cal.pack(pady=20, fill="both", expand=True)
            
            def GrabStartDate():
                global startDate
                d = datetime.datetime.strptime(cal.get_date(),"%m/%d/%y").date()
                startDate = d
                print("You've selected start date")
                
            def GrabEndDate():
                global endDate
                d = datetime.datetime.strptime(cal.get_date(),"%m/%d/%y").date()
                endDate = d
                print("You've selected end date")
            
            def ShowGraphPls():
                if(startDate == "" or endDate == ""):
                    print("First select start and end dates.")
                elif(startDate > today or endDate > today):
                    print("Start or end date mustn't be greater than current date(" + str(today) + ")")
                elif(startDate > endDate):
                    print("Start date must be less than end date.")
                else:
                    ShowGraph(startDate, endDate)
            
            
            myButton = Button(root, text="Select start date", command=GrabStartDate)
            myButton.pack(pady=0)
            
            myButton1 = Button(root, text="Select end date", command=GrabEndDate)
            myButton1.pack(pady=20)
            
            endButton = Button(root, text="Show graph", command=ShowGraphPls)
            endButton.pack(pady=20)    
            
            root.mainloop()
        else:
            SubstractDate(myLabel)
      
    options = ["Last week", "Last month", "Last 3 months", "Last year", "Set period"]
    clicked = StringVar()
    clicked.set(options[0])
    drop = OptionMenu(root, clicked, *options)
    drop.pack()
    myButton = Button(root, text = "Select", command=Selected).pack()
    root.mainloop()
    

print("\n1. Päev kõige kõrgema Bitcoini hinnaga.\n=================================")
print("The biggest bitcoin price is " + str(int(HighesBitcoinPrice()[1])) + " in " + str(HighesBitcoinPrice()[0]))
print("\n2. Päevad, millal Bitcoini hind kõige rohkem langes ja tõusis.\n=================================")
PriceDynamic()
print("\n3. Kõige pikemad perioodid, mille jooksul on Bitcoini hind langenud ja tõusnud.\n=================================")
PeriodDynamic()
print("\n5. Bitcoini hind kasutaja valitud perioodiks.\n=================================")
print("Show graph. You can change dates.")
##Enter your date below
ShowGraph("2019-02-02", "2021-01-01")
print("\n6.  Punkt nr. 5 graafilise liidese abil\n=================================")
print("Select period")
ButtonEvent()




