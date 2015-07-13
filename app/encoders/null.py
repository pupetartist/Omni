from app.util import singleton

@singleton
class JsonEncoder:
    def default(self, obj):
        return ''
