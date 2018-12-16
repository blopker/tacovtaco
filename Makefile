run:
	gunicorn app:app

deploy:
	@git push dokku master

git:
	@git remote add dokku dokku@ssh.kbl.io:tacovtaco
