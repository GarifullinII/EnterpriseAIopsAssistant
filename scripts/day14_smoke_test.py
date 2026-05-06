from __future__ import annotations

import argparse
import json
from pathlib import Path

import requests


DEFAULT_SAMPLE_FILE = Path("uploads/028a6f84-db48-42ce-bec5-7ae2e93dff1f.pdf")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the Day 14 end-to-end smoke test for the project."
    )
    parser.add_argument("--api-base", default="http://127.0.0.1:8000")
    parser.add_argument("--n8n-base", default="http://127.0.0.1:5678")
    parser.add_argument(
        "--sample-file",
        default=str(DEFAULT_SAMPLE_FILE),
        help="Path to a sample PDF/DOC file for upload and full pipeline testing.",
    )
    parser.add_argument(
        "--search-query",
        default="accountant safety requirements",
    )
    parser.add_argument(
        "--ask-question",
        default="What are the safety requirements for an accountant?",
    )
    return parser.parse_args()


def require_ok(response: requests.Response, step_name: str) -> dict:
    if response.status_code >= 400:
        raise RuntimeError(
            f"{step_name} failed with status {response.status_code}: {response.text}"
        )
    try:
        return response.json()
    except ValueError as exc:
        raise RuntimeError(f"{step_name} did not return valid JSON: {response.text}") from exc


def main() -> None:
    args = parse_args()
    api_base = args.api_base.rstrip("/")
    n8n_base = args.n8n_base.rstrip("/")
    sample_file = Path(args.sample_file)

    if not sample_file.exists():
        raise FileNotFoundError(f"Sample file not found: {sample_file}")

    summary: dict[str, object] = {}

    health = require_ok(
        requests.get(f"{api_base}/health", timeout=15),
        "health",
    )
    summary["health"] = health

    with sample_file.open("rb") as file_handle:
        upload = require_ok(
            requests.post(
                f"{api_base}/documents/upload",
                data={"title": "Day 14 Smoke Test Document", "source": "manual"},
                files={
                    "file": (
                        sample_file.name,
                        file_handle,
                        "application/pdf",
                    )
                },
                timeout=60,
            ),
            "document upload",
        )

    document_id = upload["id"]
    summary["uploaded_document_id"] = document_id

    for step in ("process", "chunk", "index"):
        result = require_ok(
            requests.post(
                f"{api_base}/documents/{document_id}/{step}",
                timeout=240,
            ),
            f"document {step}",
        )
        summary[f"document_{step}"] = result["status"]

    search_result = require_ok(
        requests.post(
            f"{api_base}/search",
            json={"query": args.search_query, "limit": 3},
            timeout=120,
        ),
        "search",
    )
    summary["search_results"] = len(search_result.get("results", []))

    ask_result = require_ok(
        requests.post(
            f"{api_base}/ask",
            json={"question": args.ask_question, "limit": 3},
            timeout=180,
        ),
        "ask",
    )
    summary["ask_sources"] = len(ask_result.get("sources", []))

    agent_payloads = {
        "search": {"query": "найди требования по охране труда", "limit": 3},
        "ask": {"query": "какие требования по охране труда для бухгалтера?", "limit": 3},
        "action": {"query": "покажи документы", "limit": 5},
    }
    agent_summary: dict[str, dict[str, str]] = {}
    for name, payload in agent_payloads.items():
        result = require_ok(
            requests.post(
                f"{api_base}/agent/query",
                json=payload,
                timeout=120,
            ),
            f"agent route {name}",
        )
        agent_summary[name] = {
            "route": result["route"],
            "agent": result["agent"],
        }
    summary["agent_routes"] = agent_summary

    workflow_trigger = require_ok(
        requests.post(
            f"{api_base}/workflows/trigger",
            json={
                "workflow_name": "ingestion_reindex",
                "document_id": document_id,
            },
            timeout=240,
        ),
        "workflow trigger",
    )
    summary["workflow_trigger"] = workflow_trigger["status"]

    notification_webhook = require_ok(
        requests.post(
            f"{n8n_base}/webhook/notification-sync",
            json={
                "document_id": document_id,
                "status": "indexed",
                "message": "Day 14 smoke test notification",
            },
            timeout=60,
        ),
        "notification webhook",
    )
    summary["notification_workflow"] = notification_webhook["status"]

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
