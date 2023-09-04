install:
	pip install -r requirements.txt

server:
	python manage.py runserver

test:
	python manage.py test

migrate:
	python manage.py makemigrations && python manage.py migrate

admin:
	python manage.py createsuperuser