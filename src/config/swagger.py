template = {
    "swagger": "2.0",
    "info": {
        "title": "Chatboot Liqahona API",
        "description": "This is a QNA boot API that provides informations about Covid 19 vaccin in Morocco",
        "contact": {
            "responsibleOrganization": "linkedin.com/in/hassan-abida/",
            "responsibleDeveloper": "linkedin.com/in/hassan-abida/",
            "email": "abidahass.uca@gmail.com",
            "url": "linkedin.com/in/hassan-abida/",
        },
        "termsOfService": "linkedin.com/in/hassan-abida/",
        "version": "1.0"
    },
    "basePath": "/api/v1",  # base bash for blueprint registration
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
}