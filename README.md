# Personal Finance Report

### Background
As I look to start properly budgeting and diversifying my investments, it occurred to me that there's none more suited to the task than myself - a career analyst with a brand new qualification in Power BI. So, I set myself a task of creating a personal finance report. But I didn't want this to be a manual process, where I download the bank statements myself, import them into Power BI and continually do this, I figure why not automate it and make things a bit more smart. 

### Goals
1. Automate the download and ETL of my banking transactions.
2. Analyse outgoings data pulled from my banking statements. 
#### Questions
* What are the regular outgoings that are consistently occuring at same time every month?
* What outgoings seem erroneous, that could potentially be marked for cut-down?
* What is the remainder of my income after regular/consistent payments have been completed?
* When savings are calculated and taken into account, what return can I expect to see out of them over the course of a calendar year?

#### Tools
* Microsoft Power BI
* MySQL
* Python
* GoCardless API

### Method
So, obviously, this is no small project. What I am wanting to achieve is a method of automatically and periodically requesting my monthly statement or potentially just any transaction that occurs, performing some basic ETL on it to make it less all over the shop and actually useful data, storing it in a local MySQL database, then importing this into Power BI to then transform into a report with useful insights about my spending, saving and investing. 
First thing I need to understand, is how a regular schmuck like myself can communicate with the Lloyds Bank API without having a business account. From what I read, I can use **GoCardless**. Some independent users report that the tokens last a "short while", but a "short while" really means 90 days, which is actually pretty standard; if you've ever used services like Plum, you'll know you need to refresh the link to your account every 90 days, so I really don't see that being a problem. Looking at the quick-start guide, it looks like I need to basically need an API key, institution ID, to then get my bank account details, and then hit a transactions endpoint to get this information. So we have a few scripts to run (which I'll include in the repo and possibly refactor to make it user friendly and more of a menu-based script where you can do it all in 1 go, the quickstart guides use cURL but I'm more of a Python and _Requests_ fella, so I rewrote it to be used in Python, so I could then later refactor as mentioned).
The traditional JSON output in python is unformatted and awful, so we can use the _json_ library to tidy it up and format it, and after some tweaking and setting up all the keys and details, we have lift-off!
![image](https://github.com/user-attachments/assets/40c8090a-d6f6-4105-8604-6836dd2f1087)
This is good news. It now means we can access our transactions without having to log on to the banking app or website. We'll tweak and configure this later to work how we need to, for now we'll move on.

Next I need to store the data somewhere. I can't really have it just floating around the output of Visual Studio Code, so what we need to do is set up a local database. MySQL is the obvious choice. Easy enough to set up, locally (though in the future, we'll migrate it to a RaspPi or OrangePi I suspect, so I can have the DB and the script running constantly). Once we have an instance of that running locally, we'll create a schema and table:
![image](https://github.com/user-attachments/assets/8b90db71-7094-4f6b-8b7f-bebdfb70cf23)

Now we have a database, a table for our data and a method of getting the transactions, we need to figure out how to get the JSON output to the database. Python is really cool, in that you can use a _mysql_ library to create a connection to your database. So, we use all the _requests_ code we used previously to hit the endpoint, but we'll tack on some additional code to basically insert it what we get back from the API into the database. I'll include the script used in the repo, but the long and short of it is, we're going to use the _mysql.connector_ library to create a connection to our DB and insert records into the table we've chosen, the _requests_ library to hit the GoCardless endpoint, and the _json_ library to parse the output before inserting into the DB. To test the script, we'll run it without any specific parameters to see if we get anything in:
![image](https://github.com/user-attachments/assets/e50d397e-d27a-412a-97a5-dd0b81afb510)
So, now we know we've got some data in the DB successfully. This is good news. Next is setting the script to only get transactions from the last day, as we don't want duplicate data in our database. What we'll eventually do is create a cron job for the script when I eventually migrate it over to a Pi so it just runs once a day. To start with, we need to check the GoCardless documentation, to understand how we can limit the transactions we pull to certain date/times:
![image](https://github.com/user-attachments/assets/c3437625-629e-4759-bf41-c62bf13d7e40)
Seems simple enough. We need to use the datetime library in our Python script then, and then add some parameters to our json_data. And before we forget, I'm going to start this table fresh, so we'll drop all the records from it first, then reintroduce data to it with strict date/time parameters, to ensure there's no overlap or duplicate records being reinserted. 
