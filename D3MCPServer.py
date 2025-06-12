from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.responses import Response
import uvicorn
import d3py


mcpserver=FastMCP(name='D3 command fetcher') # handle session
sse_transport=SseServerTransport('/messages/') # handle io(sse,post)

@mcpserver.tool(name='fetch',description='Returns D3 server command content')
async def fetch_command(command: str):
    print('fetching....')
    d3py.logoff()
    d3py.logon("localhost", "dm", "", "mvdemo", "")
    response = d3py.run(command,True)
    print("response from d3py:",response)
    return response
    

async def sse_handler(request):
    async with sse_transport.connect_sse(request.scope,request.receive,request._send) as streams:
        # keep sse session
        await mcpserver._mcp_server.run(streams[0],streams[1],mcpserver._mcp_server.create_initialization_options()) 
    return Response(status_code=204)  # 204 No Content

app=Starlette(
    debug=True,
    routes=[
        Route('/sse',endpoint=sse_handler),
        Mount('/messages/',app=sse_transport.handle_post_message)
    ]
)
uvicorn.run(app,host='0.0.0.0',port=8000)