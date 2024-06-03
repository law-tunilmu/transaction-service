import midtransclient
import os
from dotenv import load_dotenv
from supabase.client import create_client
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType


load_dotenv()



PRODUCTION = os.environ.get('PRODUCTION', False)
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
MIDTRANS_SERVER_KEY = os.environ.get('MIDTRANS_SERVER_KEY')
MIDTRANS_CLIENT_KEY = os.environ.get('MIDTRANS_CLIENT_KEY')

conf = ConnectionConfig(
    MAIL_USERNAME = "Tunilmu",
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD"),
    MAIL_FROM = os.environ.get("MAIL_USER"),
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
)

def create_supabase_client():
    load_dotenv()
    supa_client = create_client(
        os.environ['SUPABASE_URL'],
        os.environ['SUPABASE_KEY']
    )
    # if not os.environ.get('PRODUCTION', False):
    #     supa_client.rest_url = os.environ['SUPABASE_URL']

    return supa_client

# Create Core API instance

snap = midtransclient.Snap(
    is_production=False,
    server_key=MIDTRANS_SERVER_KEY,
    client_key=MIDTRANS_CLIENT_KEY
)


