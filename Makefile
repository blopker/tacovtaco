run:
	pipenv run gunicorn app:app --reload

deploy:
	@git push dokku master

generate_photos:
	pipenv run python generate_photos.py
	scp storage/photos.json root@ssh.kbl.io:/var/lib/dokku/data/storage/tacovtaco/
	ssh root@ssh.kbl.io -C "chown -R 32767:32767 /var/lib/dokku/data/storage/tacovtaco"

git:
	@git remote add dokku dokku@ssh.kbl.io:tacovtaco
