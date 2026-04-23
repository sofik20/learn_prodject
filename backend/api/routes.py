from services.status_service import get_status_data, get_items_data
from schemas.status_schema import StatusOutSchema
from schemas.item_schema import ItemsOutSchema


def register_routes(app):
    @app.get("/api/status")
    @app.output(StatusOutSchema)
    def api_status():
        return get_status_data()

    @app.get("/api/items")
    @app.output(ItemsOutSchema)
    def api_items():
        return {"items": get_items_data()}