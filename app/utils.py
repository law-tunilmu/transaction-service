import hmac
import hashlib
from app.config import MIDTRANS_SERVER_KEY
# verify incoming notifications
def verify_signature(notification_data):

    signature = notification_data.get("signature")
    order_id = notification_data.get("transaction_details", {}).get("order_id")

    # Create the data string to be signed
    data = f"{order_id}{notification_data['status']}{notification_data['gross_amount']}{MIDTRANS_SERVER_KEY}"
    hashed_data = hmac.new(MIDTRANS_SERVER_KEY.encode("utf-8"), data.encode("utf-8"), hashlib.sha512).hexdigest()

    return hashed_data == signature