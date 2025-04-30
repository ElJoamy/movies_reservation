genre_create_examples = {
    201: {
        "description": "Género creado exitosamente",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "name": "Acción"
                }
            }
        }
    }
}

genre_update_examples = {
    200: {
        "description": "Género actualizado exitosamente",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "name": "Aventura"
                }
            }
        }
    }
}

genre_list_examples = {
    200: {
        "description": "Lista de géneros",
        "content": {
            "application/json": {
                "example": [
                    {"id": 1, "name": "Comedia"},
                    {"id": 2, "name": "Drama"}
                ]
            }
        }
    }
}

genre_detail_examples = {
    200: {
        "description": "Detalle del género",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "name": "Ciencia Ficción"
                }
            }
        }
    },
    404: {
        "description": "Género no encontrado",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Genre with ID 99 not found."
                }
            }
        }
    }
}

genre_delete_examples = {
    204: {
        "description": "Género eliminado exitosamente"
    },
    404: {
        "description": "Género no encontrado",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Genre with ID 99 not found."
                }
            }
        }
    }
}
