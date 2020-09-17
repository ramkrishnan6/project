import os

import requests
import base64

from mysite import settings


def ocr(file_name):
    CLIENT_ID = "vrfPBXjhPibvuDv8XFtOg4LGMn3Kj9NeVZbPVGn"
    ENVIRONMENT_URL = "api.veryfi.com"

    username = "kopika6803"
    api_key = "19e0ed6b098a53f2c54ddaacf4e75e5c"
    process_image_url = 'https://{0}/api/v7/partner/documents/'.format(ENVIRONMENT_URL)
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "CLIENT-ID": CLIENT_ID,
        "AUTHORIZATION": "apikey {0}:{1}".format(username, api_key)
    }

    # file path and file name
    image_path = os.path.join(settings.BASE_DIR + '/media/', file_name)

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
    cost = int(response['total'])
    date = response['date'][0:10]

    transaction = [date, description, cost]

    return transaction
