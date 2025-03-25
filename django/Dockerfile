from python:3
workdir /django/
copy requirements .
run pip install --upgrade pip && pip install -r requirements
copy . .
entrypoint \
	cd project && \
	python3 manage.py makemigrations && \
	python3 manage.py migrate && \
	celery multi start w1 -A tasks -B --loglevel=INFO \
		--pidfile="/django/celery/%n.pid" \
		--logfile="/django/celery/%n%I.log" && \
	/usr/local/bin/gunicorn \
		--access-logfile '-' \
		--bind ivanefremovbot-django:8000 \
		project.wsgi:application
