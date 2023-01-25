# Team Meetings

# Sprint 0/1

### Sprint Schedule
1. Planning -- M Jan 23 - F Jan 27
2. Development -- Sat Jan 28 - F Feb 10
3. Clean-up -- Sat Feb 11 - T Feb 14
4. Presentation -- W Feb 15

### Check-in Dates

* W Jan 25
* W Feb 1
* W Feb 8

### Meeting Notes

F Jan 13 / 1:15 - 2:00 / Dr. Vorachek, Gabby, Julia

- Walked Dr. V through paying for Heroku
- Discussed semester goals
- Got a walk-through of the website
- Site was up and running when we left

M Jan 16, W Jan 18, F Jan 20 / 11:15 - 12:05 / Gabby, Julia

- met during class time in classroom, mostly worked on frontfacing site: https://juliabays.github.io/cps491s23-team04/
- discussed the ongoing issues (Heroku), access, confusing code, admin page

F Jan 20 / 2:30 - 3:30 / Gabby, Dr. Stiffler

- fixed some issues with front facing site
- looked through Heroku issues
- emailed Gabe to try to resolve the issue/set up a meeting

Sun Jan 22 / 11:00 - 11:45 / Gabe Hoban, Gabby, Julia

- need to run npm install from each directory (admin, backend, frontend, convert)
- when logged in to heroku as support, can see the env variables within settings, kept there for security
- how to run locally: 
    - cd into backend
    - npm run dev
    - should be on local host 3000 or 4000?
    - once up, add /admin to the URL to get to admin page
- for logging in to admin page:
    - must first add a UD email to MongoDB under Users collection (must be UD email, @udayton.edu)
    - then should be able to log in through Google Auth
- for uploading spreadsheets:
    - convert directory was created for this
        - convert.py (with the help of helper.py) converts the spreadsheets into a usable/uploadable format
    - *** VERY IMPORTANT ***
        - By uploading the file/running convert.py, you are adding everything from the spreadsheet to the people collection
        - Dr. V keeps one long running file that she updates
        - MUST FOLLOW THESE STEPS
        1. Go into MongoDB
        2. Delete peopleBackup
        3. Change the people name to peopleBackup
        4. Create new people collection (empty)
        - This ensures there is a backup in case there are issues with the excel sheet conversions (apparently very likely, may have to edit the convert.py file each time to cater to any issues)
    - Steps for uploading file:
        - upload/overwrite the excel spreadsheet as source.xlsx within the convert directory (should be at the same level as convert.py and helper.py)
        - Make the above edits to MongoDB ***
        - pip install all the imports at the top of convert.py file
        - run python 3 convert.py
- code overview
    - admin
        - dist = compiled code, what the browser uses
            - js
                - pages
                    aduser = code for add user on admin
            - html code
    - backend
        - dist = distribution
        - src
            - models = in type script (ts), what the DB looks like
            - routes = routes for API
        - app.ts = main file, pulls everything together
        - .htaccess = attempt to not show .html in the URL (something Dr. V wanted, Gabe is not sure if it actually works...)
- Misc
    - Dr. Stiffler has access to CloudFlare, we do not...
        - Dr. V has the domain in her Google account, Google Domains
    - .github/workflows
        - every push to the main branch auto builds to Heroku
    - MongoDB backups - just duplicate each collection and add "backup" to the title
    - will have to rereate the .env file everytime we clone?
- Heroku issue
    - Gabe removed his card information from the support (owner) account
    - Dr. V will need to login as support, enter card info, turn on dynos

W Jan 25 / 11:00 - 11:20 / Gabby, Julia, Dr. Stiffler
- check in meeting
- consider switching to postgres because of data validation issues
- start coming up with a list of last questions for Gabe
- 

W Jan 25 / 11:20 - 12:15 / Gabby, Julia
- got SWJ to run locally on Gabby's laptop
- looked through admin site capabilities
    - we weren't sure why Dr. V doesn't just update/add member info this way, why through a spreadsheet upload?
    - likely because *the edit button doesn't work* (at least not locally... so now makes sense why she doesn't go through the admin page)
- site still not loading, cannot load any memebers, perform any searches, just shows loading
- plan to look through the admin folder to identify what is used for the edit button and submit button, why it isn't working
- determined 3 of Dr. V's main pressing issues are actually just due to typos/data validation issues (no one comes up when you search for 1895-1896, should be one person --> this is because the person is listed as 1894-1896 in the DB... so a typo?)

# Sprint 2

### Sprint Schedule
1. Planning -- Sat Feb 18 - F Feb 24
2. Development -- Sat Feb 25 - F Mar 10
3. Spring Break -- Sat Mar 11 - Sat Mar 18
4. Clean-up -- Sun Mar 19 - T Mar 21
5. Presentation -- W Mar 22

### Check-in Dates

* W Feb 22
* W Mar 1
* W Mar 8



# Sprint 3

### Sprint Schedule
1. Planning -- Sat Mar 25 - F Mar 31
2. Development -- Sat Apr 1 - F Apr 14
3. Clean-up -- Sat Apr 15 - Sun Apr 23
4. Presentation -- M Apr 24
5. Final Presentation -- M May 1

### Check-in Dates

* W Mar 29
* W Apr 12
* W Apr 19
