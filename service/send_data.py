import requests


def send_data(url,data):
    """Send data on server"""
    requests.post(url,data={'FIELD_NAME':data})
    