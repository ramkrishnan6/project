import requests
import base64


def ocr(file_path, file_name):
    CLIENT_ID = "vrf7TkGKGp57XTD2Y52xSZu4ucih2ekwkWevYPG"
    ENVIRONMENT_URL = "api.veryfi.com"

    username = "checkproject55"
    api_key = "629d84bed7f8e07ccab045455c0c57f8"
    process_image_url = 'https://{0}/api/v7/partner/documents/'.format(ENVIRONMENT_URL)
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "CLIENT-ID": CLIENT_ID,
        "AUTHORIZATION": "apikey {0}:{1}".format(username, api_key)
    }

    # file path and file name
    image_path = "D:\KUSH_DATA\SCOE\BE\Sem 1\Project\Sem 2\project\media\\" + file_name
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
    cost = int(response['total'])
    date = response['date'][0:10]

    transaction = [date, description, cost]

    return transaction
