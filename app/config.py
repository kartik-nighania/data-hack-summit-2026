"""Workshop configuration: constants from config.yaml + keys from .env / environment.

Import-time discipline: importing this module does NO network calls — the Langfuse
client, project id, etc. are created lazily on first use so `import app.*` stays fast
and works before keys are loaded.
"""
import os
from pathlib import Path

import yaml

os.environ.setdefault("DEEPEVAL_TELEMETRY_OPT_OUT", "1")   # no analytics
os.environ.setdefault("DEEPEVAL_DISABLE_DOTENV", "1")      # don't auto-load .env files
os.environ.setdefault("DEEPEVAL_NO_INSPECT_PROMPT", "1")   # no post-run TUI prompts

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"

CONFIG = yaml.safe_load((REPO_ROOT / "config.yaml").read_text())
AGENT_MODEL = CONFIG["agent_model"]
JUDGE_MODEL = CONFIG["judge_model"]
DATASET_NAME = CONFIG["dataset_name"]
CANDIDATES_DATASET_NAME = CONFIG["candidates_dataset_name"]
EXPERIMENT_CONCURRENCY = CONFIG["experiment_concurrency"]
INGESTION_WAIT_S = CONFIG["ingestion_wait_s"]
TRAFFIC_SESSIONS = CONFIG["traffic_sessions"]


def load_env():
    """Load keys from .env (setdefault — real env vars win) and normalize the host:
    the SDK reads LANGFUSE_BASE_URL, older docs use LANGFUSE_HOST; we keep both set."""
    env_file = REPO_ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
    host = (os.environ.get("LANGFUSE_HOST") or os.environ.get("LANGFUSE_BASE_URL")
            or CONFIG["langfuse_host"])
    os.environ["LANGFUSE_HOST"] = os.environ["LANGFUSE_BASE_URL"] = host.strip().rstrip("/")
    return os.environ["LANGFUSE_HOST"]


_CLIENT_INITIALIZED = False


REQUIRED_KEYS = ["OPENAI_API_KEY", "LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY"]


def load_keys():
    """Load API keys: .env at the repo root (copy .env.example and fill it in) → env vars → manual prompt."""
    load_env()   # reads .env; real env vars win; host gets normalized, quotes stripped
    source = ".env / environment"
    missing = [k for k in REQUIRED_KEYS if not os.environ.get(k)]
    if missing:
        print(f"⚠️  missing {missing}")
        print("   Fix: copy .env.example to .env at the repo root and paste your keys — or enter them now:")
        from getpass import getpass
        for name in missing:
            os.environ[name] = getpass(f"Paste {name}: ").strip()
        source = "manual input"
    print(f"✅ keys loaded from {source} | Langfuse host: {os.environ['LANGFUSE_HOST']}")


def get_lf():
    """The shared Langfuse client (created on first call, after load_env), with the
    PII masking hook registered — masking is a no-op until PII_PATTERNS is filled
    (see app/pii_data_masking.py)."""
    from langfuse import Langfuse, get_client

    from app.pii_data_masking import pii_masking_hook
    global _CLIENT_INITIALIZED
    load_env()
    if not _CLIENT_INITIALIZED:
        Langfuse(
            public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
            secret_key=os.environ["LANGFUSE_SECRET_KEY"],
            base_url=os.environ["LANGFUSE_HOST"],
            environment="development",
            mask_otel_spans=pii_masking_hook,
        )
        _CLIENT_INITIALIZED = True
    return get_client()


_PROJECT_ID = None


def trace_url(trace_id: str) -> str:
    global _PROJECT_ID
    if _PROJECT_ID is None:
        _PROJECT_ID = get_lf().api.projects.get().data[0].id
    return f"{os.environ['LANGFUSE_HOST']}/project/{_PROJECT_ID}/traces/{trace_id}"
