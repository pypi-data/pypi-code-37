from __future__ import print_function
import cv2
import jsonpickle
import requests


class ConnectionError(Exception):
    pass


def ImageSender(image, host="0.0.0.0", port= 5000, endpoint="/api/image"):
    # type: (np.array, str, int, str) -> dict
    """Utility function to send numpy image to api endpoint

    :param image: Image in the format of a uint8 numpy array
    :param host: Remote IP address
    :param port: Remote address port
    :param endpoint: The api endpoint set in the image receiver
    :return: Response dictionary containing endpoint response
    """
    headers = {'content-type': 'image/jpeg'}
    post_url = "http://{}:{}{}".format(host, port, endpoint)
    _, img_encoded = cv2.imencode('.jpg', image)
    try:
        post_response = requests.post(post_url, data=img_encoded.tostring(), headers=headers)
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError(e)
    return jsonpickle.decode(post_response.text)


if __name__ == '__main__':
    from timeit import default_timer as timer

    while True:
        start = timer()
        img = cv2.imread('test.png')
        response = ImageSender(img)
        print("Response received in {:.2f} ms:".format((timer() - start) * 1000), response)
