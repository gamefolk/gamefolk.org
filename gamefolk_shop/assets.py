from flask.ext.assets import Bundle, Environment

js = Bundle(
    'foundation/js/foundation.js'
)

css = Bundle(
    'foundation/css/foundation.css'
)

assets = Environment()

assets.register('js_all', js)
assets.register('css_all', css)
