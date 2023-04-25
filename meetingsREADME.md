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

W Jan 25 / 11:20 - 12:15 / Gabby, Julia

- got SWJ to run locally on Gabby's laptop
- looked through admin site capabilities
    - we weren't sure why Dr. V doesn't just update/add member info this way, why through a spreadsheet upload?
    - likely because *the edit button doesn't work* (at least not locally... so now makes sense why she doesn't go through the admin page)
- site still not loading, cannot load any memebers, perform any searches, just shows loading
- plan to look through the admin folder to identify what is used for the edit button and submit button, why it isn't working
- determined 3 of Dr. V's main pressing issues are actually just due to typos/data validation issues (no one comes up when you search for 1895-1896, should be one person --> this is because the person is listed as 1894-1896 in the DB... so a typo?)

F Jan 27 / 11:10 - 12:15 / Gabby, Julia

- errors on Heroku: SSL certificate / Domain
- website worked on F Jan 13 when we first set it up with Dr. V, now doesn't load, we have not touched the code...
    - hoping it is just the heroku error???
    - when trying to load member list the inspect --> console gives these errors
        - Access to XMLHttpRequest at 'https://swj1894.org/api/v1/person/list' from origin 'https://swj-capstone.herokuapp.com' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.   MembersList.html:1     
        - GET https://swj1894.org/api/v1/person/list net::ERR_FAILED 200     DisplayMembers.js:736 
    - think this is all because the URL is now ...herokuapp.com, the domain is supposed to be http://swj1894.org   
- there are edit functions on the admin page but they don't work...
    - could it just be that nothing is working/loading corerctly
- ********************************everything just changed...*******************************************
- *we were looking at https://swj-capstone.herokuapp.com/ ... supposed to be https://swj1894.org ... :|*
- "open app" button on Heroku is not corrected to the correct URL
- *Important question: does the code push to the correct site?*
- *so... now everything works*
- Dr. V should probably just make all changes through the admin page
    - shouldn't be uploading full spreadsheets... just make the changes directly to the site
        - unless she hates this idea maybe??
    - already a way to export the data through multiple ways (excel, pdf, print, csv...)
- possible that she would like the date ranges to work correctly, and that not all errors are really errors...
    - The person that doesn't come up for the date range 1913-1914 is listed as active during the range 1912-1915
        - so technically that person *was* active during the 1913-1914 range, so maybe the ranges are too specific?
        - *ask Dr. V about this*
- Already fixed one of the issues for Pearl, must have just been a typo, took 30 seconds to fix through updating the user on the admin page
- Our current ideas
    - maybe can quickly fix the majority of the main issues she listed (mostly just typos)
        - typos, contributors page, bio/notes box are all of the high priority issues
    - start on the notes/bio box in the admin page
    - also maybe can ignore the DB change thoughts and move on to replacing the pop up windows with actual pages
- Our current plan
    - wait for Gabby to ask/tell Dr. Stiffler about all of this
    - then go fix all the typos/contributors page
    - how do we go about telling/asking Dr. V why she doesn't use the admin page/ is she committed to excel spreadsheets/wouldn't want to change
        - maybe have to change the format of the excel spreadsheet to get her to agree to update only through admin page
            - Dr. Stiffler says to leave the database how it is, advise Dr. V to edit using admin page, look into sessions to stop using pop up windows for results
            - recommends asking for one final spreadsheet and manually going through it to fix any errors in DB

M Jan 30 / 11:10 - 11:50 / Gabby, Julia
- Plan:
    - get spreadsheet
    - divide between the two of us and verify all of it/fix any errors in DB
    - meet with Dr. V to tell her to use admin page -- do this week
    - start on other stuff
- After errors fixed:
    - contributors page -- do this week
    - bio box on admin but add to site
    - prefixes (Mrs)
    - notes for admin side only
    - link people with changing last names
    - sessions
