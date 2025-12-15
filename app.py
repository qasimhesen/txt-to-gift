from flask import Flask, request, send_file, render_template_string
import io
import os


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
    questions = text.strip().split("\n\n")
    out = []

    for q in questions:
        lines = [l.strip() for l in q.split("\n") if l.strip()]
        if len(lines) < 2:
            continue

        out.append(lines[0])
        out.append("{")

        for l in lines[1:]:
            # variant formatı yoxlanır: A) text
            if ")" not in l:
                continue

            parts = l.split(")", 1)
            answer = parts[1].strip()

            if not answer:
                continue

            if l.startswith("*"):
                out.append("= " + answer)
            else:
                out.append("~ " + answer)

        out.append("}\n")

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


