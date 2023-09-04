install:
	pip install -r requirements.txt

server:
	python manage.py runserver

test:
	python tests.py

migrate:
	python manage.py makemigrations && python manage.py migrate && python manage.py migrate --run-syncdb

admin:
	python manage.py createsuperuser