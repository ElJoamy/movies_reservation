from datetime import datetime

showtime_create_examples = {
    201: {
        "description": "Showtime created successfully",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "show_datetime": "2025-05-01T19:00:00",
                    "movie": {
                        "id": 5,
                        "title": "Inception",
                        "description": "A mind-bending thriller",
                        "poster_url": "https://example.com/inception.jpg",
                        "duration_minutes": 148,
                        "director": "Christopher Nolan"
                    },
                    "seats": [
                        {"id": 1, "seat_number": "A1", "is_reserved": False},
                        {"id": 2, "seat_number": "A2", "is_reserved": False}
                    ]
                }
            }
        }
    },
    400: {
        "description": "Invalid data",
        "content": {
            "application/json": {
                "examples": {
                    "invalid_movie": {
                        "summary": "Movie not found",
                        "value": {
                            "detail": "Movie with ID 5 not found."
                        }
                    },
                    "past_date": {
                        "summary": "Date is in the past",
                        "value": {
                            "detail": "Cannot create a showtime in the past."
                        }
                    }
                }
            }
        }
    }
}

showtime_update_examples = {
    200: {
        "description": "Showtime updated successfully",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "show_datetime": "2025-05-01T20:30:00",
                    "movie": {
                        "id": 5,
                        "title": "Inception",
                        "description": "A mind-bending thriller",
                        "poster_url": "https://example.com/inception.jpg",
                        "duration_minutes": 148,
                        "director": "Christopher Nolan"
                    },
                    "seats": [
                        {"id": 1, "seat_number": "A1", "is_reserved": True},
                        {"id": 2, "seat_number": "A2", "is_reserved": False}
                    ]
                }
            }
        }
    },
    400: {
        "description": "Invalid update",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Cannot update a showtime to a past datetime."
                }
            }
        }
    },
    404: {
        "description": "Showtime not found",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Showtime with ID 1 not found."
                }
            }
        }
    }
}

showtime_list_examples = {
    200: {
        "description": "List of grouped showtimes by movie",
        "content": {
            "application/json": {
                "example": [
                    {
                        "id": 5,
                        "title": "Inception",
                        "description": "A mind-bending thriller",
                        "poster_url": "https://example.com/inception.jpg",
                        "duration_minutes": 148,
                        "director": "Christopher Nolan",
                        "showtimes": [
                            {"id": 1, "show_datetime": "2025-05-01T19:00:00"},
                            {"id": 2, "show_datetime": "2025-05-02T21:00:00"}
                        ]
                    },
                    {
                        "id": 6,
                        "title": "Interstellar",
                        "description": "Journey beyond the stars",
                        "poster_url": "https://example.com/interstellar.jpg",
                        "duration_minutes": 169,
                        "director": "Christopher Nolan",
                        "showtimes": [
                            {"id": 3, "show_datetime": "2025-05-01T20:00:00"}
                        ]
                    }
                ]
            }
        }
    }
}

showtime_detail_examples = {
    200: {
        "description": "Showtime detail",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "show_datetime": "2025-05-01T19:00:00",
                    "movie": {
                        "id": 5,
                        "title": "Inception",
                        "description": "A mind-bending thriller",
                        "poster_url": "https://example.com/inception.jpg",
                        "duration_minutes": 148,
                        "director": "Christopher Nolan"
                    },
                    "seats": [
                        {"id": 1, "seat_number": "A1", "is_reserved": True},
                        {"id": 2, "seat_number": "A2", "is_reserved": False}
                    ]
                }
            }
        }
    },
    404: {
        "description": "Showtime not found",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Showtime with ID 1 not found."
                }
            }
        }
    }
}

showtime_delete_examples = {
    204: {
        "description": "Showtime deleted successfully"
    },
    404: {
        "description": "Showtime not found",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Showtime with ID 1 not found."
                }
            }
        }
    }
}

showtime_search_examples = {
    200: {
        "description": "Showtimes found for specified date and time",
        "content": {
            "application/json": {
                "example": [
                    {
                        "id": 5,
                        "title": "Inception",
                        "description": "A mind-bending thriller",
                        "poster_url": "https://example.com/inception.jpg",
                        "duration_minutes": 148,
                        "director": "Christopher Nolan",
                        "showtimes": [
                            {"id": 1, "show_datetime": "2025-05-01T19:00:00"}
                        ]
                    }
                ]
            }
        }
    },
    404: {
        "description": "No showtimes found for specified criteria",
        "content": {
            "application/json": {
                "example": {
                    "detail": "No showtimes found for the specified date and time."
                }
            }
        }
    }
}
