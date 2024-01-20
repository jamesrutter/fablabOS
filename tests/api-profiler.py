#!flask/bin/python
from werkzeug.middleware.profiler import ProfilerMiddleware
from api import app

app.config['PROFILE'] = True
app.wsgi_app = ProfilerMiddleware(app=app.wsgi_app,
                                  restrictions=[50])
app.run(debug=True)
