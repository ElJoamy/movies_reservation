update_profile_example = {
    200: {
        "description": "User profile updated successfully.",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "name": "Juan",
                    "lastname": "Perez",
                    "nickname": "juanito",
                    "email": "juan@example.com",
                    "country_code": "+591",
                    "phone_number": "69898989",
                    "country": "Bolivia"
                }
            }
        }
    },
    400: {
        "description": "Validation error (e.g. phone already exists)",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Phone number is already registered."
                }
            }
        }
    },
    401: {
        "description": "Unauthorized - missing or invalid token",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Not authenticated"
                }
            }
        }
    },
    500: {
        "description": "Unexpected server error",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Internal Server Error. Please try again later."
                }
            }
        }
    }
}
