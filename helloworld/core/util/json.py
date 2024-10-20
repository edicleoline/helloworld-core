import json

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, int) and obj > 1e15:
            return str(obj)
        return super().default(obj)

def jsonify(data):
    return json.dumps(data, cls=CustomJSONEncoder)