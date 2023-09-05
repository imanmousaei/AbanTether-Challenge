# Django Backend for AbanTether adminpanel

## Run on Local

- `make migrate`
- `make admin`
- (optional) run `make test` to run testcases
- `make server`
- go to `http://127.0.0.1:8000/admin/` and use it


## Backup Database
```bash
su - postgres
pg_dump -U postgres AbanTetherdb > dbexport_1402_06_14.pgsql
```
in this way dbexports are saved at : `/var/lib/postgresql`

## Deploy 
[Django Deployment Document on Ubuntu with Nginx & Gunicorn](./Deploy.md)

## CI 
The file `.gitlab-ci.yml` is configured to run django tests on gitlab when a commit is pushed to master branch
