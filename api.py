import json
from flask import Flask, request, jsonify
import time


api = Flask(__name__)

def next_transaction_id():
    with open('transactions_data.json') as savefile:
        transactions = json.load(savefile)
    maxId = -1
    for transaction in transactions:
        maxId = max(transaction.get("id"), maxId)
    return maxId + 1

#Helper methods for file input and output
def read_accounts_from_file():
    with open('accounts_data.json') as savefile:
         return json.load(savefile)
     
def write_accounts_to_file(accounts):
    with open('accounts_data.json', 'w') as savefile:
        json.dump(accounts, savefile)

def read_transactions_from_file():
    with open('transactions_data.json') as savefile:
         return json.load(savefile)
     
def write_transactions_to_file(transactions):
    with open('transactions_data.json', 'w') as savefile:
        json.dump(transactions, savefile)

@api.get("/accounts")
def get_accounts():
    return read_accounts_from_file()

@api.get("/transactions")
def get_transactions():
    return read_transactions_from_file()

@api.get("/accounts/<int:id>")
def get_account(id):
    accounts = read_accounts_from_file()
    for account in accounts:
        if account.get("id") == id:
            return jsonify(account)
    return "Error, account does not exist", 404

@api.post("/transactions")
def make_transaction():
    if(request.is_json):
        accounts = read_accounts_from_file()
        transactions = read_transactions_from_file()
        #Json parsing and transaction intial varibales are set
        transaction = request.get_json()
        transaction["registeredTime"] = int(time.time() * 1000)
        transaction["successTime"] = 0
        transaction["id"] = next_transaction_id()
        transaction["success"] = False
        
        #Helper variables are fetched from json input
        sourceId = transaction.get("sourceAccountId")
        destId = transaction.get("destinationAccountId")
        amountToTransfer = transaction.get("cashAmount")
        print(amountToTransfer)
        if(amountToTransfer == 0):
            return "Wrong json request format", 400
        
        #Checks are run to see if the transaction is legal or not
        #Assumption, source and destination id must be different
        if(sourceId == destId):
            return "Error, source and destination account cannot be the same", 400
        sourceAccount = []
        destAccount = []
        for account in accounts:
            if account.get("id") == sourceId:
                sourceAccount = account
            if account.get("id") == destId:
                destAccount = account
        if sourceAccount == []:
            return "Error, Source account not found", 400
        if destAccount == []:
            return "Error, Destination account not found", 400
        if amountToTransfer <= 0:
            return "Error, cash amount to transfer must be greater than 0", 400
        if sourceAccount.get("availableCash") < amountToTransfer:
            return "Error, source account does not have enough cash", 400
        
        #If all the checks are good we do the account transfer and record the transaction
        sourceAccount["availableCash"] = sourceAccount.get("availableCash") - amountToTransfer
        destAccount["availableCash"] = destAccount.get("availableCash") + amountToTransfer
        transaction["successTime"] = int(time.time() * 1000)
        transaction["success"] = True
        transactions.append(transaction)
        
        write_transactions_to_file(transactions)
        write_accounts_to_file(accounts)
        
        return jsonify(transaction), 200
    else:
        return "Error, request was not a json", 400


if __name__ == '__main__':
    api.run(host="0.0.0.0", port=5100, debug=True)