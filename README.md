# Django Backend for AbanTether adminpanel
## Apps :
### quizes
- Question
- Quiz
- Story
### games
- GameTable
- GamePlay
- Game Results
- Import GameTable from Excel: read from excel by pandas sheet by sheet column by column and save them in corresponding GameTables
- Import GameTable audios from zip: extract zip in the desired directory and set GameTable files' paths to these
### educational
- Video
- VideoQuestion
- Educational Box
### users
- Signup & login for Users & their parents

## settings.py
- in the logging section a file is specified(`static/errors/errors.log`) that errors in the server are written in this file (for easier debugging)
- you can also config the emails to email you the errors(but error characters exceed gmail's limit)

## CI 
- the file .gitlab-ci.yaml is configured to run django tests on gitlab when a commit is pushed to master branch

## Deploy 
[Django Deployment Document on Ubuntu with Nginx & Gunicorn](./Deploy.md)

## Working with server
[Working with current server](./VPS.md)

## Run
- `make migrate`
- `make admin`
- `make server`
- go to `http://127.0.0.1:8000/admin/`