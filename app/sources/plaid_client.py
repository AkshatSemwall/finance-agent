from typing import List, Dict, Any

from app.sources.base import BaseTransactionSource

class PlaidClient(BaseTransactionSource):
    def fetch(self) -> List[Dict[str, Any]]:
        raise NotImplementedError("Plaid integration not implemented yet")