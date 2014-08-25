"""Initializes frontend assets."""
import os

from flask.ext.assets import Bundle, Environment

js = Bundle(
    'jquery/jquery.js',
    'modernizr/modernizr.js',
    'foundation/foundation.js',
)

css = Bundle(
    'css/styles.css',
    'foundation/foundation.css'
)

js_syntax = Bundle(
    'highlightjs/highlight.pack.js'
)

css_syntax = Bundle(
    'highlightjs/default.css'
)


def init_app(app):
    """Set up webassets for the specified application."""
    assets = Environment(app)
    assets.append_path(os.path.join(app.static_folder, 'build'))

    assets.register('js_all', js)
    assets.register('css_all', css)
    assets.register('js_syntax', js_syntax)
    assets.register('css_syntax', css_syntax)
