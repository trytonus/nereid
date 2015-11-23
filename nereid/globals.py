# This file is part of Tryton & Nereid. The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from flask.globals import (_request_ctx_stack, current_app,  # noqa
    request, session, g, LocalProxy, _find_app)
from flask.ext.login import current_user                     # noqa


def _find_cache():
    """
    The application context will be automatically handled by
    _find_app method in flask
    """
    app = _find_app()
    return app.cache


def _get_locale():
    Locale = current_app.pool.get('nereid.website.locale')
    locale_id = getattr(_request_ctx_stack.top, 'locale', None)
    if locale_id is None:
        locale_id = _set_locale()
    return Locale(locale_id)


def _set_locale():
    website = _get_website()
    locale = website.get_current_locale(_request_ctx_stack.top.request)
    _request_ctx_stack.top.locale = locale.id
    return locale.id


def _get_website():
    Website = current_app.pool.get('nereid.website')
    website_id = getattr(_request_ctx_stack.top, 'website', None)
    if website_id is None:
        website_id = _set_website()
    return Website(website_id)


def _set_website():
    Website = current_app.pool.get('nereid.website')
    website = Website.get_from_host(_request_ctx_stack.top.request.host)
    _request_ctx_stack.top.website = website.id
    return website.id


cache = LocalProxy(_find_cache)
current_locale = LocalProxy(lambda: _get_locale())
current_website = LocalProxy(lambda: _get_website())
