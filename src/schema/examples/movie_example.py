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
        "description": "Género no válido",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Genre with ID 99 not found."
                }
            }
        }
    },
    422: {
        "description": "Error de validación",
        "content": {
            "application/json": {
                "example": {
                    "detail": [
                        {
                            "loc": ["body", "title"],
                            "msg": "Title cannot be empty.",
                            "type": "value_error"
                        },
                        {
                            "loc": ["body", "duration_minutes"],
                            "msg": "Duration must be a positive integer.",
                            "type": "value_error"
                        },
                        {
                            "loc": ["body", "year"],
                            "msg": "Year must be between 1888 and next year.",
                            "type": "value_error"
                        }
                    ]
                }
            }
        }
    }
}

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

movie_update_examples = {
    200: {
        "description": "Película actualizada exitosamente",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "title": "Inception (Updated)",
                    "description": "Updated description",
                    "poster_url": "https://example.com/inception-updated.jpg",
                    "year": 2010,
                    "duration_minutes": 150,
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
        "description": "Género no válido",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Genre with ID 42 not found."
                }
            }
        }
    },
    404: {
        "description": "Película no encontrada",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Movie with ID 55 not found."
                }
            }
        }
    },
    422: {
        "description": "Error de validación",
        "content": {
            "application/json": {
                "example": {
                    "detail": [
                        {
                            "loc": ["body", "duration_minutes"],
                            "msg": "Duration must be a positive integer.",
                            "type": "value_error"
                        }
                    ]
                }
            }
        }
    }
}

movie_delete_examples = {
    204: {
        "description": "Película eliminada exitosamente"
    },
    404: {
        "description": "Película no encontrada",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Movie with ID 77 not found."
                }
            }
        }
    }
}
