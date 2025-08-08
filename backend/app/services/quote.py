import json
from typing import List, Optional

from ..data.models.quote import Quote, QuoteRequest, QuoteResponse
from ..data.utilities import data_file
from .server import ServerService


class QuoteService:
    """Service for managing quote requests with in-memory JSONL persistence."""

    def __init__(self, server_service: ServerService):
        self.server_service = server_service
        self.quotes_file_path = data_file("quotes.jsonl")
        self._ensure_file_exists()

    def create_quote(self, request: QuoteRequest) -> QuoteResponse:
        try:
            config_response = self.server_service.get_server_configuration(request.configuration)
        except ValueError as e:
            raise ValueError(f"Invalid configuration: {e}")

        quote = Quote(
            configuration=request.configuration,
            contact_name=request.contact_name,
            contact_email=request.contact_email,
            company=request.company,
            total_price=config_response.total_price,
            total_discount=config_response.total_discount,
        )

        self._append_quote(quote)

        return QuoteResponse(
            id=quote.id,
            total_price=quote.total_price,
            created_at=quote.created_at,
        )

    def get_quote(self, quote_id: str) -> Optional[Quote]:
        try:
            with open(self.quotes_file_path, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        quote_data = json.loads(line)
                        if quote_data.get("id") == quote_id:
                            return Quote.model_validate(quote_data)
                    except (json.JSONDecodeError, ValueError):
                        continue
            return None
        except FileNotFoundError:
            return None

    def list_quotes(self) -> List[Quote]:
        quotes = []
        try:
            with open(self.quotes_file_path, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        quote_data = json.loads(line)
                        quotes.append(Quote.model_validate(quote_data))
                    except (json.JSONDecodeError, ValueError):
                        continue
        except FileNotFoundError:
            pass

        return quotes

    def _append_quote(self, quote: Quote) -> None:
        try:
            self.quotes_file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.quotes_file_path, "a", encoding="utf-8") as file:
                quote_json = quote.model_dump_json()
                file.write(f"{quote_json}\n")
                file.flush()
        except IOError as e:
            raise RuntimeError(f"Failed to save quote: {e}")

    def _ensure_file_exists(self) -> None:
        try:
            self.quotes_file_path.parent.mkdir(parents=True, exist_ok=True)
            if not self.quotes_file_path.exists():
                self.quotes_file_path.touch()
        except IOError as e:
            raise RuntimeError(f"Failed to initialize quotes file: {e}")
