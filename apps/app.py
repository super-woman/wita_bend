"""The app module, containing the app factory function."""
import logging
import sys

from flask import Flask

from apps import commands, sample
from apps.extensions import csrf_protect, db, debug_toolbar, migrate  # noqa
from apps.utils.error_handlers import handle_exception
from apps.utils.handled_errors import BaseModelValidationError
from apps.utils.validators import json_validator
from flask_marshmallow import Marshmallow


def create_app(config_object="apps.settings"):
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    app.url_map.strict_slashes = False

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    register_before_register(app)
    configure_logger(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)

    Marshmallow(app)

    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(sample.views.blueprint)

    return None


def register_errorhandlers(app):
    """Register error handlers."""

    app.register_error_handler(Exception, handle_exception)
    app.register_error_handler(BaseModelValidationError, handle_exception)


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"db": db, "Sample": sample.models.Sample}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)


def register_before_register(app):
    app.before_request(json_validator)