- Emailed Dr. V asking for latest spreadsheet and updating her
- Meet Friday or early next week with Dr. V
    - what does she need in order to feel comfortable only editing through the admin page
        - change the way it exports?
        - add more to the admin page table view and the export
        - add data validation? on submit button after edit member
    - date range issue
    - next plans, bio box, notes on admin, link people, prefixes

W Feb 1 / 11:00 - 11:20 / Checkin 2 / Gabby, Julia, Dr. Stiffler

- lots of talking about the spreadsheet and DB issues
- overall plans going forward
    - reorgannize latest spreadsheet into masterlist
    - determine how much is changing per year / best way to organize all the data
    - make a proposition for Dr. V
    - after approval, divide and conquer to populate new DB
- for meeting w/ Dr. V
    - ask what she would need to be able to mostly just use admin page instead of DB
    - show her the data we reorganized, how we think it would best be reorganized
- long term goal
    1. repopulate DB with new schema
    2. add new functionality to admin page search/table view/export
    3. show Dr. V that she can export, add/edit/delete members, then export again the new updated list
    4. *get Dr. V everything she needs to feel comfortable using/relying on the website*
- other...
    - should test to see if build still works properly even with the domain issues

W Feb 1 / 11:20 - 12:30 / excel / Gabby, Julia

- creating masterlist from latest spreadsheet
- highlighted possible issues/conflicting info for the first and last 200 rows

F Feb 3 / 1:30 - 2:15 / Gabby, Julia, Dr. V

- discussed inconsistencies in the speradsheet
- got her thinking about how she would ideally like the member profiles to look/what information they should contain
    - should have full name with title (by year but will only apply to a few known name changes), full addresses by year, DOB, DOD, proposer, pen name by year, leadership position by year
    - all other info will eventually be held in the member profile
- talked about general fixes for the inconsistencies, see email details below (M Feb 6)
- we will send her our highlighted spreadsheet for her to look over again
- she is willing to have the admin page be her sole resource to make changes to the data (no more uploading spreadsheets)
    - we will first fix the DB errors, redesign its schema to add date ranges for several elements
    - will eventually change the format of the admin table view to include all the info, or just make changes to the export methods so they output all data, not only what is displayed in the table
- we will eventually add cookies/sessions so each member has a unique page (also will be needed for the citations feature)

M Feb 6 / 11:10 - 11:45 / Gabby, Julia

- cleaned up highlighted masterlist
- sent email to Dr. V
    - her response: 
        - c/o means "in care of." (If you were having your mail delivered to my office, you would address the envelope: Gabby Snyder, c/o Dr. Vorachek, 269 Humanities, Dayton, OH 45469.) This is valuable information, so please have it show up on the website.
        - For the estimated dates (where it says abt 1869), please keep that. This means that we don't have an exact date, but based on the person's age when she died, we know about when she was born (for example).
        - For lines 146-151, don't correct that. The Adelphi was the name of the building at 5 Robert Street. The Eaton Terrace one should stay as is too.
        - You would like member profiles to display only the surname, firstname, prefix/title, DOB, DOD, leadership position, address, neighborhood, city, post code, proposer (with date ranges where appropriate). PLEASE INCLUDE PEN NAME where applicable. And eventually, space for a biography.
        - When in doubt, assume similar names are different people (Florence Abraham vs F. Abraham) CORRECT
        - DOB, DOD, proposer, joined, shouldn't need date ranges  CORRECT
        - Extra titles (L. L. A) should be omitted, they will be included in the biography eventually CORRECT
    - she will work on the spreadsheet and send it back

W Feb 8 / 11:10 - 11:30 / Checkin 3 / Gabby, Julia, Dr. Stiffler

- talked a lot more about the database and schema
    - thinking of doing an array of arrays of objects: 
        - position array
            - array for each different position
                - object for position
                - object for year
