# rowbot.io
A rowing schedule manager

Briefly, the goal is to quickly manage the problem of finding a replacement for a position if someone drops out. An exact number of people are needed to fill the available roles, and events often take place very early in the morning (between 5am and 7am). Because of this, the roster needs to be solid the night before or even earlier. This inevitably leads to a flurry of panic the night before an event to lock everything down.

This application smoothes that process by keeping a roster of people with their confirmation, and a list of reserves for an event. If someone drops out, it is on them to notify the reserves and fill their place. The number of times a person drops can be recorded, and they can be disciplined. If someone offers themselves as a reserve, their slate can be wiped clean.

This model applies very well to a number of sports, but I wanted to start with rowing, as that is what I experienced personally as the Men's Captain of the St. Edmund's College Boat Club.

## Install

Requires python3.6 and an internet connection.

1. Go to directory
2. Virtualenv: ~$ python3.6 -m venv .
3. Activate the virtualenv with ~$ source ./bin/activate
4. Requirements: ~$ pip install -r reqs/development.txt
5. Create settings config: ~$ open django_backend/settings/conf.json
`{"path": "settings.development.np"} # path within django_backend/`
If you want to override settings, you can create a new file and enter the path here. This file will not be tracked.
6. Database: ~$ python manage.py migrate
7. Start a second shell, go to redis_scheduler/
8. Start redis server: ~$ ./start.sh
9. Start a third shell, go to node_ws_gateway and install node if necessary: https://nodejs.org/en/download/
10. Start websocket server: ~$ node server.js
11. Start the django development server: ~$ python manage.py runserver
12. In a browser, go to localhost:8000.
13. Check plan/phases.txt

## Processes

1. Django web backend
2. Node.js websocket gateway
3. Redis event queue

## The Django backend

The Django process contains the ORM and data model, responds to HTTP requests, runs the scheduler in the background and interfaces with the websocket server.

For the backend, an explanation of the structure can be found in the rowbot/models/__init__.py script.

For the frontend, the most important parts are:

1. rowbot/static
2. rowbot/templates
3. urls.py
4. rowbot/api/routes.py
5. assets/js/api.js

The static directory stores the static files for interfaces in the app. The templates directory stores the templates that consume the static files.

urls.py shows the routes to the api and main app.html template. The routes.py script contains the routes for all api objects. This is the set of routes loaded by the schema url.

In the browser, making a request to the schema url will yield the full list of all objects and specific methods used to manipulate them. This can be called directly, even with a tool like cURL. The assets/js/api.js can also fully manipulate the databaseo objects.

## The Node websocket gateway

The websocket gateway maintains named websocket connections that have been fed to it by the django backend. Websockets are associated with active user accounts and can be used to send messages to a specific set of users. When an event is triggered, a request will be sent to the node http server (can also use a simple unix socket). This will trigger a message to be sent out on all active websockets whose names match the list sent by the Django server, corresponding to the subscribers of that event.
