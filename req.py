import requests
import json
from picamera import PiCamera
import requests
from time import sleep

# Örnek bir resim dosyasının yolu
image_path = './cam.jpg'

# POST isteği için endpoint URL'si
command_url = 'http://greenscan.pythonanywhere.com/capture'
camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()
sleep(2)
#TODO: implement camera and send picture in post request to webservice
def get_command():
    camera.capture('cam.jpg')
    sleep(0.4)
    with open(image_path, 'rb') as file:
        files = {'image': file}
        response = requests.post(url, files=files)
    # API'nin yanıtını kontrol et
    if response.status_code == 200:
        try:
            result = json.loads(response.text)
            print("Etiket: ", result['label'])
            first_char = str(result['label'][0])
            chars = ['G', 'H', 'P', 'A']
            for i in range(len(chars)):
                if first_char == chars[i]:
                    return i+1
        except Exception as e:
            print("Hata Oluştu: ",str(e))
    else:
        print("İstek başarısız. HTTP Hata Kodu:", response.status_code)

recycle_url = ''
def post_recycled(data):
    response = requests.post(recycle_url, data=data)
    print("Recycle response: ".format(response))
