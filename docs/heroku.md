# Heroku Deployment

### From scratch

1. Create a new Heroku app. For the purposes of these instructions we'll call it "dce-course-admin", but it could really be anything.
2. Install the [heroku-toolbelt](https://toolbelt.heroku.com/).
3. Clone the [dce_course_admin](https://github.com/harvard-dce/dce_course_admin repo).
4. Run `heroku git:remote -a dce-course-admin`
5. Add the required heroku add-ons: 
    * [Heroku Postgres](https://addons.heroku.com/heroku-postgresql) 
    * [RedisToGo](https://elements.heroku.com/addons/redistogo)
6. Set up the remaining environment vars via `heroku config:set ...` (see below)
7. Create a loggly logging drain:
    * `heroku drains:add https://logs-01.loggly.com/bulk/<loggly token>/tag/heroku,dce-course-admin`
7. Run `git push heroku master`. Heroku will detect and build the app.
8. Run `heroku run python manage.py migrate` to initialize the database. 
    * Say, 'yes', when prompted to create an admin user. This is necessary for setting up the canvas developer key.
9. Visit `https://<app_url>/admin`, login using the super user created in the previous step, and enter your Canvas developer key.
    * Note: the redirect URI used to initially create the developer key via the Canvas admin must match `https://<app_url>`.
9. Install the LTI app in the Canvas account settings UI. 
    * Configuration Type: 'By URL'
    * Name: 'DCE Course Admin'
    * Consumer Key: value of the **LTI_OAUTH_COURSE_ADMIN_CONSUMER_KEY** env var
    * Consumer Secret: value of the **LTI_OAUTH_COURSE_ADMIN_CONSUMER_SECRET** env var
    * Config URL: `https://<app_url>/course_admin/tool_config`

### Required env vars

    LTI_OAUTH_COURSE_ADMIN_CONSUMER_KEY=...
    LTI_OAUTH_COURSE_ADMIN_CONSUMER_SECRET=...
    DJANGO_SECRET_KEY=...
    PYTHONPATH=fakepath
    DJANGO_DATABASE_DEFAULT_ENGINE=django_postgrespool
    CURRENT_TERM_ID=2014-2
    REDIS_URL=...

* **LTI_OAUTH_COURSE_ADMIN_CONSUMER_KEY** and **LTI_OAUTH_COURSE_ADMIN_CONSUMER_SECRET** are credentials needed during the Canvas LTI app installation. The key should be some simple, identifying string, like "dce-course-admin". For the secret you can probably just use a generated password or a [uuid4](http://en.wikipedia.org/wiki/Universally_unique_identifier#Version_4_.28random.29), but if you want to get fancy there's a [secret key generator](http://techblog.leosoto.com/django-secretkey-generation/) that I sometimes use.
* **DJANGO_SECRET_KEY**: see comments above about the *LTI_OAUTH_COURSE_ADMIN_CONSUMER_SECRET*.
* **PYTHONPATH**: This is a common kludge to deal with [gunicorn weirdness on heroku](https://github.com/heroku/heroku-buildpack-python/wiki/Troubleshooting#no-module-named-appwsgiapp).
* **CURRENT_TERM_ID**: this specifies which enrollment term should be the default view (currently listed in `settings.py`.
* **REDIS_URL**: copy this from the **REDISTOGO_URL** that was inserted into your heroku config when the redis add-on was added.

### Additional env vars

    DATABASE_URL=...

These are all provided by add-ons; do not set them manually.