- discussed creating a python script to manage data entry into the database
- talked about ideas for our presentation
    - Who is our client
    - What is our project
    - What are the main goals
    - overview slide of how everything works - languages, framework
    - technical slide of our issues... 
    - contributions - per person, two cols
    - project plan/overview, sprint review and future plans
    - recorded demo of what we are trying to fix going forward
    - show bottom of spreadsheet - actually doomscroll from top to bottom of spreadsheet - this is problematic
    - DB not working as well as we want
    - 10 mins
    - 8-12 slides
    - no trello board

W Feb 8 / 11:30 - 12:00 / Gabby, Julia

- looked further into our database schema idea
- looked into writing a python script

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

# Team Meetings

M Feb 20 / 11:15 - 11:45 / Gabby, Julia

- looked over Julia's python script
- questions: 
    - debating over DB schema still
    - might need to set up staging
    - unsure of how search functionality will be affected by DB schema, need to look at those files
- before wednesday: 
    - Gabby look at build/heroku/push to main issue also look into functionality code, also figure out my vscode
    - Both make a mockup of DB schema
    - Both do checkin documents

W Feb 22 / 11:15 - 12:15 / Gabby, Julia, Dr. Stiffler (just for length of checkin)

- we figured out the CI/CD issue
    - the new repo we created, cps491s23, does not have the variables set up in secrets
    - need to go to repo - settings - secrets - add variables for Heroku API key and Heroku app name
        - what do we do for shared support account on Heroku now that they require MFA??
- going forward: 
    - decide on DB schema
        - look at search functionality
    - set up staging
- Stiffler advice: 
    - write wrapper functions for searchSingleField, searchArray, ...
    - stop overplanning and just try it
    - will probably be repopulating database a million times to get it right

F Feb 24 / 11:00 - 11:45 / Gabby, Julia

- Overall sprint goals: 
    - database filled fully by end of next week, maybe the weekend
    - functionality figured out before spring break
        - Gabby can wrap up loose ends over spring break
- still need to make notes/instructions for next years team making secrets (why our heroku build was broken)
- Sprint 3 goals
    - export function
    - sessions and new pages for each member
    - citations
- By monday we should have: 
    - picked a schema
    - both tested/messed with python script in dummy DB
    - looked over functionality

M Feb 27 / 11:00 - 12:00 / Gabby, Julia

- Looked at Julia's python, Gabby's mongoose trial
- want to have two people fully in dummy DB by Wed
- ask Dr. Stiffler about order of uploading all, breaking functionality
    - staging? just run locally?
- both keep working on python script, maybe look at mongoose
- decided on schema :)
- Friday update contributors page together

W Mar 1 / 11:00 - 12:00 / Gabby, Julia, Dr. Stiffler (for checkin)

- goal: three full entries into db by next wednesday's checkin
- talked about keeping Julia's fullname entry and uniqueid hash
- will need to create staging environment
    - will update completely in staging until end of semester
    - can make the website our own in a way (rewrite some of the old code if we want)
    - will also be connected to new db, not Gabe's
- plan: keep looking into python and do contributor's list on Friday

F Mar 3 / 11:15 - 12:30 / Gabby, Julia

- updated contributors page!!!!! YAY!!!
- still looking at python script
- code that works on Julia's laptop does not work on Gabby's :)))))))
    - no clue why... Gabby will figure it out *hopefully*
- going forward: Gabby keep looking into python script, Gabby has Julia's latest version of convert.py

M Mar 7 / 11:15 - 12:30 / Gabby, Julia

- Gabby spent all weekend trying to get code to work on her laptop
    - needed to add tls workarounds to this:
        - client = MongoClient(connection_string, tls=True, tlsAllowInvalidCertificates=True)
    - Gabby then spent this morning working on script
- talked about/looked over Gabby's improvements
    - still a lot to figure out...
        - Julia has names working as well as the one-time string entries (DOB, DOD...)
        - Gabby needs to figure out positions and addresses (arrays of objects) as well as the arrays (organizations, sources, maybe more?)
- Going forward: 
    - Gabby email Dr. V with update
    - Gabby keep working on script
        - need three full entries by wed
    - Julia do checkin docs

