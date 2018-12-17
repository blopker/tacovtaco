run:
	pipenv run gunicorn app:app --reload

deploy:
	@git push dokku master

git:
	@git remote add dokku dokku@ssh.kbl.io:tacovtaco
