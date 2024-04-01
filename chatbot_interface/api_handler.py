import httpx

API_URL = "http://127.0.0.1:8000"

async def _api_interaction(url: str, method: str = 'get', data: dict = None):
    """Handles interaction with the API based on the method and data provided."""
    async with httpx.AsyncClient() as client:
        if method == 'post':
            response = await client.post(url, json=data)
        elif method == 'put':
            response = await client.put(url, json=data)
        elif method == 'delete':
            response = await client.delete(url)
        else:  # default to 'get'
            response = await client.get(url)

        response.raise_for_status()
        return response.json()

async def api_call(operation, message):
    if operation == "ADD":
        result = await _api_interaction(f"{API_URL}/items/", 'post', message.dict())
        result_message = "Item added successfully!"
    elif operation == "UPDATE":
        result = await _api_interaction(f"{API_URL}/items/{message}", 'put', message.dict())
        result_message = "Item updated successfully!"
    elif operation == "DELETE":
        await _api_interaction(f"{API_URL}/items/{message}", 'delete')
        result_message = "Item deleted successfully!"
    elif operation == "READ":
        item = await _api_interaction(f"{API_URL}/items/{message}")
        result_message = f"Item details: {item}"
    elif operation == "READ_ALL":
        items = await _api_interaction(f"{API_URL}/items/")
        result_message = f"All items: {items}"
    else:
        result_message = "Unrecognized command. Please use valid operations."
    return result_message