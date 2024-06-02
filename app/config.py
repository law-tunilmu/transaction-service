import midtransclient
import os
from dotenv import load_dotenv
from supabase.client import create_client

load_dotenv()



PRODUCTION = os.environ.get('PRODUCTION', False)

# async def supa_async() -> AsyncClient:
#     load_dotenv()
#     supa_client = AsyncClient(
#         os.environ['SUPABASE_URL'],
#         os.environ['SUPABASE_KEY']
#     )
#     if not os.environ.get('PRODUCTION', False):
#         supa_client.rest_url = os.environ['SUPABASE_URL']

#     return supa_client

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
    server_key=os.getenv('MIDTRANS_SERVER_KEY'),
    client_key=os.getenv('MIDTRANS_CLIENT_KEY')
)


