from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost/bank'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class Customer(db.Model):
    custid = db.Column('cust_id', db.Integer(), primary_key=True)
    name = db.Column('cust_name', db.String(50))
    age = db.Column('cust_age', db.Integer())
    email = db.Column('cust_email', db.String(50))
    address = db.Column('cust_address', db.String(50))
    contact = db.Column('cust_contact', db.BigInteger())
    bankaccref = db.relationship('Bank_Cust_Account', backref="custref", lazy=True, uselist=True)


class Account(db.Model):
    accno = db.Column('acc_id', db.Integer(), primary_key=True)
    type = db.Column('acc_type', db.String(50))
    balance = db.Column('acc_bal', db.Float())
    bankcustref = db.relationship('Bank_Cust_Account', backref="accref", lazy=True, uselist=True)


class Bank_Cust_Account(db.Model):
    id = db.Column('id', db.Integer(), primary_key=True)
    bankid = db.Column('bank_id', db.ForeignKey('bank.bank_id'), unique=False)
    custid = db.Column('cust_id', db.ForeignKey('customer.cust_id'), unique=False)
    accid = db.Column('acc_id', db.ForeignKey('account.acc_id'), unique=True)

    def get_bank_instance(self):
        return Bank.query.filter_by(bankid=self.bankid).first()

    def get_account_instance(self):
        return Account.query.filter_by(accno=self.accid).first()

    def get_customer_instance(self):
        return Customer.query.filter_by(custid=self.custid).first()

    def get_all_details(self):
        return self.get_account_instance(), self.get_bank_instance(), self.get_customer_instance()

    
class Bank(db.Model):
    bankid = db.Column('bank_id', db.Integer(), primary_key=True)
    bankname = db.Column('bank_name', db.String(100))
    custaccref = db.relationship(Bank_Cust_Account, backref="bankref", lazy=True, uselist=True)





import sys
if __name__ == '__main__':

    db.create_all()

    b1 = Bank(bankid=112233, bankname='SBI')
    b2 = Bank(bankid=423433, bankname='HDFC')
    b3 = Bank(bankid=124233, bankname='ICICI')

    db.session.add_all([b1, b2, b3])
    db.session.commit()
    print('Bank Records Created..!')

    c1 = Customer(custid=101, name='XXXX', age=20, email='abc@gmail.com', address='Pune', contact=7778888888)
    c2 = Customer(custid=102, name='XXXX', age=26, email='yyy@gmail.com', address='Pune', contact=8888888888)
    c3 = Customer(custid=103, name='Hotel', age=29, email='zzz@gmail.com', address='Pune', contact=9998888888)
    db.session.add_all([c1, c2, c3])
    db.session.commit()
    print('Customer Records Created..!')

    ac1 = Account(accno=172633, type='saving', balance=78823.3)
    ac2 = Account(accno=123633, type='saving', balance=62823.3)
    ac3 = Account(accno=238633, type='saving', balance=5823.3)
    ac4 = Account(accno=12312, type='current', balance=24823.3)
    ac5 = Account(accno=12333, type='current', balance=123823.3)
    db.session.add_all([ac1, ac2, ac3, ac4, ac5])
    db.session.commit()
    print('Account Records Created..!')

    bca1 = Bank_Cust_Account(bankid=112233, custid=101, accid=172633)
    bca2 = Bank_Cust_Account(bankid=112233, custid=102, accid=123633)
    bca3 = Bank_Cust_Account(bankid=423433, custid=102, accid=238633)
    bca4 = Bank_Cust_Account(bankid=423433, custid=103, accid=12312)
    bca5 = Bank_Cust_Account(bankid=124233, custid=102, accid=12333)
    db.session.add_all([bca1, bca2, bca3, bca4, bca5])
    db.session.commit()