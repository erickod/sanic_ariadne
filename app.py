from random import randint
from asyncio import sleep

import ujson
from sanic import Sanic, HTTPResponse
from sanic.response import json
from ariadne import QueryType, graphql_sync, make_executable_schema, graphql
from ariadne.asgi import GraphQL
from ariadne.constants import PLAYGROUND_HTML

#import graphql_endpoints



type_defs = """
    type Query {
        hello: String!
    }
"""

query = QueryType()

@query.field("hello")
async def resolve_hello(_, info):
    v = randint(0, 5)
    await sleep(v)
    return f"Hello guest! It token {v} secconds..."


schema = make_executable_schema(type_defs, query)

app = Sanic(__name__)

@app.route("/graphql", methods=["GET"])
async def graphql_playground(request):
    return HTTPResponse(PLAYGROUND_HTML, 200)

@app.route("/graphql", methods=["POST"])
async def graphql_server(request):

    data = ujson.loads(request.body)
    success, result = await graphql(schema,
        data,
        context_value=None,
        debug=app.debug)


    return json(result)

if __name__ == '__main__':
    app.run()