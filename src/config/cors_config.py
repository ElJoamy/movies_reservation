from fastapi.middleware.cors import CORSMiddleware

allowed_origins = [
    '*'
]

def add_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,  # Permitir estos orígenes
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Métodos permitidos
        allow_headers=["Authorization", "Content-Type"],  # Headers permitidos
    )
