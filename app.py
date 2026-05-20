from flask import Flask, render_template, request, send_file
import fitz
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        pdf_file = request.files.get("pdf_file")
        keywords_text = request.form.get("keywords")

        if not pdf_file:
            return "Không có file PDF"

        # Tạo tên file random
        unique_id = str(uuid.uuid4())

        input_pdf_path = os.path.join(
            UPLOAD_FOLDER,
            f"{unique_id}_input.pdf"
        )

        output_pdf_path = os.path.join(
            UPLOAD_FOLDER,
            f"{unique_id}_highlighted.pdf"
        )

        # Save file upload
        pdf_file.save(input_pdf_path)

        # Tách keywords
        keywords = [
            k.strip()
            for k in keywords_text.splitlines()
            if k.strip()
        ]

        # Mở PDF
        doc = fitz.open(input_pdf_path)

        # Highlight keywords
        for page_num in range(len(doc)):

            page = doc.load_page(page_num)

            for keyword in keywords:

                text_instances = page.search_for(keyword)

                for inst in text_instances:
                    page.add_highlight_annot(inst)

        # Save output
        doc.save(output_pdf_path)
        doc.close()

        # Download file
        return send_file(
            output_pdf_path,
            as_attachment=True
        )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
