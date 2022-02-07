#Baseline_
Web App Directory 
_____________________________________________
Installation
Use the package manage [pip](https://pip.pypa.io/en/stable/) to install requirements.txt file 
to install all required packages.
```bash
pip install -r requirements.txt
```
______________________________________________
Baseline_
    Backend Directory
•	__init__.py
•	asgi.py - (used for server setting)
•	setting.py - (used for the full app settings, security, middleware, static directories, etc..)
•	url.py - (used for routing back-end urls) - only has admin panrl and front-end urls
•	wsgi.py - (used for more server settings)
_______________________________________________
dashboard
    Front-End Directory
•	__init__.py
•	admin.py - (set admin settings for django admin panel)- not in use
•	apps.py - (unsure of use) - not in use
•	migration - (changes made in the database) -not in use
•	models.py - (used for creating database tables and pushes them into the migration directory)
•	static - (directory used for holding Images, CSS files, Javascript files and CSV files)
•	templates - (used for holding all html files)
•	test.py - (used for writing test for the front-end)
•	urls.py - (used for routing all urls in the front end)
•	views.py - (used for writing the data that post to the html files) 
________________________________________________
.gitignore - used for ignore files in git.
________________________________________________
manage.py - used to run django app
Use command below to run server on local host to view site in action.
```bash
python manage.py runserver
```
_________________________________________________
db.sqlite - preinstalled once you run the django server
    This is where we need to point the pipline file to save our data.
_________________________________________________
