import os, re, subprocess, yaml, argparse, time, mimetypes
from werkzeug.wrappers import Request, Response
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.middleware.http_proxy import ProxyMiddleware
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from werkzeug.wsgi import get_path_info, wrap_file
from werkzeug.utils import get_content_type
from werkzeug.http import http_date, is_resource_modified

__version__ = "0.6.1"

applicationFolder = ""

def loadYamlFile(path):
	'''load yaml file from given path'''
	try:
		cronYaml = open(path, "r")
		cronYamlObj = yaml.load(cronYaml, Loader=yaml.Loader)
		return cronYamlObj
	except Exception as e:
		print(e)
		return None

def buildStaticRoutes():
	'''build static routes from yaml handlers'''
	path = os.path.join(applicationFolder,"app.yaml")
	appdata = loadYamlFile(path)

	if not appdata:
		return None

	static_routes = {}
	for route in appdata["handlers"]:
		if "static_dir" in route:
			static_routes.update({route["url"]: {"path":route["static_dir"],"type":"dir"}})

		if "static_files" in route:
			static_routes.update({route["url"]: {"path":route["static_files"],"type":"file"}})

	return static_routes

class WrappingApp(object):
	'''simple wrapping app'''
	def __init__(self, config):
		pass

	def wsgi_app(self, environ, start_response):
		request = Request(environ)
		response = Response(f'Path not found or invalid: {request.path}', status=404)
		return response(environ, start_response)

	def __call__(self, environ, start_response):
		return self.wsgi_app(environ, start_response)

class myProxy(ProxyMiddleware):
	"""this addition allows to redirect all routes to given targets"""

	def __init__(self, app, targets,chunk_size=2 << 13,timeout=10):

		super().__init__(app,targets,chunk_size,timeout)

		def _set_defaults(opts):
			opts.setdefault("remove_prefix", False)
			opts.setdefault("host", "<auto>")
			opts.setdefault("headers", {})
			opts.setdefault("ssl_context", None)
			return opts

		self.targets = {
			f"{k}": _set_defaults(v) for k, v in targets.items()
		}

class myDispatcher(DispatcherMiddleware):
	'''use regex to find a matching route'''
	def __call__(self, environ, start_response):
		app = self.mounts["/"]

		for route, _app in self.mounts.items():
			if re.match(route,environ["PATH_INFO"]):
				app = _app
				break

		return app(environ, start_response)


class mySharedData(SharedDataMiddleware):
	'''use regex to find a matching files'''

	def __init__(
			self,
			app,
			exports,
			disallow: None = None,
			cache: bool = True,
			cache_timeout: int = 60 * 60 * 12,
			fallback_mimetype: str = "application/octet-stream",
	) -> None:
		self.org_exports = exports.copy()
		super().__init__(app, exports, disallow, cache, cache_timeout, fallback_mimetype)


	def __call__(self, environ, start_response):
		path = get_path_info(environ)
		file_loader = None

		for search_path, loader in self.exports:
			#lets check for regex, and inject real_path
			if re.match(search_path, path):
				real_path = re.sub(search_path, self.org_exports[search_path], path, 1)
				real_filename, file_loader = self.get_file_loader(real_path)(None)

				if file_loader is not None:
					break

			if search_path == path:
				real_filename, file_loader = loader(None)

				if file_loader is not None:
					break

			if not search_path.endswith("/"):
				search_path += "/"

			if path.startswith(search_path):
				real_filename, file_loader = loader(path[len(search_path):])

				if file_loader is not None:
					break

		if file_loader is None or not self.is_allowed(real_filename):  # type: ignore
			return self.app(environ, start_response)

		guessed_type = mimetypes.guess_type(real_filename)  # type: ignore
		mime_type = get_content_type(guessed_type[0] or self.fallback_mimetype, "utf-8")
		f, mtime, file_size = file_loader()

		headers = [("Date", http_date())]

		if self.cache:
			timeout = self.cache_timeout
			etag = self.generate_etag(mtime, file_size, real_filename)  # type: ignore
			headers += [
				("Etag", f'"{etag}"'),
				("Cache-Control", f"max-age={timeout}, public"),
			]

			if not is_resource_modified(environ, etag, last_modified=mtime):
				f.close()
				start_response("304 Not Modified", headers)
				return []

			headers.append(("Expires", http_date(time.time() + timeout)))
		else:
			headers.append(("Cache-Control", "public"))

		headers.extend(
			(
				("Content-Type", mime_type),
				("Content-Length", str(file_size)),
				("Last-Modified", http_date(mtime)),
			)
		)
		start_response("200 OK", headers)
		return wrap_file(environ, f)

def create_app(host, port, app_port, protocol="http", with_static=True):
	'''use the disapatcherMiddleware to connect SharedDataMiddleware and ProxyMiddleware with the wrapping app.'''
	app = WrappingApp({})
	apps = {}

	if with_static:
		staticRoutes = buildStaticRoutes()

		for route,config in staticRoutes.items():
			static_app = mySharedData(app.wsgi_app,
			{
				route:  os.path.join(applicationFolder, config["path"])
			})
			if config["type"] =="dir":
				apps.update({route+"/.*":static_app})
			else:
				apps.update({route: static_app})

	script_app = myProxy(app.wsgi_app, {
		"/": {
			"target": f"{protocol}://{host}:{app_port}/",
			"host": f"{host}:{port}"
		}
	})

	apps.update({"/": script_app})
	app.wsgi_app = myDispatcher(app.wsgi_app,apps)

	return app


def start_server(host, port, app_port):
	'''create app and start server'''
	app = create_app(host,port, app_port)
	time.sleep(5)
	run_simple(host, port, app, use_debugger=True, use_reloader=True, threaded=True)

def envVars(application_id):
	'''set nessesary environment variables'''
	os.environ["GAE_ENV"] = "localdev"
	os.environ["CLOUDSDK_CORE_PROJECT"] = application_id
	os.environ["GOOGLE_CLOUD_PROJECT"] = application_id
	os.environ["GAE_VERSION"] = str(time.time())

def main():
	'''main entrypoint

	collect parameters
	set environment variables
	start gunicorn
	start wrapping app
	'''
	global applicationFolder
	ap = argparse.ArgumentParser(
		description="alternative dev_appserver"
	)

	ap.add_argument("config_paths", metavar='yaml_path', nargs='+', help='Path to app.yaml file')
	ap.add_argument(
		'-A', '--application', action='store', dest='app_id', required=True,
		help='Set the application, overriding the application value from the app.yaml file.')
	ap.add_argument('--host', default="localhost", help='host name to which application modules should bind')
	ap.add_argument('--port', type=int, default=8081, help='port to which we bind the application')
	ap.add_argument('--app_port', type=int, default=8090, help='internal gunicorn port')
	ap.add_argument('--worker', type=int, default=1, help='amount of gunicorn workers')
	ap.add_argument('--threads', type=int, default=5, help='amount of gunicorn threads')
	ap.add_argument('-V', '--version', action='version', version='%(prog)s ' + __version__)

	args = ap.parse_args()
	print(args)
	envVars(args.app_id)

	applicationFolder = os.path.abspath(args.config_paths[0])
	currentFolder = os.getcwd()

	try:
		os.chdir(applicationFolder)
		gunicornCMD = f"gunicorn -b :{args.app_port} -w {args.worker} --threads {args.threads} --reload --disable-redirect-access-to-syslog main:app"
		p = subprocess.Popen(gunicornCMD.split())
		os.chdir(currentFolder)
		start_server(args.host,args.port, args.app_port)
	except Exception as e:
		print(e)


if __name__ == '__main__':
	main()




