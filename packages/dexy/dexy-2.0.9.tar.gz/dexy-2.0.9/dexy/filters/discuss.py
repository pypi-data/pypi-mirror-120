from dexy.filters.api import ApiFilter

try:
    import discourse
    AVAILABLE = False
except ImportError:
    AVAILABLE = True

class DiscussFilter(ApiFilter):
    """
    Filter for posting text, files, or images to a matrix room. Uses matrix-nio

    Create a .dexyapis JSON file in your HOME dir with format:

    {
        "matrix": {
            "homeserver" : "https://example.org",
            "username" :  "@example:example.org",
            "password" : "sekret1!"
        }
    }

    """
    aliases = ['discuss', 'discourse']

    def is_active(self):
        return AVAILABLE

    def process(self):
        if self.input_data.ext in ('.txt'):
            pass

client = discourse.Client(
    host='http://127.0.0.1:3000/',
    api_username='discourse1',
    api_key='714552c6148e1617aeab526d0606184b94a80ec048fc09894ff1a72b740c5f19',
)
