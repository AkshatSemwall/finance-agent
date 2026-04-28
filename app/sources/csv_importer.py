import csv
import json
import os
from typing import List, Dict, Any

from app.sources.base import BaseTransactionSource
from app.config import settings

class CsvImporter(BaseTransactionSource):
    def __init__(self, csv_path: str = "data/sample.csv"):
        self.csv_path = csv_path
        self._ensure_transactions_file()

    def fetch(self) -> List[Dict[str, Any]]:
        transactions = self._load_transactions()
        return transactions

    def import_csv(self, csv_path: str) -> None:
        new_transactions = self._parse_csv(csv_path)
        existing = self._load_transactions()
        existing.extend(new_transactions)
        self._save_transactions(existing)

    def _parse_csv(self, csv_path: str) -> List[Dict[str, Any]]:
        transactions = []
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Auto-fill missing category
                if not row.get('category') or row['category'].strip() == '':
                    row['category'] = 'uncategorized'
                # Convert amount to float
                row['amount'] = float(row['amount'])
                transactions.append(row)
        return transactions

    def _load_transactions(self) -> List[Dict[str, Any]]:
        if not os.path.exists(settings.transactions_file):
            return []
        with open(settings.transactions_file, 'r') as f:
            return json.load(f)

    def _save_transactions(self, transactions: List[Dict[str, Any]]) -> None:
        os.makedirs(os.path.dirname(settings.transactions_file), exist_ok=True)
        with open(settings.transactions_file, 'w') as f:
            json.dump(transactions, f, indent=2)

    def _ensure_transactions_file(self) -> None:
        if not os.path.exists(settings.transactions_file):
            # Seed with sample data
            sample_transactions = self._parse_csv(self.csv_path)
            self._save_transactions(sample_transactions)