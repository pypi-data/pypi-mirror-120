import os
import json
import uuid
import glob
import munch
import importlib
from werkzeug.utils import send_from_directory
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.routing import Map, Rule
from mako.lookup import TemplateLookup

apiname = os.environ.get('SOLACE_API_NAME', str(uuid.uuid4()))

# TODO: raise our own custom error types
def objectify(dict):
    return munch.munchify(dict)

class SolaceResponse(Response):
    json = munch.munchify({})
    html = None
    text = None

    def __init__(self, config = {}):
        super().__init__()
        self.config = config
        
        self.imports = []
        # TODO: look into programattic imports for | methods to mako
        
        self.lookup = TemplateLookup(
            directories=[self.config.get("templates_dir", "src/templates")],
            module_directory=self.config.get("modules_dir", "src/modules"),
        )

    def tpl(self, template, context = {}):
        if self.config.get('static') is not None:
            context["static"] = self.config.get('static')
        template = self.lookup.get_template(template)
        self.html = template.render(**context)

class Solace:
    def __init__(self, config = {}):
        self.cors = None
        self.config = objectify(config)
        self.rules = Map([])
        self.views = {}
        self.assets = {}
        self.static_url = self.config.get("static_url", None)

        if self.static_url is not None:
            path = f"{self.static_url}/<path:path>"
            self.get(path, self.__static_files)
        
        # TODO: we could make this configurable.
        self.assets_directory = f"{os.getcwd()}/src/assets"

        self.__auto_register_assets()


    def __auto_register_assets(self):
        """ this method will auto register all static assets in designated directories """
        self.assets["styles"] = {}
        self.assets["scripts"] = {}
        css_directory = f"{self.assets_directory}/css/*.css"
        js_directory = f"{self.assets_directory}/js/*.js"

        for style in glob.glob(css_directory):
            self.assets["styles"][os.path.basename(style)] = f"{self.static_url}{style.removeprefix(self.assets_directory)}"
        
        for script in glob.glob(js_directory):
            self.assets["scripts"][os.path.basename(script)] = f"{self.static_url}{script.removeprefix(self.assets_directory)}"


    def __rule(self, method, urlpath, handler):
        # NOTE: uuids are slow, we could use a randit and make this slightly faster
        uid = str(uuid.uuid4())
        self.rules.add(
            Rule(
                urlpath, 
                endpoint=uid,
                methods=[method]
            )
        )
        self.views[uid] = handler
    
    def __static_files(self, req, res):
        self.static = True
        path = self.req.params.path
        return send_from_directory(self.assets_directory, path, req.environ)

    def get(self, urlpath, handler):
        """
        The GET method requests a representation of the 
        specified resource. Requests using GET should only 
        retrieve data.
        """
        self.__rule('GET', urlpath, handler)

    def head(self, urlpath, handler):
        """
        The HEAD method asks for a response identical to that
        of a GET request, but without the response body.
        """
        self.__rule('HEAD', urlpath, handler)

    def post(self, urlpath, handler):
        """
        The POST method is used to submit an entity to the 
        specified resource, often causing a change in state
        or side effects on the server.
        """
        self.__rule('POST', urlpath, handler)

    def put(self, urlpath, handler):
        """
        The PUT method replaces all current representations 
        of the target resource with the request payload.
        """
        self.__rule('PUT', urlpath, handler)

    def delete(self, urlpath, handler):
        """
        The DELETE method deletes the specified resource.
        """
        self.__rule('DELETE', urlpath, handler)

    def connect(self, urlpath, handler):
        """
        The CONNECT method establishes a tunnel to the server 
        identified by the target resource.
        """
        self.__rule('CONNECT', urlpath, handler)

    def options(self, urlpath, handler):
        """
        The OPTIONS method is used to describe the communication
        options for the target resource.
        """
        self.__rule('OPTIONS', urlpath, handler)

    def trace(self, urlpath, handler):
        """
        The TRACE method performs a message loop-back test along 
        the path to the target resource.
        """
        self.__rule('TRACE', urlpath, handler)

    def patch(self, urlpath, handler):
        """
        The PATCH method is used to apply partial modifications
        to a resource.
        """
        self.__rule('PATCH', urlpath, handler)
    
    def __next_func(self, handler):
        handler(self.req, self.res)

    def __dispatch(self, req):
        adapter = self.rules.bind_to_environ(req.environ)
        self.req = req
        self.req.next = self.__next_func
        self.res = SolaceResponse(self.config)
        try:
            endpoint, values = adapter.match()
            self.req.params = munch.munchify(values)
            if endpoint not in self.views:
                raise NotFound

            # NOTE: this defines the signature for all request handlers...
            r = self.views[endpoint](self.req, self.res)
            if r is not None:
                # NOTE: this is here for the send_from_directory method to work properly
                if str(type(r)) == "<class 'werkzeug.wrappers.response.Response'>":
                    return r
                # NOTE: this is here for the Page resource to work properly.
                if str(type(r)) == "<class 'solace.Page'>":
                    r.render(self.assets)
                    self.res.html = r.html

            # Enables CORS Support
            # TODO: should we add a supported list of keys?
            # or can this be open to adding any desired headers
            # to every response?
            if self.cors is not None:
                for header in self.cors:
                    self.res.headers.set(header, self.cors.get(header))

            if self.res.json:
                self.res.content_type = "application/json"
                self.res.data = json.dumps(self.res.json)
                return self.res

            if self.res.html:
                self.res.content_type = "text/html"
                self.res.data = self.res.html
                return self.res
            
            if self.res.text:
                self.res.content_type = "text/plain"
                self.res.data = self.res.text
                return self.res

            return self.res
        except HTTPException as e:
            # TODO: offer an optional HTML error page to avoid showing JSON errors.
            err = {
                'code': e.code,
                'message': e.description
            }
            res = Response(json.dumps({"error": err}), e.code)
            res.content_type = 'application/json'
            return res

    def __wsgi_app(self, environ, start_response):
        req = Request(environ)
        res = self.__dispatch(req)
        return res(environ, start_response)

    def __call__(self, environ, start_response):
        return self.__wsgi_app(environ, start_response)

class DevelopmentServer:
    
    # TODO: look at more configuration options 
    # that we can support for the DevelopmentServer.
    # https://werkzeug.palletsprojects.com/en/2.0.x/serving/

    def __init__(self, app, host = "127.0.0.1", port = 5000, reload = True):
        self.app = app
        self.host = host
        self.port = port
        self.reload = reload
    
    def start(self):
        run_simple(
            self.host, 
            self.port, 
            self.app, 
            use_debugger=False,
            use_reloader=self.reload
        )

class Page(SolaceResponse):
    
    def __init__(self, template):
        super().__init__()
        self.template = template
        self.title = "Undefined"
        self.styles = []
        self.scripts = []
        self.context = objectify({})

    def set(self, key, value):
        setattr(self, key, value)

    def render(self, assets):
        """ render the final html result of the page """
        final_styles = []
        final_scripts = []
        for style in self.styles:
            css = assets.get('styles').get(style)
            if css is not None:
                final_styles.append(css)
        
        for script in self.scripts:
            js = assets.get('scripts').get(script)
            if js is not None:
                final_scripts.append(js)

        self.ctx = {
            "title": self.title,
            "styles": final_styles,
            "scripts": final_scripts,
        }
        if self.context is not None:
            self.ctx.update(self.context)
        self.tpl(self.template, self.ctx)
