Start project

git clone

virtualenv - python -m venv venv

pip install -r requirements.txt - install requirements

createdb test_db - create PostgreSQL database  or use sqlite3

python manage.py migrate - migrate database

python manage.py createsuperuser

python manage.py runserver - run development server
