# Script Usage Guide

This script was created for personal use to track items on BestBuy, especially for pre-order items. Unlike other tracking sites that may refresh too slowly (e.g., 1-minute intervals) or fail to notify you quickly when an item becomes available, this script ensures you stay updated in real-time. Best of all, you no longer need to register your personal information on third-party websites!

Feel free to use it for your own needs!

---

## Prerequisites

To use this script, you will need to provide the following parameters:

### 1. `Product ID(s)`
The Product ID can be obtained from the BestBuy website. Follow these steps to find it:

1. Search for the desired item on the [BestBuy Canada website](https://www.bestbuy.ca).
2. Navigate to the product page. For example: "https://www.bestbuy.ca/en-ca/product/nvidia-geforce-rtx-5090-32gb-gddr7-video-card/18931348"
3. The Product ID is the number at the end of the URL after the last forward slash (`/`). In the example above, the Product ID is `18931348`.

### 2. `toEmail`
This is the email address that will receive the notification email.

### 3. `fromEmail`
This is your Gmail address that will be used to log in to Gmail and send the notification email. **Note:** This must be a Gmail account.

### 4. `fromPassword`
This is the app password required to access your Gmail account and send the email. To generate an app password:

1. Ensure that 2-Factor Authentication (2FA) is enabled on your Gmail account.
2. Follow the instructions in [Google's App Password Guide](https://support.google.com/accounts/answer/185833?hl=en) to generate an app password.

### 5. `monitorFrequencyInSec`
This parameter determines how frequently the script checks for updates on BestBuy. By default, it is set to **30 seconds**. You can adjust this value to make the checks more or less frequent.

### 6. `logging`
If set to `true`, the script will log informational messages during its run, such as when an item becomes available or when an email is sent. Error logs will always be logged and are not affected by this setting.

---

## How to Use

1. Fill in the 4 required parameters (`Product ID`, `toEmail`, `fromEmail`, and `fromPassword`) in the `main()` function call within the script.
2. Optionally, adjust the `monitorFrequencyInSec` value to your preferred frequency.
3. Optionally, set `logging` to `true` if you want to enable informational logging.
4. Run the script using the following command:
```bash
python "BB Stock Monitor & Email Alert.py"


# Example of filling in the parameters in the main() function
def main():
    #18931348 - 5090 FE
    startMonitoring([18931348], "test@gmail.com", "test@gmail.com", "your app password", monitorFrequencyInSec=30, logging=True)
