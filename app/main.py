import uvicorn

from app.utils.factories import (
    create_app,
    custom_openapi,
    setup_cors,
    setup_database,
    setup_routes,
)

app = create_app()

setup_database(app)
setup_cors(app)
setup_routes(app)

custom_openapi(app)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
