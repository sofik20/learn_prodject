from apiflask import APIFlask
from backend.api.routes import register_routes

app = APIFlask(
    __name__,
    title="Backend API",
    version="1.0.0",
    docs_path="/docs"
)

app.config["SYNC_LOCAL_SPEC"] = False

register_routes(app)

if __name__ == "__main__":
    app.run(port=5001, debug=True)