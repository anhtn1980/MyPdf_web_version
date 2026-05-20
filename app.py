from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        pdf_file = request.files.get("pdf_file")
        keywords = request.form.get("keywords")

        return f"""
        Upload thành công!<br><br>

        File: {pdf_file.filename}<br><br>

        Keywords:<br>
        {keywords}
        """

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
