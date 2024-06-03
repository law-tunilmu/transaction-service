import hashlib
from app.config import MIDTRANS_SERVER_KEY
# verify incoming notifications
def verify_signature(notification_data):

    signature = notification_data.get("signature_key")
    order_id = notification_data.get("order_id")
    status_code = notification_data.get("status_code")
    gross_amount = notification_data.get("gross_amount")


    # Create the data string to be signed
    data = f"{order_id}{status_code}{gross_amount}{MIDTRANS_SERVER_KEY}"

    sha512_hash = hashlib.sha512()

    # Update the hash object with the string
    sha512_hash.update(data.encode())

    # Get the hexadecimal representation of the hash
    hex_hash = sha512_hash.hexdigest()
    return hex_hash == signature