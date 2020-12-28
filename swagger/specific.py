from flask_swagger_ui import get_swaggerui_blueprint

def setup_swagger_specific(app):
    """
    init swagger specific
    """

    SWAGGER_URL = '/swagger'
    API_URL = '/static/weather.json'
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Weather Cast API"
        }
    )
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)