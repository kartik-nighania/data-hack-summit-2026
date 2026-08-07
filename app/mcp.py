"""Mock world + Meridian's service-desk MCP server (FastMCP, stdio transport).

Data: database.json holds the transactional records, knowledge_base.json the
policy corpus the retriever searches. Both are read-only fixtures; runtime
mutations (new tickets) stay in memory and are never written back. Ticket ids
are derived from the tickets table itself (500 + row count), so no counter
state needs to persist anywhere.

Server: the agent does not import the two ticket tools — it connects to this
module over stdio and discovers them via MCP (see SERVICE_MCP_SERVERS in
app/agent.py). Run with `python -m app.mcp` from the repo root. Do NOT run
`python app/mcp.py`: that puts app/ first on sys.path and this file would
shadow the real `mcp` package that fastmcp imports internally.
"""
import json
import os
from typing import Literal

os.environ.setdefault("FASTMCP_LOG_LEVEL", "WARNING")   # keep per-call stderr quiet

from fastmcp import FastMCP
from pydantic import BaseModel, Field, ValidationError

from app.config import DATA_DIR

# ── the mock world ───────────────────────────────────────────────────────────
_db = json.loads((DATA_DIR / "database.json").read_text())
CUSTOMERS = _db["CUSTOMERS"]
LOANS = _db["LOANS"]
TICKETS = _db["TICKETS"]
POLICY_KB = json.loads((DATA_DIR / "knowledge_base.json").read_text())


class TicketRequest(BaseModel):
    customer_id: str = Field(pattern=r"^CUST-\d{4}$")
    category: Literal["statement_request", "address_change", "complaint", "prepayment_request", "other"]
    description: str = Field(min_length=15)


def new_ticket(customer_id: str, category: str, description: str) -> str:
    """Validate and raise a service ticket; returns the JSON the tool exposes."""
    try:
        req = TicketRequest(customer_id=customer_id, category=category, description=description)
    except ValidationError as e:
        return f"ERROR: invalid ticket request: {e.errors()[0]['msg']}"
    tid = f"TKT-2026-{500 + len(TICKETS):04d}"
    TICKETS[tid] = {**req.model_dump(), "status": "open", "created": "2026-07-20", "owner": "L1-support"}
    return json.dumps({"ticket_id": tid, "status": "open",
                       "sla": "acknowledged in 48h, resolution target 7 days"})


def ticket_status(ticket_id: str) -> str:
    t = TICKETS.get(ticket_id)
    return json.dumps({"ticket_id": ticket_id, **t}) if t else f"ERROR: no ticket {ticket_id}"


# ── the MCP server ───────────────────────────────────────────────────────────
mcp = FastMCP("meridian-service-desk")


@mcp.tool
def create_ticket(customer_id: str, category: str, description: str) -> str:
    """Raise a service ticket (category: statement_request|address_change|complaint|prepayment_request|other)."""
    return new_ticket(customer_id, category, description)


@mcp.tool
def get_ticket_status(ticket_id: str) -> str:
    """Check an existing ticket's status by its TKT- id."""
    return ticket_status(ticket_id)


if __name__ == "__main__":
    # stdio is the default transport; the banner would spam stderr on every
    # tool call (the client spawns a fresh server per call)
    mcp.run(show_banner=False)
