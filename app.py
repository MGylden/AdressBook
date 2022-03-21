import shutil
import pandas as pd
import csv
from flask import Flask, app, render_template

"""
Customer er blueprintet/manualen til objektet. 
"""
class Customer:
    def __init__(self, customerId, name, phone, email, adress, contactName, contactPhone, contactEmail, contactJobTitle) :
        self.customerId = customerId
        self.name = name
        self.phone = phone
        self.email = email
        self.adress = adress
        self.contactName = contactName
        self.contactPhone = contactPhone
        self.contactEmail = contactEmail
        self.contactJobTitle = contactJobTitle
    
    """
    Printer attributes du har defineret tidligere oppe i en metode.
    """
    def printToString(self):
        print("Kunde ID: " + self.customerId)
        print("Kunde Navn: " + self.name)
        print("Kunde Telefon: " + self.phone)
        print("Kunde Email: " + self.email)
        print("Kunde Adresse: " + self.adress)
        print("Kontakt Navn: " + self.contactName)
        print("Kontakt Tlf Nummer: " + self.contactPhone)
        print("Kontakt E-Mail: " + self.contactEmail)
        print("Kontakts Stilling: " + self.contactJobTitle)

"""
Først definere vi funktionen getCustomers
Herefter opretter vi en liste customerList = []
Så kører vi try except block
Så kører vores open function der åbner vores csv fil.
herefter laver vi vores reader DictReader bruges i stedet for normal reader da den læser den første linje og bruger den som "header" og kategoriserer dem i key value pairs 
Så laver vi vores for loop igennem csv filen, herefter laver vi en variabel i for loopet så vi henter vores class ind, og derefter smider vi vores class ind i en liste og appender det.
Herefter kører vores andet for loop som looper igennem vores customerlist og printer vores loop og function (printToString) vi har defineret op over
"""
def getCustomers():
    customerList = []
    try:
        with open('static/csv/Customercontactlist.csv', mode="r", newline="") as file:
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                customer = Customer(row["customerId"], row["name"], row["phone"], row["email"], row["adress"], row["contactName"], row["contactPhone"], row["contactEmail"], row["contactJobTitle"])
                customerList.append(customer)
            file.close()
        for customer in customerList:
            print(customer.printToString())
        print("Tryk Enter for at vende tilbage til menuen.")
        input()
    except Exception:
        print("House is on fire.." + Exception)
"""
her gør vi samme som ovenstående men returnere data så vi kan bruge den bearbejdede data udenfor vores funktion. 
Vi bruger denne data til at display det via Flask
"""
def getCustomersFlask():
    customerList = []
    try:
        with open('static/csv/Customercontactlist.csv', mode="r", newline="") as file:
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                customer = Customer(row["customerId"], row["name"], row["phone"], row["email"], row["adress"], row["contactName"], row["contactPhone"], row["contactEmail"], row["contactJobTitle"])
                customerList.append(customer)
            file.close()
        return customerList
    except Exception:
        print("House is on fire.." + Exception)

