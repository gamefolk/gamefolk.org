"""Initializes frontend assets."""
from pathlib import Path

from flask.ext.assets import Bundle, Environment

js = Bundle(
    'libs/jquery/jquery.js',
    'libs/modernizr/modernizr.js',
    'libs/foundation/js/foundation.js',
)

scss = Bundle('scss/app.scss', filters=['pyscss', 'autoprefixer'])

css = Bundle(scss, filters='autoprefixer', output='public/styles.css')

js_syntax = Bundle(
    'highlightjs/highlight.pack.js'
)

css_syntax = Bundle(
    'highlightjs/default.css'
)


def init_app(app):
    """Set up webassets for the specified application."""
    assets = Environment(app)

    assets.config['PYSCSS_LOAD_PATHS'] = [
        str(Path(app.static_folder) / 'libs')
    ]

    assets.config['AUTOPREFIXER_BIN'] = (
        str(app.config['APP_ROOT'] / 'node_modules' / 'autoprefixer' / 'autoprefixer')
    )

    assets.register('js_all', js)
    assets.register('css_all', css)
    assets.register('js_syntax', js_syntax)
    assets.register('css_syntax', css_syntax)
