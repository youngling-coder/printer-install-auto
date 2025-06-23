from flask import Flask, render_template_string
from storage import Storage


app = Flask(__name__)
storage = Storage()


HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Printer Management</title>
    <style>
        body { font-family: sans-serif; margin: 40px; }
        h2 { color: #333; }
        table { border-collapse: collapse; width: 100%; margin-bottom: 30px; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>Printer Overview</h1>
    {% for location in locations %}
        <h2>{{ location.name }}</h2>
        <table>
            <thead>
                <tr>
                    <th>IP</th>
                    <th>Name</th>
                    <th>Driver</th>
                    <th>Model</th>
                    <th>Available</th>
                </tr>
            </thead>
            <tbody>
                {% for printer in location.printers %}
                <tr>
                    <td>{{ printer.ip }}</td>
                    <td>{{ printer.name }}</td>
                    <td>{{ printer.driver_name }}</td>
                    <td>{{ printer.model }}</td>
                    <td>{{ "✅" if printer.is_available else "❌" }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    {% endfor %}
</body>
</html>
"""


@app.route("/")
def index():

    storage.load_from_json(output=False)

    data = []
    for location in storage.get_locations():
        data.append(
            {
                "name": location.name,
                "printers": [
                    {**printer.to_dict(), "is_available": printer.is_available()}
                    for printer in location.get_printers()
                ],
            }
        )
    return render_template_string(HTML_TEMPLATE, locations=data)


if __name__ == "__main__":
    app.run(port=8765)
