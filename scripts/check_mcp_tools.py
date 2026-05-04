from pathlib import Path
import sys
import anyio


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from mcp import types
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamable_http_client


MCP_URL = "http://127.0.0.1:8000/mcp"


def format_tool(tool: types.Tool) -> str:
    return f"- {tool.name}: {tool.description or 'no description'}"


def format_resource(resource: types.Resource) -> str:
    return f"- {resource.name}: {resource.uri}"


def format_prompt(prompt: types.Prompt) -> str:
    return f"- {prompt.name}: {prompt.description or 'no description'}"


async def main() -> None:
    async with streamable_http_client(MCP_URL) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            init_result = await session.initialize()
            print("Connected to MCP server")
            print(
                "Server:",
                f"{init_result.serverInfo.name} {init_result.serverInfo.version}",
            )

            tools_result = await session.list_tools()
            resources_result = await session.list_resources()
            prompts_result = await session.list_prompts()

            print("\nTools")
            for tool in tools_result.tools:
                print(format_tool(tool))

            print("\nResources")
            for resource in resources_result.resources:
                print(format_resource(resource))

            print("\nPrompts")
            for prompt in prompts_result.prompts:
                print(format_prompt(prompt))


if __name__ == "__main__":
    anyio.run(main)
