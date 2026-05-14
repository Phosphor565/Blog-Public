import azure.functions as func
import azure.durable_functions as df
import requests

myApp = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# HTTP-triggered starter for the durable orchestrator.
# Expects a JSON body like: { "urls": ["https://example.com", "https://contoso.com"\] }
@myApp.route(route="orchestrators/{functionName}")
@myApp.durable_client_input(client_name="client")
async def http_start(req: func.HttpRequest, client):
    function_name = req.route_params.get('functionName')
    try:
        body = req.get_json()
    except ValueError:
        body = {}

    urls = body.get("urls") or []
    if not isinstance(urls, list):
        urls = []

    instance_id = await client.start_new(function_name, client_input={"urls": urls})
    response = client.create_check_status_response(req, instance_id)
    return response

# Orchestrator that iterates through a list of URLs and delegates reachability checks to an activity.
@myApp.orchestration_trigger(context_name="context")
def check_urls_orchestrator(context):
    input_data = context.get_input() or {}
    urls = input_data.get("urls") or []
    results = []

    for url in urls:
        result = yield context.call_activity("check_url", url)
        results.append(result)

    return results

# Activity that performs a simple HTTP request to determine whether the URL is reachable.
@myApp.activity_trigger(input_name="url")
def check_url(url: str):
    try:
        response = requests.get(url, timeout=10)
        reachable = response.status_code < 400
        status = "available" if reachable else "not available"
        return {"url": url, "available": reachable, "status": status, "status_code": response.status_code}
    except requests.RequestException:
        return {"url": url, "available": False, "status": "not available"}
