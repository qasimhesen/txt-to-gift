from flask import Flask, request, send_file, render_template_string
import io

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
        lines = q.split("\n")
        out.append(lines[0])
        out.append("{")
        for l in lines[1:]:
            l = l.strip()
            if l.startswith("*"):
                out.append("= " + l[1:].split(")",1)[1].strip())
            else:
                out.append("~ " + l.split(")",1)[1].strip())
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

app.run()
