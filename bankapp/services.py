from flask import Flask, request
from bankapp.models import *
import json


@app.route("/bank/service/", methods=['POST'])
def withdraw_amount():
    reqbody = request.get_json()
    print(reqbody)
    banknm = reqbody['bankname']  # customer which bank
    mobile = int(reqbody['mobile'])  # which customer
    vendor = reqbody['vendor']  # deposit
    amount = int(reqbody['amount'])  # amount
    bank = Bank.query.filter(Bank.bankname == banknm).first()
    if not bank:
        return json.dumps({"status": "Invalid Bank..!"})

    serviceprovider = Customer.query.filter(Customer.name==vendor).first()
    if not serviceprovider:
        return json.dumps({"status" : "Invalid service provider"})
    elif not serviceprovider.bankaccref:
        return json.dumps({"status" : "service provider does not have accont"})

    if not int(amount) or int(amount) <= 0:
        return json.dumps({"status" : "Invalid amount"})

    customer = Customer.query.filter(Customer.contact==mobile).first()
    if not customer:
        return json.dumps({"status" : "Mobile number is not associated with bank record"})
    elif customer.bankaccref:
        for record in customer.bankaccref:
            print("info", record)
            if record.get_bank_instance().bankname == bank.bankname and record.get_customer_instance().contact == mobile:
                custacc = record.get_account_instance()
                serviceacc = serviceprovider.bankaccref[0].get_account_instance()
                existing = custacc.balance
                print(f'Existing customer balance {custacc.balance}')
                print(f'Existing vendor balance {serviceacc.balance}')
                custacc.balance -= amount
                serviceacc.balance += amount
                db.session.commit()
                print(f'Existing customer balance {custacc.balance}')
                print(f'Existing vendor balance {serviceacc.balance}')
                return json.dumps('Customer Existing balance {}, current Balance {}'.format(existing, custacc.balance))
        return json.dumps({"status": "Customer--Account--Bank details not matching..!"})

    return json.dumps({"status": "Service is down for the time being.!"})

if __name__ == '__main__':
    app.run(debug=True)