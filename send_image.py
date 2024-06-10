import requests
import base64

def send_image(file_path, server_url):
    with open(file_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        params = {
            "api_key": "IW2EMzEFoRss1ULjETA2"
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.post(server_url, data=encoded_image, params=params, headers=headers)

        if response.status_code == 200:
            return response
        else:
            return None
