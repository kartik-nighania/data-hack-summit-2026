"""PII masking at export time (Module 2.8/2.9).

The hook is registered on the Langfuse client at construction (app/config.py); it is
a no-op until PII_PATTERNS is filled — notebook 00 appends the redaction rules live:

    PII_PATTERNS.extend([
        (re.compile(r"\\b[A-Z]{5}\\d{4}[A-Z]\\b"), "«PAN-REDACTED»"),      # Indian PAN
        (re.compile(r"\\+91[-\\s]?\\d{10}\\b"), "«PHONE-REDACTED»"),       # +91 phone numbers
        (re.compile(r"\\b[\\w.+-]+@[\\w-]+\\.[\\w.]+\\b"), "«EMAIL-REDACTED»"),  # emails
    ])

The model still sees the real values — only the EXPORTED telemetry is masked.
"""

PII_PATTERNS: list = []   # (compiled_regex, replacement_label) tuples


def pii_masking_hook(*, params):
    """Redact PII from every exported span attribute. Runs at export time, so it
    also covers spans created by the LangChain/LangGraph integration."""
    from langfuse.types import MaskOtelSpansResult, OtelSpanPatch
    if not PII_PATTERNS:
        return None
    try:
        patches = {}
        for ident, span in params.spans.items():
            repl = {}
            for key, value in span.attributes.items():
                if isinstance(value, str):
                    masked = value
                    for pattern, label in PII_PATTERNS:
                        masked = pattern.sub(label, masked)
                    if masked != value:
                        repl[key] = masked
            if repl:
                patches[ident] = OtelSpanPatch(set_attributes=repl)
        return MaskOtelSpansResult(span_patches=patches)
    except Exception:
        return None
