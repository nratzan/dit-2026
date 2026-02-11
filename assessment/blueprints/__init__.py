def register_all_blueprints(app):
    from blueprints.assessment import bp as assessment_bp
    from blueprints.chat import bp as chat_bp
    from blueprints.api import bp as api_bp
    app.register_blueprint(assessment_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(api_bp)
