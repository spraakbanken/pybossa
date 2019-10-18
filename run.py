# -*- coding: utf8 -*-
# This file is part of PYBOSSA.
#
# Copyright (C) 2015 Scifabric LTD.
#
# PYBOSSA is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PYBOSSA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PYBOSSA. If not, see <http://www.gnu.org/licenses/>.
import sys
import datetime

sys.stderr.write('{} >>> Pybossa Started\n'.format(datetime.datetime.now()))

from pybossa.core import create_app


class ReverseProxied(object):

    def __init__(self, app, script_name=None, scheme=None, server=None):
        self.app = app
        self.script_name = script_name
        self.scheme = scheme
        self.server = server

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '') or self.script_name
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]
        scheme = environ.get('HTTP_X_SCHEME', '') or self.scheme
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        server = environ.get('HTTP_X_FORWARDED_SERVER', '') or self.server
        if server:
            environ['HTTP_HOST'] = server
        return self.app(environ, start_response)


if __name__ == "__main__":  # pragma: no cover
    app = create_app()
    #logging.basicConfig(level=logging.NOTSET)
    if len(sys.argv) > 1 and sys.argv[1] == 'run-production':
        from gevent import monkey
        monkey.patch_all()
        from gevent.pywsgi import WSGIServer

        print("app.config['APPLICATION_ROOT'] = {}".format(app.config.get('APPLICATION_ROOT')))

        port = app.config['PORT']
        if app.config.get('APPLICATION_ROOT'):
            app.wsgi_app = ReverseProxied(app.wsgi_app, script_name=app.config['APPLICATION_ROOT'])
        WSGIServer(('0.0.0.0', port), app).serve_forever()
    else:
        # run in debug mode
        app.run(host=app.config['HOST'], port=app.config['PORT'],
            debug=app.config.get('DEBUG', True))
else:
    app = create_app()
