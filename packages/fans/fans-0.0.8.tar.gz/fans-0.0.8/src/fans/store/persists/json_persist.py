import json


class Persist:

    def load(self, path, hint, **kwargs):
        with path.open() as f:
            return json.load(f, **kwargs)

    def save(self, path, data, hint, **kwargs):
        kwargs.setdefault('ensure_ascii', False)
        # TODO: atomic write
        with path.open('w') as f:
            json.dump(data, f, **kwargs)
