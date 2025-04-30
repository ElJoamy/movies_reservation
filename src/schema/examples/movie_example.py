# POST /movies
movie_create_examples = {
    201: {
        "description": "Película creada exitosamente",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "title": "Inception",
                    "description": "A mind-bending thriller",
                    "poster_url": "https://example.com/inception.jpg",
                    "year": 2010,
                    "duration_minutes": 148,
                    "director": "Christopher Nolan",
                    "genres": [
                        {"id": 1, "name": "Sci-Fi"},
                        {"id": 2, "name": "Action"}
                    ]
                }
            }
        }
    },
    400: {
        "description": "Género no válido o faltante",
        "content": {
            "application/json": {
                "example": {
                    "detail": "One or more genre IDs are invalid."
                }
            }
        }
    },
    422: {
        "description": "Error de validación en los datos enviados",
        "content": {
            "application/json": {
                "example": {
                    "detail": [
                        {
                            "loc": ["body", "poster_url"],
                            "msg": "URL scheme not permitted",
                            "type": "value_error.url.scheme"
                        },
                        {
                            "loc": ["body", "year"],
                            "msg": "ensure this value is less than or equal to 2100",
                            "type": "value_error.number.not_le"
                        }
                    ]
                }
            }
        }
    }
}

# GET /movies/{id}
movie_detail_examples = {
    200: {
        "description": "Detalle de película",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "title": "Inception",
                    "description": "A mind-bending thriller",
                    "poster_url": "https://example.com/inception.jpg",
                    "year": 2010,
                    "duration_minutes": 148,
                    "director": "Christopher Nolan",
                    "genres": [
                        {"id": 1, "name": "Sci-Fi"},
                        {"id": 2, "name": "Action"}
                    ]
                }
            }
        }
    },
    404: {
        "description": "Película no encontrada",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Movie with ID 42 not found."
                }
            }
        }
    }
}

# GET /movies
movie_list_examples = {
    200: {
        "description": "Lista de películas",
        "content": {
            "application/json": {
                "example": [
                    {
                        "id": 1,
                        "title": "Inception",
                        "poster_url": "https://example.com/inception.jpg",
                        "year": 2010,
                        "duration_minutes": 148,
                        "director": "Christopher Nolan",
                        "genres": [
                            {"id": 1, "name": "Sci-Fi"},
                            {"id": 2, "name": "Action"}
                        ]
                    },
                    {
                        "id": 2,
                        "title": "Interstellar",
                        "poster_url": "https://example.com/interstellar.jpg",
                        "year": 2014,
                        "duration_minutes": 169,
                        "director": "Christopher Nolan",
                        "genres": [
                            {"id": 1, "name": "Sci-Fi"},
                            {"id": 3, "name": "Drama"}
                        ]
                    }
                ]
            }
        }
    }
}

# PUT /movies/{id}
movie_update_examples = {
    200: {
        "description": "Película actualizada exitosamente",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "title": "Inception (Updated)",
                    "duration_minutes": 150,
                    "genres": [
                        {"id": 1, "name": "Sci-Fi"},
                        {"id": 2, "name": "Action"}
                    ]
                }
            }
        }
    },
    404: {
        "description": "Película no encontrada para actualizar",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Movie with ID 55 not found."
                }
            }
        }
    }
}

# DELETE /movies/{id}
movie_delete_examples = {
    204: {
        "description": "Película eliminada exitosamente",
        "content": {
            "application/json": {
                "example": {}
            }
        }
    },
    404: {
        "description": "Película no encontrada para eliminar",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Movie with ID 77 not found."
                }
            }
        }
    }
}
