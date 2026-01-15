def normalize(payload):
    return {
        "channel": payload.get("channel"),
        "text": payload.get("message"),
        "user_id": payload.get("user_id")
    }
