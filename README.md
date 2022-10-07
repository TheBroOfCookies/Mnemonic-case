# Mnemonic-case

## Description
The REST API has been implemented in accordance to the requirements given. Being able to execute a transaction between two bank accounts. This is done by POST-ing a new trasaction json object to  the address url/transactions. This must contain the id of the source and destination bank accounts as well as teh amount of cash to transfer.
Extra added functionaloity is GET on either url/accounts or url/transactions to return all accounts or transactions in the system. For a real world use on a website the url would likely be changed to url/api/newTransaction to seperate all the api calls form the users tring to use the website. 
The data structures for accounts and transactions are saved in json files (accounts_data.json and transactions_data.json)

## Requirements
- Requires Python3
- With modules json, flask and time

## How to run
To run the server with the API simply run the python file api.py. Default config for the url is http://127.0.0.1:5100 (or simply http://localhost:5100)

## Testing
To test that the requirements are met a rest clint (Advanced Rest Client) has been used. Curl can also be used for this purpose. The validity of the tests depend on the test caes. Which have been transfering with negative cash amount. Transfering from an account that does not have sufficient funds. Having the source and destiantion accounts be the same account. And ofcourse trying to transfer a valid amount form an existing account with coverage to another valid and existing account. all the tests have been performed by sending POST requests with json objects to http://localhost:5100/transactions

## Other scenarios
In a more complex scenario we would likely have to validate the users ownership of an account before allowing transfer of cash. Such as with login credentials matching certain accounts. Account creation and manipulation would also need to be adressed. This would include things such as POST-ing new accounts. Deleting obsolete accounts and depositing of withdrawing cash. New accounts would be POST onto url/accounts. Changing account balance PUT on url/accounts/<id>, where <id> is the account id. 
