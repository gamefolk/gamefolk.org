from flask.ext.assets import Bundle, Environment

js = Bundle(
    'foundation/js/vendor/jquery.js',
    'foundation/js/vendor/modernizr.js',
    'foundation/js/foundation.min.js',
)

css = Bundle(
    'foundation/css/normalize.css',
    'foundation/css/foundation.css'
)

js_syntax = Bundle(
    'highlightjs/highlight.pack.js'
)

css_syntax = Bundle(
    'highlightjs/styles/default.css'
)

assets = Environment()

assets.register('js_all', js)
assets.register('css_all', css)
assets.register('js_syntax', js_syntax)
assets.register('css_syntax', css_syntax)
