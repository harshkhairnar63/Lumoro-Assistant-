import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

async def main():
    client = MultiServerMCPClient(
        {
            "filesystem" : {
                "command" : "npx",
                "args" : ["@modelcontextprotocol/server-filesystem",
                    "C:/Users/HARSHWARDHAN KHAIRNA/Documents"],
                "transport" : "stdio"
            }
        }
    )
    tools = await client.get_tools()

    print("Tools found")
    for tool in tools:
        print(tools)

asyncio.run(main())