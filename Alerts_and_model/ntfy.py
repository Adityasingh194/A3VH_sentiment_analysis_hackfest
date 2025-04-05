import requests
def notification(data):
    requests.post(
        f"https://ntfy.sh/PU0i7LMA0UhBi7fZ",
        data=data.encode(encoding='utf-8'))
    
# notification("HELLO")