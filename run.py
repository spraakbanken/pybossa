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

from pybossa.core import create_app


class PrefixMiddleware(object):

    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):

        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])
            return ["This url does not belong to the app.".encode()]


if __name__ == "__main__":  # pragma: no cover
    app = create_app()
    #logging.basicConfig(level=logging.NOTSET)
    if len(sys.argv) > 1 and sys.argv[1] == 'run-production':
        from gevent import monkey
        monkey.patch_all()
        from gevent.pywsgi import WSGIServer
        port = app.config['PORT']
        if app.config.get('URL_PREFIX'):
            app.wsgi_app = PrefixMiddleware(app.wsgi_app, app.config['URL_PREFIX'])
        WSGIServer(('0.0.0.0', port), app).serve_forever()
    else:
        # run in debug mode
        app.run(host=app.config['HOST'], port=app.config['PORT'],
            debug=app.config.get('DEBUG', True))
else:
    app = create_app()
