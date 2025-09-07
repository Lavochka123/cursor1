# svety/web/__init__.py
from __future__ import annotations

from datetime import datetime, timezone

from flask import Flask, jsonify, render_template, abort, send_from_directory
import json
from pathlib import Path

from svety.core.config import cfg

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["SECRET_KEY"] = cfg.SECRET_KEY


@app.get("/")
def index():
    """Главная страница."""
    return render_template("index.html", year=datetime.now().year)


@app.get("/healthz")
def healthz():
    """Пробный эндпоинт для проверки живости приложения."""
    return jsonify(status="ok", ts=datetime.now(timezone.utc).isoformat())


@app.get("/p/<pid>")
def project_page(pid: str):
    """
    Страница проекта с красивым превью: показывает три картинки (если есть),
    приветствие, согласие/несогласие и комментарий.
    Ищем проект по всем пользовательским каталогам (tg_id нам неизвестен в вебе).
    """
    base: Path = cfg.DATA_DIR
    if not base.exists():
        abort(404)
    found = None
    user_id = None
    for uid_dir in base.iterdir():
        meta = uid_dir / pid / "meta.json"
        if meta.exists():
            try:
                data = json.loads(meta.read_text(encoding="utf-8"))
                found = data
                user_id = uid_dir.name
                break
            except Exception:
                continue
    if not found:
        abort(404)

    # Пути к страницам
    proj_dir = base / str(user_id) / pid
    p1 = proj_dir / "tri_page1.jpg"
    p2 = proj_dir / "tri_page2.jpg"
    p3 = proj_dir / "tri_page3.jpg"

    return render_template(
        "project.html",
        pid=pid,
        title=found.get("title", ""),
        greeting=found.get("tri_greeting", ""),
        consent=found.get("tri_consent", None),
        comment=found.get("tri_comment", ""),
        img1=str(p1.relative_to(cfg.DATA_DIR)) if p1.exists() else None,
        img2=str(p2.relative_to(cfg.DATA_DIR)) if p2.exists() else None,
        img3=str(p3.relative_to(cfg.DATA_DIR)) if p3.exists() else None,
        year=datetime.now().year,
    )


@app.get("/data/<path:subpath>")
def data_files(subpath: str):
    """Отдаём файлы из каталога DATA_DIR безопасно (только чтение)."""
    base: Path = cfg.DATA_DIR
    # Ограничим выход из каталога
    safe_path = (base / subpath).resolve()
    if not str(safe_path).startswith(str(base.resolve())) or not safe_path.exists():
        abort(404)
    return send_from_directory(base, subpath)


__all__ = ["app"]

