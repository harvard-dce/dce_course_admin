A Django LTI app for viewing and updating Canvas LMS courses.

## Setup

1. copy `example.env` to `.env`. The example settings are workable for a dev/test scenario.
1. create a postgres user and database:
    ```
    $ createuser -U postgres -P dce_course_admin
    $ createdb -U postgres -E UTF-8 -T template0 --lc-collate=en_US.UTF-8 --lc-ctype=en_US.UTF-8 --owner dce_course_admin dce_course_admin
    ```    
1. check that the `DATABASE_URL` value in your `.env` matches the user/db you created
1. run `python manage.py migrate`
1. run `python manage.py runserver [host:ip]`
1. check that the app's tool config output is functional by visiting http://\[host:ip]/course_admin/tool_config
1. register the app in your canvas instance 
    1. Go to the canvas Admin -> Settings -> Apps tab and click on `+ App` button
    1. Choose Configuration Type: URL
    1. `Name` can be whatever you want, e.g. "DCE Course Admin"
    1. Consumer Key will be the `LTI_OAUTH_COURSE_ADMIN_CONSUMER_KEY` from your `.env`
    1. Shared Secret will be the `LTI_OAUTH_COURSE_ADMIN_CONSUMER_SECRET` from your `.env`
    1. Config URL will be `http(s)://[host:ip]/course_admin/tool_config`

## Development setup

If you already have easy access to a development instance of Canvas congrats! If you don't
I suggest using the [canvas-docker](https://github.com/harvard-dce/canvas-docker) docker
image.

To start a instance of `canvas-docker` that can communicate with the `dce_course_admin`
app you will need to start the container using the `--network host` option of the `docker run`
command, like so:

    docker run -t -i -p 3000:3000 --network host lbjay/canvas-docker:latest
    
Wait a minute or so for the container's services to spin up and then visit [http://localhost:3000]()

Tip: because the `canvas-docker` container has it's own instance of postgres bound
to port 5432, and because we're using docker's `--network host` option, you will get a
port collision if your local postgres server used by the django app is also on port 5432.
My workaround for this is to start a container instance of postgres on port 5433:

    docker run -d -p 5433:5432 postgres:9.3
