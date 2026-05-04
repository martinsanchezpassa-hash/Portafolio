import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)
app.secret_key = "portafolio-secret-key"

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_photos():
    photos = []
    for filename in sorted(os.listdir(UPLOAD_FOLDER)):
        if allowed_file(filename):
            photos.append(filename)
    return photos


@app.route("/")
def index():
    photos = get_photos()
    return render_template("index.html", photos=photos)


@app.route("/upload", methods=["POST"])
def upload():
    if "photo" not in request.files:
        flash("No se seleccionó ningún archivo.")
        return redirect(url_for("index"))

    file = request.files["photo"]

    if file.filename == "":
        flash("No se seleccionó ningún archivo.")
        return redirect(url_for("index"))

    if not allowed_file(file.filename):
        flash("Formato no permitido. Usá PNG, JPG, JPEG, GIF o WEBP.")
        return redirect(url_for("index"))

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    # Avoid overwriting: add suffix if file already exists
    base, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(filepath):
        filename = f"{base}_{counter}{ext}"
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        counter += 1

    file.save(filepath)

    # Validate it's a real image
    try:
        with Image.open(filepath) as img:
            img.verify()
    except Exception:
        os.remove(filepath)
        flash("El archivo no es una imagen válida.")
        return redirect(url_for("index"))

    flash(f"Foto '{filename}' subida correctamente.")
    return redirect(url_for("index"))


@app.route("/delete/<filename>", methods=["POST"])
def delete(filename):
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(filename))
    if os.path.exists(filepath):
        os.remove(filepath)
        flash(f"Foto '{filename}' eliminada.")
    else:
        flash("Foto no encontrada.")
    return redirect(url_for("index"))


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run(debug=True)
