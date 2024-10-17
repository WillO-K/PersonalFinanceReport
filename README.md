# Personal Finance Report

### Background
As I look to start properly budgeting and diversifying my investments, it occurred to me that there's none more suited to the task than myself - a career analyst with a brand new qualification in Power BI. So, I set myself a task of creating a personal finance report. But I didn't want this to be a manual process, where I download the bank statements myself, import them into Power BI and continually do this, I figure why not automate it and make things a bit more smart. 

### Goals
1. Automate the download and ETL of my banking transactions.
2. Analyse outgoings data pulled from my banking statements.
3. Create a database server on a Raspberry Pi that we can query from any device on the network.
4. Use multiple technologies to extend my knowledge in the fields of software development, database administration/SQL development, Data Engineering and Data Analysis/Business Intelligence (ish)
#### Questions
* What are the regular outgoings that are consistently occuring at same time every month?
* What outgoings seem erroneous, that could potentially be marked for cut-down?
* What is the remainder of my income after regular/consistent payments have been completed?
* When savings are calculated and taken into account, what return can I expect to see out of them over the course of a calendar year?

#### Tools
* Microsoft Power BI
* MariaDB
* MotherDuck (or will be using in the future)
* Python
* GoCardless API
* Raspberry Pi 4 Model B

### GoCardlessSetup
To get your banking data, you need to basically connect your bank account to GoCardless. I found the process quite tedious to be honest, so I whipped up GoCardlessSetup.py to make the whole process a bit easier (ish) so if I need to come back and go through it again, I don't need to find and follow the API docs again and have all these cURL commands knocking around. 

GoCardlessSetup.py uses the requests library to basically emulate the cURL requests that GoCardless provide in their developer/quick start documentation, and take you step by step through the process. It's worth having a read of the documenation anyway, so you're familiar with the terminology, but if you're not really super up to speed with cURL and the likes, this makes things a bit easier. 

The JSON library helps tidy things up a bit in terms of the output too, so it's not dreadful to read. The script isn't perfect by any means, but it got the job done.

![image](https://github.com/user-attachments/assets/7f54a600-3199-41ad-b89d-9861ca8090bc)

### TransactionGrabber
Once the link to your bank is set up, you're ready to start querying for data. TransactionGrabber.py is meant to run automatically, I have it running as a crob job on a Raspberry Pi at the moment, but will be transitioning it to an actual server at some point in the future (when I can be bothered to set one up). 

The idea behind TransactionGrabber.py is to grab all transactions from the previous day and inserts them into a Maria/MySQL database. It's currently working quite smoothly for me, it's probably not optimal and there will be 100 things obviously wrong on it, to an actual Python Dev, but given that I am not a Python Dev, and the fact it works for what I need it for, I'm not too fussed. 

### GetNewToken
Your bearer token expires every 24 hours, and manually refreshing it was not an option because it's a massive PITA, so GetNewToken.py automates the refreshing of the token. Pop in the refresh token, and whack on a cron job for it, and you now have a way to refresh the token every 24 hours. Makes life a bit easier for me, and means I can basically have everything running automatically and quite smoothly (until I need to refresh my connection with the bank every 90 days, but I don't think there's an automatic way of doing this and is pretty much standard for businesses who deal with this too).

### Database
I'm using a MariaDB to store all my data in currently. It's open source and fairly easy to work with. The table structure looks like this:

![image](https://github.com/user-attachments/assets/58070f55-6241-43dc-bdfc-40f905a1941e)

This is also running on the Raspberry Pi. 

### Exploratory Analysis
The goal is to eventually get an instance of Motherduck up and running, at which point we'll create a pipeline that does all the ETL we need and ingests it into the Motherduck "data warehouse". But for the time being (as I don't have the time for this right now), we'll do some exploratory analysis on the data we have in the MariaDB, so we'll start by cleaning some of it in Power Query:

![image](https://github.com/user-attachments/assets/92e21aec-0e7c-4efe-9071-3f963ffe8654)

We'll create a date table too:

![image](https://github.com/user-attachments/assets/c589768a-8b6c-4433-992f-bd4bd8983f98)

And we'll (for now) use DAX to categorise transactions based on some conditions (we'll eventually do all this in either the SQL that queries the DB or just have it done in the pipeline to Motherduck so it keeps the model small):

![image](https://github.com/user-attachments/assets/e76e4d48-ebc1-475b-989d-7ebd0c93183d)

TBC

