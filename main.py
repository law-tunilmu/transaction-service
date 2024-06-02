from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from starlette.responses import JSONResponse
import uvicorn

from app.models import SnapTransaction
from app.config import snap, create_supabase_client


import supabase

app = FastAPI()
app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000","*"],
        allow_credentials=True,
        allow_methods=["*"], 
        allow_headers=["*"], 
    )



TRANSACTION_TABLE_NAME = 'transaction'
supabase_client = create_supabase_client()

@app.post(
    "/transaction/confirm", 
    description="""Make transaction and will be returned a token to be used in pay button"""
)
def confirm_transaction(transaction_info: SnapTransaction):
    transaction = transaction_info.model_dump()
    try:
        transaction_response = snap.create_transaction(transaction)
    except Exception as e:
        return JSONResponse(e.message, status_code=500)
    transactionInDB = {
        "order_id": transaction["transaction_details"]["order_id"],
        "gross_amount": transaction["transaction_details"]["gross_amount"],
        "email": transaction["customer_details"]["email"],
        "status": "Unpaid",
    }
    try:
        supabase_client.table(TRANSACTION_TABLE_NAME) \
                    .insert(transactionInDB).execute()
        
        return JSONResponse(transaction_response)
    except supabase.PostgrestAPIError as e:
        print(e)
        return JSONResponse({"message": "Postgres Error"}, status_code=500)
    


@app.get(
    "/transaction/status/{order_id}", 
    description="""Make transaction and will be returned a token to be used in pay button"""
)
def get_transaction_status(order_id: str):
    status_response = snap.transactions.status(order_id)
    
    return JSONResponse(status_response)
    

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info", reload=True)

