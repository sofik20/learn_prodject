from flask import Flask, render_template
from frontend.clients.backend_client import BackendApiClient

app = Flask(__name__)
backend_client = BackendApiClient("http://localhost:5001")

@app.route("/")
def index():
    status_data = backend_client.get_status()
    items_data = backend_client.get_items()

    return render_template(
        "index.html",
        status_data=status_data,
        items=items_data["items"]
    )

if __name__ == "__main__":
    app.run(port=5000, debug=True)