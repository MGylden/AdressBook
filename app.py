import shutil
import pandas as pd
import csv
from flask import Flask, app, render_template
import time
import ctypes
import threading

"""
Customer er blueprintet/manualen til objektet.
Self er objektet vi derefter laver f.eks. novo nordisk/Maersk/Lego som vi derefter kan give attributes
"""


class Customer:
    def __init__(self, customerId, name, phone, email, adress, contactName, contactPhone, contactEmail, contactJobTitle):
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
    Printer attributes du har defineret tidligere, i en metode.
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


def getCustomers():
    customerList = []
    try:
        with open('static/csv/Customercontactlist.csv', mode="r", newline="") as file:
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                customer = Customer(row["customerId"], row["name"], row["phone"], row["email"], row["adress"],
                                    row["contactName"], row["contactPhone"], row["contactEmail"], row["contactJobTitle"])
                customerList.append(customer)
            file.close()
        for customer in customerList:
            print(customer.printToString())
        print("Tryk Enter for at vende tilbage til menuen.")
        input()
    except Exception:
        print("House is on fire.." + Exception)


def getCustomersFlask():
    customerList = []
    try:
        with open('static/csv/Customercontactlist.csv', mode="r", newline="") as file:
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                customer = Customer(row["customerId"], row["name"], row["phone"], row["email"], row["adress"],
                                    row["contactName"], row["contactPhone"], row["contactEmail"], row["contactJobTitle"])
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
            writer.writerow([customerId, customerName, customerPhone, customerEmail,
                            customerAdress, contactName, contactPhone, contactEmail, contactJobTitle])
        file.close()
    except Exception:
        print("House is on fire.." + Exception)


"""
Først definere vi metoden/funktionen updateCustomer, herefter printer vi "hvad er kundeID"
Derefter får vi input fra brugeren
Herefter åbner vi csv filen med open og indlæser den med DictReader som oversætter csv filen til en dictionary
DictReader bruges i stedet for writer/reader da den læser den første linje og bruger den som "header" og -
kategoriserer dem som f.eks:  {'customerId': '42', 'name': 'Lego', 'phone': '33445566'}
Herefter bruger vi et for loop som læser dictionary og leder efter user input derefter printer den.
Når customerId er fundet breaker vi loopet
"""


def updateCustomer():
    print("Hvad er kundeID?")
    customerId = input()
    fields = ["customerId", "name", "phone", "email", "adress",
              "contactName", "contactPhone", "contactEmail", "contactJobTitle"]

    try:
        with open('static/csv/Customercontactlist.csv', mode="r+", newline="") as file, open('static/csv/tempCustomercontactlist.csv', mode="w+", newline="") as tempOutput:
            reader = csv.DictReader(file, delimiter=';')
            writer = csv.DictWriter(
                tempOutput, fieldnames=fields, delimiter=';')
            writer.writeheader()

            for row in reader:
                if customerId in row["customerId"]:
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

                    writer.writerow(row)
                    print(row)
                else:
                    writer.writerow(row)
            file.close()
            tempOutput.close()
            shutil.move("static/csv/tempCustomercontactlist.csv",
                        "static/csv/Customercontactlist.csv")
        print("Tryk Enter for at vende tilbage til menuen.")
        input()
    except Exception:
        print("House is on fire.." + Exception)


def deleteCustomer():
    print("Hvad er kundeID du vil slette?")
    customerId = input()
    fields = ["customerId", "name", "phone", "email", "adress",
              "contactName", "contactPhone", "contactEmail", "contactJobTitle"]
    foundCustomer = False

    try:
        with open('static/csv/Customercontactlist.csv', mode="r+", newline="") as file, open('static/csv/tempCustomercontactlist.csv', mode="w+", newline="") as tempOutput:
            reader = csv.DictReader(file, delimiter=';')
            writer = csv.DictWriter(
                tempOutput, fieldnames=fields, delimiter=';')
            writer.writeheader()

            for row in reader:
                if customerId in row["customerId"]:
                    print("Kunden er fundet og slettet.")
                    foundCustomer = True
                    continue
                else:
                    writer.writerow(row)
            file.close()
            tempOutput.close()
            shutil.move("static/csv/tempCustomercontactlist.csv",
                        "static/csv/Customercontactlist.csv")
        if foundCustomer == False:
            print("Fandt ikke din kunde, har ikke slettet noget.")
        print("Tryk Enter for at vende tilbage til menuen.")
        input()
    except Exception:
        print("House is on fire.." + Exception)


class FlaskThreadWithException(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        # target function of the thread class
        try:
            while True:
                app.run(host='0.0.0.0', port=9000,
                        debug=True, use_reloader=False)
        finally:
            print('ended')

    def get_id(self):
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                         ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')


def runFlaskApp():
    # Starter "app.run(..)" som en thread. reloader = false da det ikke understøtter threading ud af boksen.
    threading.Thread(target=lambda: app.run(
        host='0.0.0.0', port=9000, debug=True, use_reloader=False), name="flaskThread").start()


# #Definere objekter med data og smider dem i en samlet liste nederst
# novonordisk = Customer(1, "Novo Nordisk", 9999999, "novonordisk@novonordisk.dk", "Novo nordisk vej 42, Bagsværd", "Birgitte", 22334455, "Birgitte@novonordisk.dk", "Supervisor")
# maersk = Customer(2, "Maersk", 88888888, "maersk@maersk.dk", "Maerskvej 1, København", "Birgit", 11223344, "birgit@maersk.dk", "HR Manager")
# lego = Customer(3, "Lego", 77777777, "lego@lego.dk", "legovej 1, Billund", "Mads", 44556677, "mads@lego.dk", "CTO")
# customerList = (novonordisk, maersk, lego)
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html", customers=getCustomersFlask())


def main():
    choice = ""
    # runFlaskApp()
    flaskThread = FlaskThreadWithException("FlaskThread")
    flaskThread.start()
    # Da ovenstående er en thread, forstætter den før at Flask webservicen
    # rent faktisk er startet op, derfor venter vi 2 sekunder.
    time.sleep(2)
    input("Flask app running, press any button to continue...")

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

        # match matcher user input med nedenstående case, klikker jeg f.eks. 1 kører koden for "case 1"
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
                # Luk Flask Thread
                flaskThread.raise_exception()
                # Join Thread ind til mail thread
                flaskThread.join()
                # vent pænt...
                time.sleep(2)
                # luk ned :)
                quit()
            case _:
                print("Invalid choice!")


if __name__ == "__main__":
    main()
