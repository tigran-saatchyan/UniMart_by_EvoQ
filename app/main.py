import uvicorn

from app.utils.factories import (
    create_app,
    setup_database,
    setup_cors,
    setup_routes,
    custom_openapi,
)

app = create_app()

setup_database(app)
setup_cors(app)
setup_routes(app)

custom_openapi(app)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
