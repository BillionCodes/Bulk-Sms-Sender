# Bulk Sms Sender

Bulk Sms sender is a desktop GUI Client for Sending SMS or text to a range of valid phones numbers using the email SMS Gateway service provided by textbelt. it is totally free!

## Installation

Clone this repository to install Bulk Sms sender.

```bash
> git clone https://github.com/BillionCodes/Bulk-Sms-Sender.git
> cd Bulk-Sms-Sender
> pip install -r requirements.txt
> python3 BulkSender.py
```

## Pre-requisite

You need to set up your server with this repository [textbelt](https://github.com/typpo/textbelt.git).
You can reach me on my [WhatsApp](https://api.whatsapp.com/send?phone=+2348139474542&text=Hello%20Josiah%2C%20%0AI%20am%20reaching%20out%20to%20you%20about%20your%20Bulk%20SMS%20Sender%20repo%20on%20GitHub%0AMy%20name%20is) for more details on how to setup your server on RDP/VPS

## Usage

Edit your BulkSender.py and on line 225, change url value to your server's address e.g

```python

url = #server url, default is http://localhost:9090/text
```

## Contributing

Special thanks to the team at [textbelt](textbelt.com) for making this possible. They guys inspired me.

## License

[MIT](https://choosealicense.com/licenses/mit/)
