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
* MotherDuck
* Python
* Pandas
* GoCardless API
* Raspberry Pi 4 Model B

### Method
So, obviously, this is no small project. What I am wanting to achieve is a method of automatically and periodically requesting my monthly statement or potentially just any transaction that occurs, performing some basic ETL on it to make it less all over the shop and actually useful data, storing it in a local MariaDB database, then importing this into Power BI to then transform into a report with useful insights about my spending, saving and investing. 
First thing I need to understand, is how a regular schmuck like myself can communicate with the Lloyds Bank API without having a business account. From what I read, I can use **GoCardless**. Some independent users report that the tokens last a "short while", but a "short while" really means 90 days, which is actually pretty standard; if you've ever used services like Plum, you'll know you need to refresh the link to your account every 90 days, so I really don't see that being a problem. Looking at the quick-start guide, it looks like I need to basically need an API key, institution ID, to then get my bank account details, and then hit a transactions endpoint to get this information. So we have a few scripts to run (which I'll include in the repo and possibly refactor to make it user friendly and more of a menu-based script where you can do it all in 1 go, the quickstart guides use cURL but I'm more of a Python and _Requests_ fella, so I rewrote it to be used in Python, so I could then later refactor as mentioned).
The traditional JSON output in python is unformatted and awful, so we can use the _json_ library to tidy it up and format it, and after some tweaking and setting up all the keys and details, we have lift-off!

![image](https://github.com/user-attachments/assets/40c8090a-d6f6-4105-8604-6836dd2f1087)

This is good news. It now means we can access our transactions without having to log on to the banking app or website. We'll tweak and configure this later to work how we need to, for now we'll move on.

Next I need to store the data somewhere. I can't really have it just floating around the output of Visual Studio Code, so first thing is first, we want to test setting up a local DB and test the script works with that. At the initial time of writing, I went with MySQL server to test, but we'll be using MariaDB when it comes to the Pi. Easy enough to set up, locally. Once we have an instance of that running locally, we'll create a schema and table:

![image](https://github.com/user-attachments/assets/8b90db71-7094-4f6b-8b7f-bebdfb70cf23)

Now we have a database, a table for our data and a method of getting the transactions, we need to figure out how to get the JSON output to the database. Python is really cool, in that you can use a _mysql_ library to create a connection to your database. So, we use all the _requests_ code we used previously to hit the endpoint, but we'll tack on some additional code to basically insert it what we get back from the API into the database. I'll include the script used in the repo, but the long and short of it is, we're going to use the _mysql.connector_ library to create a connection to our DB and insert records into the table we've chosen, the _requests_ library to hit the GoCardless endpoint, and the _json_ library to parse the output before inserting into the DB. To test the script, we'll run it without any specific parameters to see if we get anything in:

![image](https://github.com/user-attachments/assets/e50d397e-d27a-412a-97a5-dd0b81afb510)

So, now we know we've got some data in the DB successfully. This is good news. Next is setting the script to only get transactions from the last day, as we don't want duplicate data in our database. What we'll eventually do is create a cron job for the script when I eventually migrate it over to a Pi so it just runs once a day. To start with, we need to check the GoCardless documentation, to understand how we can limit the transactions we pull to certain date/times:

![image](https://github.com/user-attachments/assets/c3437625-629e-4759-bf41-c62bf13d7e40)

Seems simple enough. We need to use the datetime library in our Python script then, and then add some parameters to our json_data. And before we forget, I'm going to start this table fresh, so we'll drop all the records from it first, then reintroduce data to it with strict date/time parameters, to ensure there's no overlap or duplicate records being inserted. 

Now that I'm happy my program works, we'll move on to the more complicated (for me) portion of the project. I have a Raspberry Pi 4 Model B I've had for years, just waiting to be used. I won't run through all the technical instructions and tasks I had to do to set this up, so I'll run through it in bullet points quickly.
* Flashed an SD card with the latest Raspberry Pi OS.
* Installed MariaDB and phpmysql (for a front end for it in case I need it)
* Set up MariaDB in a way that I can login and access the database from outside of the Pi without having to RDP on the Pi.
* Set up the table and it's structure.
* Set up a Cron job for the script to run at midnight every day.

Having tested the cron job, there were a few kinks to work out:
* The INSERT statement needed to be INSERT IGNORE so I don't try to insert dupe transactions by mistake (it outputs an error anyway if it does... believe me, I learned the hard way)
* I forgot that the bearer token only lasts 24 hours, so I had to create an additional script that hits the refresh endpoint with my refresh token, then stores the bearer token that's returned to me.
* Set the above script to run as a cron job 5 minutes prior to the main script.
* Modified the main script to use the new token from the additional script.
* Fixed some dodgy bits around the date functionality.

That's the hardest part of this all pretty much set up, I reckon. It's at this point in the project that I'm slightly adding to the scope of my objectives here; I like the idea of getting my teeth stuck in some more Data Engineering, so what I'd like to do is set up a data warehouse next. I figure what I can do for the ETL process is, instead of making major transformations in Power BI, I set up a MotherDuck data warehouse (they have a free plan that is perfect for what I'd need here), and look to create some sort of pipeline to clean my data, and insert it into the warehouse. Is it pointless? Yes. But the whole point of the project is to practise my current knowledge and develop new knowledge.

According to the MotherDuck documentation, we can use Python to authenticate and connect to our database. So you know what I'm thinking... Another Python cronjob script. 10:20 is when we gather transaction data, 10:30 is when we can run our ETL pipeline and push the clean, useful data into MotherDuck. Especially since MotherDuck has a Power BI-friendly connector too. 

There's no point setting any of this up yet until we have some transformation to perform, though. So, this is what we need to focus on next. Pandas is popular for performing transformations, so we'll use this library. 
In Python, we need to open a connection to the MariaDB, select the data, perform some transformations and send it on its way to MotherDuck. But what transformations? Let's look at what we need:
* Creditor name (but we will use the RemittanceInformationUnstructured for this as CreditorName has a lot of NULLS)
* Amount
* Booking date (value date exists, but is when the amount is actually taken out, personally I would prefer to know when it is that the money is taken)
* Transaction code
* Category (this is a maybe at this point in the transformation, I may leave this to a Power BI transformation as I'm not too sure how we'll be able to categorize it yet, but this will be useful to understand debits that are for savings accounts vs debits that are for costs)

A consideration; Some of the creditor names differ or have numbers on them that we don't really want, so we need to clean the names up. 

Now, setting up the MotherDuck database was relatively straight forward, you can download an exe and use it in PowerShell to connect to your account/database and insert tables and such, so we do so to set up our stucture:
![image](https://github.com/user-attachments/assets/3a3976b0-44b0-4e7d-912a-8a51d8563536)
Now we have the table and basic structure of what we want to see. And we can even see it instantly update in the UI:
![image](https://github.com/user-attachments/assets/a25617c9-52bf-4157-88f2-3b0f7cfa5148)

Now we need to figure out how to connect to the makeshift data warehouse with a Python Script... Which is not a dormant skill I have, so this will be a bit of fiddling around. 

