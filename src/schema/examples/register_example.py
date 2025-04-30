register_examples = {
    201: {
        "description": "User registered successfully",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "name": "Joseph",
                    "lastname": "Meneses",
                    "nickname": "joamy",
                    "email": "joamy@example.com",
                    "country_code": "+591",
                    "phone_number": "71234567",
                    "country": "Bolivia"
                }
            }
        }
    },
    400: {
        "description": "Phone number or email already registered",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Phone number is already registered."
                }
            }
        }
    },
    422: {
        "description": "Validation error - invalid input (e.g., bad email format or weak password)",
        "content": {
            "application/json": {
                "example": {
                    "detail": [
                        {
                            "loc": ["body", "email"],
                            "msg": "value is not a valid email address",
                            "type": "value_error.email"
                        },
                        {
                            "loc": ["body", "password"],
                            "msg": "Password must contain at least one special character",
                            "type": "value_error"
                        }
                    ]
                }
            }
        }
    }
}
