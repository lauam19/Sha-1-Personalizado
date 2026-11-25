from flask import Flask, render_template, request
from algorithm.sha1_nl import sha1_nl, sha1_nl_analysis

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    original = None
    error = None
    if request.method == "POST":
        original = request.form.get("message", "")
        try:
            result = sha1_nl(original)
        except Exception as exc:
            error = f"No se pudo procesar el mensaje: {exc}"
    return render_template("index.html", result=result, original=original, error=error)


@app.route("/analysis", methods=["GET", "POST"])
def analysis():
    report = None
    original = ""
    error = None
    if request.method == "POST":
        original = request.form.get("message", "")
        try:
            report = sha1_nl_analysis(original.encode("utf-8"))
        except Exception as exc:
            error = f"No se pudo analizar el mensaje: {exc}"
    return render_template("analysis.html", report=report, original=original, error=error)


if __name__ == "__main__":
    app.run(debug=True)
