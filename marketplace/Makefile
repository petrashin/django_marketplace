run:
	py manage.py runserver

migrate:
	py manage.py makemigrations
	py manage.py migrate

fixtures:
	py manage.py loaddata goods
	py manage.py loaddata shops
	python manage.py loaddata tags

admin:
	py manage.py createsuperuser

start:
	make migrate
	make fixtures
	make admin
	make run
