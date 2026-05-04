from pathlib import Path
import json
import sys

import anyio


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamable_http_client


MCP_URL = "http://127.0.0.1:8000/mcp"


def build_arguments() -> dict:
    query = " ".join(sys.argv[1:]).strip() or "enterprise ai assistant"
    return {
        "query": query,
        "limit": 3,
    }


async def main() -> None:
    arguments = build_arguments()

    async with streamable_http_client(MCP_URL) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool(
                "search_documents",
                arguments=arguments,
            )

            print("Called tool: search_documents")
            print("Arguments:")
            print(json.dumps(arguments, ensure_ascii=False, indent=2))
            print("\nResult flags:")
            print(json.dumps({"isError": result.isError}, ensure_ascii=False, indent=2))
            print("\nStructured content:")
            print(json.dumps(result.structuredContent, ensure_ascii=False, indent=2))
            print("\nContent:")
            print(
                json.dumps(
                    [item.model_dump(mode="json") for item in result.content],
                    ensure_ascii=False,
                    indent=2,
                )
            )


if __name__ == "__main__":
    anyio.run(main)
