#!flask/bin/python
from werkzeug.middleware.profiler import ProfilerMiddleware
from schedulr import app

app.config['PROFILE'] = True
app.wsgi_app = ProfilerMiddleware(app=app.wsgi_app,
                                  restrictions=[100],
                                  sort_by=('ncalls', 'tottime', 'cumtime'))
app.run(debug=True)
