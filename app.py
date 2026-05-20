from flask import Flask, render_template, request, send_file
import fitz
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        # =========================
        # LẤY DỮ LIỆU FORM
        # =========================

        pdf_file = request.files.get("pdf_file")
        keywords_text = request.form.get("keywords")
        action = request.form.get("action")

        if not pdf_file:
            return "Không có file PDF"

        # =========================
        # TÊN FILE GỐC
        # =========================

        original_filename = pdf_file.filename

        base_name, ext = os.path.splitext(original_filename)

        # =========================
        # ĐƯỜNG DẪN FILE
        # =========================

        input_pdf_path = os.path.join(
            UPLOAD_FOLDER,
            f"{base_name}_input{ext}"
        )

        # =========================
        # TÊN FILE OUTPUT
        # =========================

        if action == "highlight":

            output_filename = f"{base_name}_highlighted{ext}"

        else:

            output_filename = f"{base_name}_cleaned{ext}"

        output_pdf_path = os.path.join(
            UPLOAD_FOLDER,
            output_filename
        )

        # =========================
        # SAVE FILE UPLOAD
        # =========================

        pdf_file.save(input_pdf_path)

        # =========================
        # KEYWORDS
        # =========================

        keywords = []

        if keywords_text:

            keywords = [
                k.strip()
                for k in keywords_text.splitlines()
                if k.strip()
            ]

        # =========================
        # MỞ PDF
        # =========================

        doc = fitz.open(input_pdf_path)

        # =========================
        # HIGHLIGHT MODE
        # =========================

        if action == "highlight":

            for page_num in range(len(doc)):

                page = doc.load_page(page_num)

                for keyword in keywords:

                    text_instances = page.search_for(keyword)

                    for inst in text_instances:
                        page.add_highlight_annot(inst)

        # =========================
        # REMOVE HIGHLIGHT MODE
        # =========================

        elif action == "remove":

            for page_num in range(len(doc)):

                page = doc.load_page(page_num)

                annotations = page.annots()

                if annotations:

                    annot_list = list(annotations)

                    for annot in annot_list:
                        page.delete_annot(annot)

        # =========================
        # SAVE OUTPUT PDF
        # =========================

        doc.save(output_pdf_path)
        doc.close()

        # =========================
        # DOWNLOAD FILE
        # =========================

        return send_file(
            output_pdf_path,
            as_attachment=True,
            download_name=output_filename
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
