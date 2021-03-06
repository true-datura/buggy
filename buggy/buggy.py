# -*- coding: utf-8 -*-
"""Main app script."""
from flask import Flask, render_template

from buggy import commands, comment, post, user
from buggy.assets import assets
from buggy.context_processors import tags_processor
from buggy.extensions import (bcrypt, cache, csrf_protect, db, debug_toolbar,
                              login_manager, migrate)
from buggy.settings import Config, ProdConfig


def create_app(config_object=ProdConfig):
    """
    Application factory, just like here:
    http://flask.pocoo.org/docs/0.12/patterns/appfactories/
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_context_processor(app)
    register_commands(app)
    return app


def register_extensions(app):
    """Registers all extensions."""
    assets.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(post.views.blueprint)
    app.register_blueprint(comment.views.blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code)), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'User': user.models.User,
        }

    app.shell_context_processor(shell_context)


def register_context_processor(app):
    """Registers context processors."""
    def template_context():
        return {
            'ENABLE_DISQUS': Config.ENABLE_DISQUS,
            'DISQUS_SHORTNAME': Config.DISQUS_SHORTNAME,
        }
    app.context_processor(template_context)
    app.context_processor(tags_processor)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)
    app.cli.add_command(commands.createadmin)
