# Structure Section
full_db/execute.py -> fill de db with random data
library -> app of system
system -> name of this project
db.sqlite3 -> the db use on this project
.gitignore -> have the name of the private files
requirements.txt -> contain the package are required for this project
# Structure Section

# Script Section
Recommend execute:

python -m venv .env || python3 -m venv .env || py -m venv .env
.env\Scripts\activate.bat || source tutorial-env/bin/activate || source .env/Scripts/Activate
[Link](https://docs.python.org/3/library/venv.html)
[//]: <> (||)
[Link](https://www.anaconda.com/products/distribution)

pip i -r requirements.txt
[//]: <> (You can update pip too)

python manage.py makemigrations || py manage.py makemigrations
python manage.py migrate || py manage.py migrate
python manage.py createsuperuser || py manage.py createsuperuser
[enter the username]
[enter the email]
[enter the password]
[enter the password again]
full_db/execute.py
python manage.py runserver || py manage.py migrate

deactivate
clear || cls
# Script Section
# Comments about other comments
[//]: <> (Additionaly I've the extension better comments)
[//]: <> (* is for a highlight comment, for not discard the comment as just only one more)
[//]: <> (! is for a red comment, I think this comment as something is not ok)
[//]: <> (? a blue comment, I see it as a info about something)
#