def createCustomer():
    print("Hvad er KundeID")
    customerId = input()
    print("Hvad er navnet på virksomheden?")
    customerName = input()
    print("Hvad er Tlf Nummeret?")
    customerPhone = input()
    print("Hvad er E-Mail?")
    customerEmail = input()
    print("Hvad er adressen?")
    customerAdress = input()
    print("Hvad er kontaktpersonens navn?")
    contactName = input()
    print("Hvad er kontaktpersonens tlf Nummer?")
    contactPhone = input()
    print("Hvad er kontaktpersonens E-Mail?")
    contactEmail = input()
    print("Hvad er kontaktpersonens Jobtitel")
    contactJobTitle = input()


    try:
        with open('static/csv/Customercontactlist.csv', mode="a", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow([customerId, customerName, customerPhone, customerEmail, customerAdress, contactName, contactPhone, contactEmail, contactJobTitle])
        file.close()
    except Exception:
        print("House is on fire.." + Exception)

"""
Først definere vi funktionen updateCustomer, herefter printer vi 
Derefter opretter vi en variabel som vi kalder customerId, som får vi input fra brugeren
Herefter opretter vi endnu en variabel "fields" som indeholder vores headers vi indlæser i "writer (fieldnames=fields)
Herefter laver vi en boolean som vi kalder foundCustomer og sætter den til false da vi ikke den ikke vil kunne finde noget- den går så ind i vores for loop og tjekker om det "true", 
 - hvis den ikke kan finde user input der matcher med data i csv filen bruger vi den igen i linje 202 og hvis foundCustomer er false printer vi, dette gør vi for at kunne melde tilbage til brugeren om det lykkedes eller ej
Så laver vi en try except block
Herefter åbner vi csv filen med open og indlæser den med DictReader som oversætter csv filen til en dictionary
DictReader bruges i stedet for normal reader da den læser den første linje og bruger den som "header" og 
- kategoriserer dem i key value pairs f.eks:  {'customerId': '42', 'name': 'Lego', 'phone': '33445566'}
Herefter bruger vi DictWriter som åbner en ny midlertidig fil som vi kalder tempCustomercontactlist.csv da csv reader/writer ikke tillader os at opdatere direkte i filen 
- da filen er læst af reader, derfor åbner vi en ny fil vi kan skrive i og derefter flytter vores temp fil til customercontactlist.csv og sletter vores temp fil 
Herefter bruger vi et for loop som vi kalder row, den læser dictionary og leder efter user input(customerId) i csv filen, herefter printer vi næste linje og 
- beder igen om input dette fortsætter, herefter kommer vores if statements, så if newcompanyname(userinput = blankt så skal den sætte det til det originale fra csv filen) 
- altså hvis vi bare klikker f.eks. "Enter" at den ikke bare opdatere det til blankt.   
hvis den så ikke kan finde det specifikke customerId fra user input bruger vi en else statement til at skrive det samme data som står i vores Customercontactlist.csv i vores temp fil.
Herefter lukker vi filerne og flytter vores temp liste over i vores Customerlist det gør vi med modulet shutil. 
"""

def updateCustomer():
    print("Hvad er kundeID?")
    customerId = input()
    fields = ["customerId", "name", "phone", "email", "adress", "contactName", "contactPhone", "contactEmail", "contactJobTitle"]
    foundCustomer = False
    
    try:
        with open('static/csv/Customercontactlist.csv', mode="r+", newline="") as file, open('static/csv/tempCustomercontactlist.csv', mode="w+", newline="") as tempCustomerList:
            reader = csv.DictReader(file, delimiter=';')
            writer = csv.DictWriter(tempCustomerList, fieldnames=fields, delimiter=';')
            writer.writeheader()

            for row in reader:
                if customerId == row["customerId"]:
                    print("Found your customer!")
                    print(row)
                    print("hvad er det nye virksomhedsnavn?")
                    newCompanyName = input()
                    print("hvad er det nye Tlf Nummer?")
                    newCompanyPhone = input()
                    print("hvad er den nye e-Mail?")
                    newCompanyEmail = input()
                    print("hvad er det nye adress?")
                    newCompanyAdress = input()
                    print("hvad er det nye kontaktnavn?")
                    newContactName = input()
                    print("hvad er det nye kontakt tlf Nummer?")
                    newContactPhone = input()
                    print("hvad er det nye kontakt E-Mail?")
                    newContactEmail = input()
                    print("hvad er det nye Kontakts Jobtitel?")
                    newContactJobTitle = input()

                    if newCompanyName:
                        row["name"] = newCompanyName
                    if newCompanyPhone:
                        row["phone"] = newCompanyPhone
                    if newCompanyEmail:
                        row["email"] = newCompanyEmail
                    if newCompanyAdress:
                        row["adress"] = newCompanyAdress
                    if newContactName:
                        row["contactName"] = newContactName
                    if newContactPhone:
                        row["contactPhone"] = newContactPhone
                    if newContactEmail:
                        row["contactEmail"] = newContactEmail
                    if newContactJobTitle:
                        row["contactJobTitle"] = newContactJobTitle
                    foundCustomer = True
                    writer.writerow(row)
                    print(row)
                else:
                    writer.writerow(row)
            file.close()
            tempCustomerList.close()
            shutil.move("static/csv/tempCustomercontactlist.csv", "static/csv/Customercontactlist.csv")
        if foundCustomer == False:
            print("Fandt ikke din kunde.")
        print("Tryk Enter for at vende tilbage til menuen.")
        input()
    except Exception:
        print("House is on fire.." + Exception)

"""
Først definere vi metoden/funktionen deleteCustomer, herefter printer vi 
Derefter opretter vi en variabel som vi kalder customerId, som får vi input fra brugeren
Herefter opretter vi endnu en variabel "fields" som indeholder vores headers vi indlæser i "writer (fieldnames=fields)
Herefter laver vi en boolean som vi kalder foundCustomer og sætter den til false da vi ikke den ikke vil kunne finde noget- den går så ind i vores for loop og tjekker om det "true", 
 - hvis den ikke kan finde user input der matcher med data i csv filen bruger vi den igen i linje 202 og hvis foundCustomer er false printer vi, dette gør vi for at kunne melde tilbage til brugeren om det lykkedes eller ej
Herefter åbner vi csv filen med open og indlæser den med DictReader som oversætter csv filen til en dictionary
DictReader bruges i stedet for normal reader da den læser den første linje og bruger den som "header" og 
- kategoriserer dem i key value pairs f.eks:  {'customerId': '42', 'name': 'Lego', 'phone': '33445566'}
Herefter bruger vi DictWriter som åbner en ny midlertidig fil som vi kalder tempCustomercontactlist.csv da csv reader/writer ikke tillader os at opdatere direkte i filen 
 - da filen er læst af reader, derfor åbner vi en ny fil vi kan skrive i og derefter flytter vores temp fil til customercontactlist.csv og sletter vores temp fil 
Herefter bruger vi et for loop som vi kalder row, den læser dictionary og leder efter user input i csv filen, hvis den finder customerId fortsætter den bare loopet og
 - springer den linje over/skipper den og dermed er vores data slettet.
hvis den så ikke kan finde det specifikke customerId fra user input bruger vi en else statement til at skrive det samme data som står i vores Customercontactlist.csv i vores temp fil.
Herefter lukker vi filerne og flytter vores temp liste over i vores Customerlist det gør vi med modulet shutil. 
"""

def deleteCustomer():        
    print("Hvad er kundeID du vil slette?")
    customerId = input()
    fields = ["customerId", "name", "phone", "email", "adress", "contactName", "contactPhone", "contactEmail", "contactJobTitle"]
    foundCustomer = False
    
    
    try:
        with open('static/csv/Customercontactlist.csv', mode="r+", newline="") as file, open('static/csv/tempCustomercontactlist.csv', mode="w+", newline="") as tempCustomerList:
            reader = csv.DictReader(file, delimiter=';')
            writer = csv.DictWriter(tempCustomerList, fieldnames=fields, delimiter=';')
            writer.writeheader()

            for row in reader:
                if customerId in row["customerId"]:
                    print("Kunden er fundet og slettet.")
                    foundCustomer = True
                    continue
            file.close()
            tempCustomerList.close()
            shutil.move("static/csv/tempCustomercontactlist.csv", "static/csv/Customercontactlist.csv")
        if foundCustomer == False:
            print("Fandt ikke din kunde, har ikke slettet noget.")
        print("Tryk Enter for at vende tilbage til menuen.")
        input()
    except Exception:
        print("House is on fire.." + Exception)


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", customers=getCustomersFlask())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)

#Her opretter vi variablen choice som vi sætter til ingenting, nedenunder bruger vi så choice.  
choice = ""
"""
Laver et while loop som fortsætter indtil du indtaster nummeret 5
!= betyder hvis du ikke indtaster 5 kører programmet fortsat men hvis du indtaster 5 afsluttes der.
Menuen indlæses print(1 til 5)
Herefter printes muligheder ud fra user input
"""

while choice != "5":
    print("1. Show customers.")
    print("2. Opret kunde.")
    print("3. Opdatér kunde")
    print("4. Slet kunde")
    print("5. Exit")
    print("Skriv tal for valg.")
    choice = input()

  

    #match matcher user input med nedenstående case, klikker jeg f.eks. 1 kører metoden for "case 1" 
    match choice:
        case '1':
            getCustomers()
        case '2':
            createCustomer()
        case '3':
            updateCustomer()
        case '4':
            deleteCustomer()
        case '5':
            print("Alright, cya!")
            quit()
        case _:        
            print("Invalid choice!")