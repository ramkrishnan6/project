import requests
import base64
import datetime


def ocr(file_path, file_name):
    CLIENT_ID = "vrfD4T07rmVSSo23MhPSTsRAF9i7U38U2vSldo1"
    ENVIRONMENT_URL = "api.veryfi.com"

    username = "ikrishnanram"
    api_key = "360e184691d26160a4e35aae13078464"
    process_image_url = 'https://{0}/api/v7/partner/documents/'.format(ENVIRONMENT_URL)
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "CLIENT-ID": CLIENT_ID,
        "AUTHORIZATION": "apikey {0}:{1}".format(username, api_key)
    }

    # file path and file name
    image_path = "/home/ram/mysite/media/" + file_name
    file_name = file_name

    # convert image to Base64
    with open(image_path, "rb") as image_file:
        base64_encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    categories = ["Automobile", "Bank Transfer", "Cash Withdrawal", "Education", "Entertainment",
                  "Fine", "Food", "Health", "Other", "Paytm", "Recharge", "Shopping", "Travel", "UPI"
                  ]
    payload = {
        'file_name': file_name,
        'file_data': base64_encoded_string,
        'categories': categories
    }
    response = requests.post(url=process_image_url, headers=headers, json=payload).json()

    description = response['vendor']['name']
    cost = response['total']
    date = response['date']

    date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').date()
    transaction = [date, description, cost]

    return transaction
