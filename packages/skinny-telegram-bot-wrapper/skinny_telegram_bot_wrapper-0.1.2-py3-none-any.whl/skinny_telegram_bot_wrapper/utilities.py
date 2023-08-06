def get_base_url(host, port):
    return f"{host}:{port}"
def get_listening_endpoint(token: str):
    return f"/telegram/{token}"
def get_listening_url(base_url, listening_endpoint):
    return f"{base_url}{listening_endpoint}"
