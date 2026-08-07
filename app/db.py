"""Mock world loaded from data/: database.json holds the transactional records,
knowledge_base.json holds the policy corpus the retriever searches.

Both files are read-only fixtures; runtime mutations (new tickets) stay in memory
and are never written back. Ticket ids are derived from the tickets table itself
(500 + row count), so no counter state needs to persist anywhere.
"""
import json
from typing import Literal

from pydantic import BaseModel, Field

from app.config import DATA_DIR

_db = json.loads((DATA_DIR / "database.json").read_text())
CUSTOMERS = _db["CUSTOMERS"]
LOANS = _db["LOANS"]
TICKETS = _db["TICKETS"]
POLICY_KB = json.loads((DATA_DIR / "knowledge_base.json").read_text())


class TicketRequest(BaseModel):
    """Schema every service ticket must satisfy - our 'argument correctness' ground truth."""
    customer_id: str = Field(pattern=r"^CUST-\d{4}$")
    category: Literal["statement_request", "address_change", "complaint", "prepayment_request", "other"]
    description: str = Field(min_length=15, description="What the customer needs, in one or two sentences")
