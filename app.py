from flask import Flask, render_template, request, send_file
import img2pdf
from io import BytesIO

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        files = request.files.getlist("images")
        if not files:
            return "No files uploaded", 400

        image_data = []
        for file in files:
            if file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
                image_data.append(file.read())

        if not image_data:
            return "No valid image files", 400

        pdf_bytes = img2pdf.convert(image_data)
        return send_file(BytesIO(pdf_bytes), download_name="converted.pdf", as_attachment=True, mimetype="application/pdf")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)