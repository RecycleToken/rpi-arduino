## THIS FILE IS USED TO TEST THE ROBOFLOW API WITHOUT THE NEED OF A RASPBERRY PI
import json
from time import sleep
import send_image

# Örnek bir resim dosyasının yolu
image_path = 'battery.jpg'

# POST isteği için endpoint URL'si
command_url = 'https://classify.roboflow.com/waste-detection-yljc0/1'
trash_url = 'https://detect.roboflow.com/yolov5-garbage-detection/1'


def get_command():
    trash_response = send_image.send_image(image_path, trash_url)

    if trash_response is None:
        return None
    elif trash_response.status_code == 200:
        try:
            print(json.dumps(trash_response.json(), indent=4))
            trash_result = json.loads(trash_response.text)
            if(len(trash_result['predictions']) == 0):
                print("No predictions from trash API")
                return 0
            trash_label = trash_result['predictions'][0]['class']
            if trash_label == "trash":
                print("Trash: Exiting...")
                return 0
            elif trash_label == "not trash":
                print("Not Trash: Continue...")
        except Exception as e:
            print(e)
            return

    response = send_image.send_image(image_path, command_url)
    if response is None: #TODO: Add error handling
        return None
    elif response.status_code == 200:
        try:
            result = json.loads(response.text)
            if len(result['predicted_classes']) == 0:
                return 0
            print("Etiket: ", result['predicted_classes'][0])
            predicted_class = str(result['predicted_classes'][0])

            return predicted_class
        except Exception as e:
            print("Hata Olustu: ",str(e))
            return 0
    else:
        print("Istek basarisiz. HTTP Hata Kodu:", response.status_code)
        return 0
