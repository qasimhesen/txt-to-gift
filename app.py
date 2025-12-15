from flask import Flask, request, send_file, render_template_string
import io
import os
import re

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>TXT to GIFT Converter</title>
</head>
<body>
<h1>TXT to GIFT Converter</h1>
<p>Upload a .txt file and get GIFT format.</p>

<form method="post" enctype="multipart/form-data">
<input type="file" name="file" required>
<br><br>
<button type="submit">Convert</button>
</form>
</body>
</html>
"""


def convert_to_gift(text):
    lines = [l.rstrip() for l in text.splitlines()]
    out = []

    current_question = None
    answers = []

    def flush_question():
        if current_question and answers:
            out.append(current_question)
            out.append("{")
            for a in answers:
                out.append(a)
            out.append("}\n")

    for line in lines:
        line = line.strip()

        # Yeni sual (1. , 2. , 3. və s.)
        if re.match(r"^\d+\.\s+", line):
            flush_question()
            current_question = line
            answers = []
            continue

        # Variantlar
        if ")" in line:
            parts = line.split(")", 1)
            answer_text = parts[1].strip()

            if not answer_text:
                continue

            if line.startswith("*"):
                answers.append("= " + answer_text)
            else:
                answers.append("~ " + answer_text)

    flush_question()
    return "\n".join(out)



@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        text = file.read().decode("utf-8")
        gift = convert_to_gift(text)

        return send_file(
            io.BytesIO(gift.encode()),
            as_attachment=True,
            download_name="quiz.gift",
            mimetype="text/plain"
        )

    return render_template_string(HTML)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



