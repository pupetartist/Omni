from app.util import singleton
from . import null

@singleton
class JsonEncoder:
    encoder = null
