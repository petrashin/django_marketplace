run:
	python manage.py runserver

migrate:
	python manage.py makemigrations
	python manage.py migrate

fixtures:
	python manage.py loaddata default
	python manage.py loaddata goods
	python manage.py loaddata shops
	python manage.py loaddata tags

admin:
	python manage.py createsuperuser

start:
	make migrate
	make fixtures
	make admin
	make run