W Mar 8 / 11:00 - 12:00 / Gabby, Julia, Dr. Stiffler (for checkin)

- presentation idea from Stiffler: 
    - in one or two slides
    - shit on them slide
    1. what works
    2. what doesnt work
    3. what our redesign will be now that we have repopulated the DB
    - talk about how we need new staging to develop in parallel
    - can't bring down old website, need to update in parallel
- Going forward: 
    - Gabby finish python script
    - Gabby set up staging
    - Julia go to Italy
- added Gabby's current python file to github and the delete.py file

F Mar 10 / no meeting

M Mar 20 / no meeting

- Gabby working on staging

M Mar 20 / Gabby and Dr. Stiffler / Staging help / 9:45 - 11:15

- got docker image to build locally, but still not working with staging
- Gabby got the website css / html to show on staging but no functionality works
- Heroku shows builds failing but deploys are "successful"
- Will be ok without staging for sprint presentations

T Mar 21 / Gabby and Dr. Stiffler / Staging / 3:15 - 6:00

- more breaking stuff



# Sprint 3

### Sprint Schedule
1. Planning -- Sat Mar 25 - F Mar 31
2. Development -- Sat Apr 1 - F Apr 14
3. Clean-up -- Sat Apr 15 - Sun Apr 23
4. Presentation -- M Apr 24
5. Final Presentation -- M May 1

### Check-in Dates

* W Mar 29
* W Apr 5
* W Apr 12
* W Apr 19

# Team Meetings

R Mar 23 / Gabby and Stiffler / Staging / 3:15 - 5:15

- more breaking stuff

F Mar 24 / Gabby, Julia, Dr. Stiffler / staging / 12:15 - 1:30

- more breaking stuff

M Mar 27 / Gabby and Dr. Stiffler / staging / 8:15 - 10:00

- hard coded one variable for the url
- staging is working for the full members list, but not the search on the main page
    - I (Gabby) realized this after the fact, *might* be able to fix it myself
- Stiffler thinks we should: 
    - explain to Dr. V that the old website is kind of a mess / the code base is overly complicated and hard to work
        - explain it took Dr. Stiffler almost 10 hours with us to get only one piece up and running
    - start to rebuild the website from scratch
        - won't get to admin
        - might work a little over the summer
        - might become a fall project for someone / capston 491 in fall

M Mar 27 / Gabby, Julia / checkin / 11:15 - 11:45

- Gabby explained the above to Julia
- Going forward: 
    - Julia overview for checkin wednesday
    - both look for good bootstrap
    - Gabby make a new Heroku and lets use BitBucket again (hopefully thats fine??)
        - think docker / pipelines / CI/CD will be easier on bitbucket
    - Gabby looking into fixing the staging
    
W Mar 27 / Gabby, Julia, Dr. Stiffler / checkin / 11:15 - 11:45

- try for meeting tomorrow with all of us and Dr. V tomorrow (R) 3:30 or later
- look into Django since it is a multipage site
- use a web framework (Django)
    - write the models
    - built in admin
    - switch to postgres
- for next week: 
    - each of us do chapter 1-3 of Django 4 textbook (blog site) by next wednesday

R Mar 28 / Gabby, Julia, Dr. Stiffler, Dr. Vorachek

- zoom meeting while Dr. V in NYC 
- Dr. Stiffler talked her through our plans
    - she fully approves
- at some point need to talk to her again about all of her hopes/needs for the site

Sun Apr 2 / Gabby, Julia / 1:15 - 3:45

- Django Ch 1

M Apr 3 / Gabby, Julia / 11:15 - 12:15

- Django Ch 2

W Apr 5 / Gabby, Julia, Dr. Stiffler / 11:00 - 12:45

- working through postgres w/ Julia
- Gabby catching up
- Future plans: 
    - email Dr. V and ask for her to meet us in capstone or robotics lab on Tuesday after 3:15 ish
        - need a new, updated list of all of her wants/needs for the site
    - finish through Ch 6 of notes and textbook by then
    - meet Wednesday to plan the site
