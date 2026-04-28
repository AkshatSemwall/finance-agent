import json
import os
import tempfile

import pytest

from app.sources.csv_importer import CsvImporter
from app.config import settings

VALID_CSV_CONTENT = """date,description,amount,category
2024-01-15,Grocery Store,-45.50,food
2024-01-16,Gas Station,-30.00,transport
"""

CSV_WITHOUT_CATEGORY = """date,description,amount
2024-01-15,Grocery Store,-45.50
"""

class TestCsvImporter:
    def test_parse_csv_with_category(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(VALID_CSV_CONTENT)
            csv_path = f.name
        
        importer = CsvImporter()
        transactions = importer._parse_csv(csv_path)
        assert len(transactions) == 2
        assert transactions[0]['description'] == "Grocery Store"
        assert transactions[0]['amount'] == -45.50
        assert transactions[0]['category'] == "food"
        os.unlink(csv_path)

    def test_parse_csv_auto_category(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(CSV_WITHOUT_CATEGORY)
            csv_path = f.name
        
        importer = CsvImporter()
        transactions = importer._parse_csv(csv_path)
        assert transactions[0]['category'] == "uncategorized"
        os.unlink(csv_path)

    def test_import_csv_appends(self, tmp_path):
        temp_csv = tmp_path / "test.csv"
        temp_csv.write_text(VALID_CSV_CONTENT)
        
        original_file = settings.transactions_file
        temp_transactions = tmp_path / "transactions.json"
        settings.transactions_file = str(temp_transactions)
        
        importer = CsvImporter(csv_path=str(temp_csv))
        # Since transactions file doesn't exist, it seeds with csv
        transactions = importer.fetch()
        assert len(transactions) == 2
        
        # Import again, should append
        importer.import_csv(str(temp_csv))
        transactions = importer.fetch()
        assert len(transactions) == 4
        
        settings.transactions_file = original_file

    def test_fetch_returns_list(self):
        importer = CsvImporter()
        transactions = importer.fetch()
        assert isinstance(transactions, list)
