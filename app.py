"""Pulse CRM demo — FastAPI + SQLite + Jinja2 (N4).

Palaišana:  uvicorn app:app --reload
Atvērt:     http://127.0.0.1:8000
"""

import os

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from crm import (admin, auth, info, meklesana, mijiedarbibas, organizacijas, panelis, parskats,
                 pieprasijumi, uzdevumi)
from crm.db import BASE_DIR, init_db
from crm.web import Forbidden, LoginRequired, NotFound, current_user, render


def kluda(request: Request, status_code: int, title: str, message: str):
    user = current_user(request)
    return render(request, user, "kluda.html", title, status_code=status_code,
                  layout="base.html" if user else "public.html", message=message)


def create_app() -> FastAPI:
    init_db()
    app = FastAPI(title="Pulse CRM demo", docs_url=None, redoc_url=None, openapi_url=None)
    app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
    for module in (auth, panelis, organizacijas, mijiedarbibas, pieprasijumi, uzdevumi,
                   meklesana, parskats, admin, info):
        app.include_router(module.router)

    @app.exception_handler(LoginRequired)
    def _login(request: Request, exc: LoginRequired):
        return RedirectResponse("/login", status_code=303)

    @app.exception_handler(Forbidden)
    def _forbidden(request: Request, exc: Forbidden):
        return kluda(request, 403, "Piekļuve liegta", exc.message)

    @app.exception_handler(NotFound)
    def _not_found(request: Request, exc: NotFound):
        return kluda(request, 404, "Nav atrasts", "Pieprasītais ieraksts neeksistē vai jums nav piekļuves tam.")

    @app.exception_handler(404)
    def _404(request: Request, exc):
        return kluda(request, 404, "Nav atrasts", "Šāda lapa neeksistē.")

    return app


app = create_app()
