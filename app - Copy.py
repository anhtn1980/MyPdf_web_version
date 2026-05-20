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

        # Lấy tên file gốc
        original_filename = pdf_file.filename

        # Tách tên và extension
        base_name, ext = os.path.splitext(original_filename)

        # Tạo đường dẫn file
        input_pdf_path = os.path.join(
            UPLOAD_FOLDER,
            f"{base_name}_input{ext}"
        )

        output_pdf_path = os.path.join(
            UPLOAD_FOLDER,
            f"{base_name}_highlighted{ext}"
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
            as_attachment=True,
            download_name=f"{base_name}_highlighted{ext}"
        )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
