
import json

with open('theaterData.json', 'w+') as json_file:
    json_file.write("{}")
with open('userData.json', 'w+') as json_file:
    json_file.write("{}")
with open('theaterData.json') as f:
    theaterData = json.load(f)
with open('userData.json') as f:
    userData = json.load(f)


def DisplayOptions():
    print("1. Show the seats")
    print("2. Buy a ticket")
    print("3. Statistics")
    print("4. Show booked tickets user info")
    print("0. Exit")

def showSeats():
    with open('theaterData.json') as f:
        theaterData = json.load(f)
    theaterData = json.loads(theaterData)

    print("Cinema:")
    rowCount = 1
    aRowDisplay = ''
    for a in range(0, theaterData["col"] + 1):
        if a == 0:
            aRowDisplay += "  "
        else:
            aRowDisplay += "{} ".format(a)
    print(aRowDisplay)
    for aShowRow in theaterData["bookingArray"]:
        aRowDisplay = "{} ".format(rowCount)
        rowCount += 1
        for aSeat in aShowRow:
            if aSeat == 0:
                aRowDisplay += "S "
            elif aSeat == 1:
                aRowDisplay += "B "
        print(aRowDisplay)

def isSeatAvailable(r, c):
    with open('theaterData.json') as f:
        theaterData = json.load(f)
    theaterData = json.loads(theaterData)
    
    if r > theaterData["row"] and c > theaterData["col"]:
        return True
    if theaterData["bookingArray"][r][c] == 0:
        return True
    else:
        return False

def bookASeat(br, bc, cost):
    

    name = input("Name: ")
    gender = input("Gender: ")
    age = input("Age: ")
    phoneNo = input("Phone No.: ")

    
    with open('userData.json') as f:
        userData = json.load(f)

    aNewUser = {
        'name': name,
        'gender': gender,
        'age': age,
        'phone': phoneNo,
        'tprice': cost
    }

    userData["{}{}".format(br - 1, bc - 1)] = aNewUser
    with open('userData.json', 'w+') as json_file:
        json.dump(userData, json_file)

    
    with open('theaterData.json') as f:
        theaterData = json.load(f)
    theaterData = json.loads(theaterData)

    theaterData["bookingArray"][br - 1][bc - 1] = 1


    tData = json.dumps({ 'row': theaterData["row"], 'col': theaterData["col"], 'bookingArray': theaterData["bookingArray"] })

    with open('theaterData.json', 'w+') as json_file:
        json.dump(tData, json_file)

    return True

def buyATicket():
    print("Buying ticket")
    with open('theaterData.json') as f:
        theaterData = json.load(f)
    theaterData = json.loads(theaterData)
    row = theaterData["row"]
    col = theaterData["col"]
    perRowCost = findCostOfASeatInRow(row, col)

    bookRow = int(input("Enter row number:\n"))
    bookCol = int(input("Enter col number:\n"))

    
    if bookRow <= row and bookCol <= col:
        isSeatAv = isSeatAvailable(bookRow - 1, bookCol - 1)
        isBook = input("Price for the seat: {}\nDo you want to book?(Yes/No):\n".format(perRowCost[bookRow - 1]))
        
        if isSeatAv == True and isBook.lower() == 'yes':
            
            isBooked = bookASeat(bookRow, bookCol, perRowCost[bookRow - 1])
            if isBooked == True:
                print("Booked Successfully.")
            else:
                print("Booking failed.")
        else:
            print("Booking not done!. \n Already Booked try another \n")
    else:
        print("Invalid seat number entered.!")
    return

def findCostOfASeatInRow(row, col):
    totalSeats = row * col
    pricePerRow = []
    if totalSeats <= 60:
        for i in range(row):
            pricePerRow.append(10)
    elif totalSeats > 60:
        dig = row // 2
        gid = row - dig
        
        for i in range(1, row + 1):
            if i <= dig:
                pricePerRow.append(10)
            else:
                pricePerRow.append(8)
    return pricePerRow
    

def showStats():
    with open('theaterData.json') as f:
        theaterData = json.load(f)
    theaterData = json.loads(theaterData)

    row = theaterData["row"]
    col = theaterData["col"]
    ticketCount = 0
    currentPrice = 0
    perRowCost = findCostOfASeatInRow(row, col)
    print(perRowCost)
    rowNumber = 0
    for a_row in theaterData["bookingArray"]:
        tInRow = a_row.count(1)
        ticketCount += tInRow
        currentPrice += tInRow * perRowCost[rowNumber]
        rowNumber += 1

    percentage = (ticketCount / (row * col)) * 100
    totalIncome = 0
    for rp in perRowCost:
        totalIncome += rp * col

    print("Number of purchased tickets: {}".format(ticketCount))
    print("Percenatge: {:.2f}%".format(percentage))
    print("Current Income: {}".format(currentPrice))
    print("Total income: {}".format(totalIncome))
    return

def showBookedUserInfo():
    # get userdata json
    with open('userData.json') as f:
        userData = json.load(f)

    ur = int(input("Enter booked seat row: "))
    uc = int(input("Enter booked seat col: "))

    isSeatA = isSeatAvailable(ur - 1, uc - 1)
    if isSeatA == False:
        udata = userData["{}{}".format(ur - 1, uc - 1)]
        print("Name: {}\nGender: {}\nAge: {}\nTicket Price: {}\nPhone No: {}".format(udata["name"], udata["gender"], udata["age"], udata["tprice"], udata["phone"]))
    else:
        print("\nNot Booked yet!!\n")
    return

def main():
    j=print("Welcome to Augie_Cinmex")
    row = int(input("Enter the number of rows:\n"))
    col = int(input("Enter the number of seats in each row:\n"))
    bookingArray = []
    for i in range(0, row):
        aRow = []
        for j in range(0, col):
            
            aRow.insert(j, 0)
        bookingArray.insert(i, aRow)
    tData = json.dumps({ 'row': row, 'col': col, 'bookingArray': bookingArray })

    with open('theaterData.json', 'w+') as json_file:
        json.dump(tData, json_file)

    DisplayOptions()
    selectedOption = int(input())
    while(selectedOption != 0):
       
        if selectedOption == 1:
            showSeats()
        elif selectedOption == 2:
            buyATicket()
        elif selectedOption == 3:
            showStats()
        elif selectedOption == 4:
            showBookedUserInfo()
        DisplayOptions()
        selectedOption = int(input())

if __name__ == "__main__":
    main()