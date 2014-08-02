from flask.ext.assets import Bundle, Environment

js = Bundle(
    'foundation/js/vendor/jquery.js',
    'foundation/js/vendor/modernizr.js',
    'foundation/js/foundation.min.js'
)

css = Bundle(
    'foundation/css/normalize.css',
    'foundation/css/foundation.css'
)

assets = Environment()

assets.register('js_all', js)
assets.register('css_all', css)
