# semantive

Install docker on Your local machine.

Start project by running the command:
'docker-compose up'

On next terminal screen enter to the shell the command, where work dir is root of this project:
'docker exec -it semantive_app_1 /bin/sh'

Run tests there by command:
'python manage.py test'

PEP8 is OK (custom file configuration '.flake8')

Future features:
 - logger
 - remove empty lines on website process
 - better image finder on website process
 - image thumbnail on website process
 - celery configure (e.g with mode celery turn off to not lose any data/task) 
 - set max retrieve etc for requests
 - use postgres data instead of sqlite3 or consider no sql db (mongodb) / one document - where key is URL (depend on future feature)
 - create development and production env

Solution:
Presented solution is a first step of the whole scope.
It's far away from production environment..
Celery is helping with async tasks, but it's not configured in right way, because it's not a production solution, but only draft (more less) of the way how I'm developing.
