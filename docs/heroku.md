# Heroku Deployment

### From scratch

1. Create a new Heroku app. For the purposes of these instructions we'll call it "dce-course-admin", but it could really be anything.
2. Install the [heroku-toolbelt](https://toolbelt.heroku.com/).
3. Clone the [dce_course_admin](https://github.com/harvard-dce/dce_course_admin repo).
4. Run `heroku git:remote -a dce-course-admin`
5. Add the required heroku add-ons: 
    * [Heroku Postgres](https://addons.heroku.com/heroku-postgresql) 
    * [Mandrill](https://addons.heroku.com/mandrill)
6. Set up the remaining environment vars via `heroku config:set ...` (see below)
7. Run `git push heroku master`. Heroku will detect and build the app.
8. Run `heroku run python manage.py syncdb` to initialize the database. 
    * Say, 'no', when prompted to create an admin user.
9. Install the LTI app in the Canvas account settings UI. 
    * Configuration Type: 'By URL'
    * Name: 'DCE Course Admin'
    * Consumer Key: value of the **LTI_OAUTH_COURSE_ADMIN_CONSUMER_KEY** env var
    * Consumer Secret: value of the **LTI_OAUTH_COURSE_ADMIN_CONSUMER_SECRET** env var
    * Config URL: https://dce-course-admin.herokuapp.com/course_admin/tool_config

### Required env vars

```
LTI_OAUTH_COURSE_ADMIN_CONSUMER_KEY=...
LTI_OAUTH_COURSE_ADMIN_CONSUMER_SECRET=...
CANVAS_DEVELOPER_KEY_CLIENT_ID=...
CANVAS_DEVELOPER_KEY_CLIENT_SECRET=...
DJANGO_SECRET_KEY=...
DJANGO_ADMIN_NAME=...
DJANGO_ADMIN_EMAIL=...
DJANGO_SERVER_EMAIL
PYTHONPATH=fakepath
DJANGO_DATABASE_DEFAULT_ENGINE=django_postgrespool
CURRENT_TERM_ID=2014-2
```

* **LTI_OAUTH_COURSE_ADMIN_CONSUMER_KEY** and **LTI_OAUTH_COURSE_ADMIN_CONSUMER_SECRET** are credentials needed during the Canvas LTI app installation. The key should be some simple, identifying string, like "dce-course-admin". For the secret you can probably just use a generated password or a [uuid4](http://en.wikipedia.org/wiki/Universally_unique_identifier#Version_4_.28random.29), but if you want to get fancy there's a [secret key generator](http://techblog.leosoto.com/django-secretkey-generation/) that I sometimes use.
* **CANVAS_DEVELOPER_KEY_CLIENT_ID** and **CANVAS_DEVELOPER_KEY_CLIENT_SECRET** are necessary for the oauth workflow the app uses to generate user-specific canvas api keys. See: https://canvas.instructure.com/doc/api/file.oauth.html. Note that the domain of the app (eg, *https://dce-course-admin.herokuapp.com*) must match the value of the *REDIRECT_URI* used when generating this id/secret pair.
* **DJANGO_SECRET_KEY**: see comments above about the *LTI_OAUTH_COURSE_ADMIN_CONSUMER_SECRET*.
* **PYTHONPATH**: This is a common kludge to deal with [gunicorn weirdness on heroku](https://github.com/heroku/heroku-buildpack-python/wiki/Troubleshooting#no-module-named-appwsgiapp).
* **DJANGO_ADMIN_NAME** and **DJANGO_ADMIN_EMAIL**: Set these to the name/email of the person or entity that will recieve app error notifications.
* **DJANGO_SERVER_EMAIL**: app error notifications will use this as the "From:" address.
* **CURRENT_TERM_ID**: this specifies which enrollment term should be the default view.

### Additional env vars

```
DATABASE_URL=...
MANDRILL_APIKEY=...
MANDRILL_USERNAME=...
```

These are all provided by add-ons; do not set them manually.