- final presentation will likely be an overview of all the issues we've had and justification/reasoning for why we have chosen to redo the site with Django, talk about the future of the project w/ Julia and the next team

F Apr 7 / Gabby, Julia 

- going to try to learn Django in 2 weeks
- work through blog application (Ch 1-3)
- get ideas for models.py
- if finished with blog application work through bookmarks (4-6) project

T Apr 11 / Gabby, Julia, Dr. Stiffler, Dr. Vorachek / 3:30 - 5:00

- discussed our redesign with Dr. Vorachek
- Dr. Vorachek agreeded to the much needed redesign and wants an overall sustainable website
- talked about the hopes/needs/wants for the website
- told Dr. Vorachek our upcoming plan for the website and why we will use Django
- going forward: 
    - keep working on Blog and Bookmarks Application

W Apr 12 / Gabby, Julia, Dr. Stiffler / 11:00 - 12:30

- further discussed plan for future website
- created a layout of what to do
- gained more information on how to use Django 
- fixed bugs with our blog application

W Apr 19 / Gabby, Julia, Dr. Stiffler / 10:00 - 12:00

- talked about a bunch of stuff...
- this is what Stiffler does in 242
- explain why this is suitable for swj
- show blog app and say it is an example of a Django app
- show how this could be recreated well/similarly for SWJ
    - what would be the same what would be different
- pres idea
    - show admin page
    - show unique urls
    - show search functionality
    - show pagination
- next semester
    - admin page should not be reachable to the public (by adding /admin)
	    - should limit it (through settings.py: allowed hosts, web address only reachable from certain IP range)
- Presentation
    - SWJ is a read-only website
    - 50/50 on old vs new plans
    - slide with sad face emoji (<-- google that)
        - don't talk badly about any specific team
        - say each team has taken time out of sprints struggling with working on old code
        - this will be easier to maintain
    - transition to slides of the four files (views, forms, models, urls, (admin?)) explaining what they are on a lower level
    - then a slide for our vision for each of those files
        - start with models
        - then views (logic that will use the models)
        - then urls (all of that^ can be mapped with this)
        - then an added layer are the forms that can be used by the views
    - we proposed a complete overhaul of this project with sustainability in mind
        - why we pitched the redesign 
            - not only was this difficult to work with, hard to modify, sent 7 hrs with stiffler trying to edit things that were hard coded
            - **static code was hardcoded - talk about how we couldn't even set up staging
            - trying to do anything further (get the functionality Dr. V wants to actually work) was an unkknown... not sure how bad that could have been
    - we dont need a video
        - instead do a bunch of slides with two pictures - (how search looks/works after being worked on for 3 years -- how it looks after 4 days with Django)
- README
    - mostly future plans
    - our understanding
    - an outline of the project
        - what are the important files in Django?  --> make a subsection for each
            - views: 
                - home page
                - listing members
                - displaying a specific member
            - forms: 
                - search form: date ranges, ...
            - models: 
                - database tables and entries
                - question: what database? postgres - explain why - because powerful for text lookup, can use data validation
                - q: what kind of data are we storing? a member - longer answer - date ranges, ...
            - urls: 
                - regular expressions
                - swj1894/members - list of all members possibly
                - swj1894/members/<reg expression for the user's full name>
            - admin (low priority)
            - search engine optimization (SEO):
                - just one line in README, say we promise to do something for this - can be found in textbook here___
    - three backticks to add a code snippet in markdown (```)
- make models a folder
    - inside have members.py
- succinct notes on old project
- end with "end of life: 2023"
- then "coming soon: SWJ 2.0 using Django framework"

W Apr 26 / Gabby, Julia, Dr. Stiffler / 11:00 - 12:00

- dry run through our presentation with Dr. Stiffler
- possibly share our presentation with Dr. Vorachek to get her insight and approval of project
