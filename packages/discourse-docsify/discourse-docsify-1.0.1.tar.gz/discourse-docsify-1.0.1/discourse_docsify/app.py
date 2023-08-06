import warnings

from flask import send_file, Blueprint, redirect, render_template_string
from requests.exceptions import HTTPError
from werkzeug import Response

from discourse_docsify.cache import MemoryCache, RedisCache
from discourse_docsify.discourse_api import DiscourseAPI
from discourse_docsify.parser import DiscourseParser

try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

from . import static


class Docs:
    def __init__(self, app=None, config=None, pre_content=None):
        if not (config is None or isinstance(config, dict)):
            raise ValueError("`config` must be an instance of dict or None")

        self.config = config

        self.cache = None
        self.parser = None
        self.template = None

        if app is not None:
            self.init_app(app, config, pre_content)

    def init_app(self, app, config=None, pre_content=None):
        if not (config is None or isinstance(config, dict)):
            raise ValueError("`config` must be an instance of dict or None")

        base_config = app.config.copy()
        if self.config:
            base_config.update(self.config)
        if config:
            base_config.update(config)
        config = base_config

        config.setdefault("DOCS_URL_PREFIX", "/docs")
        config.setdefault("DOCS_HOMEPAGE_TITLE", "Documentation")
        config.setdefault("DOCS_INDEX_PATH", None)
        config.setdefault("DOCS_TEMPLATE_PATH", None)
        config.setdefault("DOCS_HUMANIZE_LOCALE", None)
        config.setdefault("DOCS_CACHE_TIMEOUT", 3600 * 10)
        config.setdefault("DOCS_CACHE_TYPE", "memory")
        config.setdefault("DOCS_CACHE_REDIS_CONN", {})
        config.setdefault("DOCS_CACHE_REDIS_PREFIX", 'discourse_docsify_docs_')
        config.setdefault("DOCS_DISCOURSE_API_USERNAME", None)
        config.setdefault("DOCS_DISCOURSE_API_KEY", None)
        config.setdefault("DOCS_DISCOURSE_BASE_URL", None)
        config.setdefault("DOCS_DISCOURSE_INDEX_TOPIC_ID", None)

        self.config = config

        if config["DOCS_CACHE_TYPE"] not in ['memory', 'redis']:
            warnings.warn(f"Invalid DOCS_CACHE_TYPE value: '{config['DOCS_CACHE_TYPE']}'. Changing to 'memory'.")
            config["DOCS_CACHE_TYPE"] = 'memory'

        if config["DOCS_CACHE_TYPE"] == "memory":
            self.cache = MemoryCache(config["DOCS_CACHE_TIMEOUT"])
        else:
            self.cache = RedisCache(config["DOCS_CACHE_TIMEOUT"],
                                    config["DOCS_CACHE_REDIS_PREFIX"],
                                    **config["DOCS_CACHE_REDIS_CONN"])

        self.parser = DiscourseParser(
            api=DiscourseAPI(
                base_url=config["DOCS_DISCOURSE_BASE_URL"],
                api_username=config["DOCS_DISCOURSE_API_USERNAME"],
                api_key=config["DOCS_DISCOURSE_API_KEY"],
                index_topic_id=config["DOCS_DISCOURSE_INDEX_TOPIC_ID"]
            ),
            locale=config["DOCS_HUMANIZE_LOCALE"]
        )

        if config["DOCS_TEMPLATE_PATH"]:
            with open(config["DOCS_TEMPLATE_PATH"], 'r') as f:
                self.template = f.read()
        else:
            self.template = pkg_resources.read_text(static, 'template.md')

        blueprint = Blueprint('discourse_docsify_docs', __name__)

        @blueprint.route('/', defaults={'path': 'index.html'})
        @blueprint.route('/<string:path>')
        @blueprint.route('/<path:path>')
        def serve_docs(path):
            if pre_content:
                pre_result = pre_content(path)
                if isinstance(pre_result, Response):
                    return pre_result
            if path.endswith(".md"):
                return self.render_content(path[:-3])
            elif path == 'index.html':
                if config["DOCS_INDEX_PATH"]:
                    return send_file(config["DOCS_INDEX_PATH"])
                else:
                    return pkg_resources.read_text(static, 'index.html')
            return 404

        app.register_blueprint(blueprint, url_prefix=config["DOCS_URL_PREFIX"])

    def fetch_content(self, path=""):
        if self.cache.exists(path):
            return self.cache.get(path)

        self.parser.parse()
        if path == '_sidebar':
            content = self.sidebar()
        else:
            content = self.document_view('' if path == 'README' else path)

        self.cache.set(path, content)
        return str(content)

    def render_content(self, path=""):
        content = self.fetch_content(path)
        if not content:
            redirect('/')
        return content

    def document_view(self, path=""):
        """
        A Flask view function to serve
        topics pulled from Discourse as documentation pages.
        """
        path = "/" + path

        if path == "/":
            document = self.parser.parse_content(self.parser.index_topic, self.parser.get_section_content("Homepage"),
                                                 self.config["DOCS_HOMEPAGE_TITLE"])
        else:
            topic_url = self.parser.url_map.get(path)
            if not topic_url:
                return 404

            topic_id = self.parser.get_topic_id(topic_url)

            if topic_id == self.config["DOCS_DISCOURSE_INDEX_TOPIC_ID"]:
                return

            try:
                topic = self.parser.api.get_topic(topic_id)
            except HTTPError as http_error:
                return http_error.response.status_code

            document = self.parser.parse_topic(topic)

        return render_template_string(self.template, **document)

    def sidebar(self):
        nav_links = []
        for nav_link in self.parser.navigation_list:
            indent = '    ' * (int(nav_link['level']) - 1)
            nav_content = f"\n{indent}* "
            if nav_link['path']:
                nav_content += f"[{nav_link['navlink']}](/{nav_link['path']})"
            else:
                nav_content += nav_link['navlink']
            nav_links.append(nav_content)
        return '\n'.join(nav_links)
