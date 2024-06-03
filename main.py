from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from starlette.responses import JSONResponse
import uvicorn

from app.models import SnapTransaction, User, UserCart
from app.config import PRODUCTION, snap, create_supabase_client
from app.utils import verify_signature
from datetime import datetime

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
CART_TABLE_NAME = 'cart'
COURSE_OWNED_TABLE_NAME = 'course_owned'

supabase_client = create_supabase_client()

@app.get(
    "cart/",
    description="Get user cart"
)
def get_cart(user: User):
    try:
        query = supabase_client.table('cart').select('course_id').eq('email', user.email).execute()
    except supabase.PostgrestAPIError as e:
        print(e)
        return JSONResponse({"message": "Postgres Error"}, status_code=500)
    
    return {"courses_in_cart": query.data}

@app.post(
    "cart/add",
    description="Add course to user cart"
)
def add_course_to_cart(cart: UserCart):
    try:
        query = supabase_client.table('cart').insert(cart.model_dump()).execute()
    except supabase.PostgrestAPIError as e:
        print(e)
        return JSONResponse({"message": "Postgres Error"}, status_code=500)
    
    return {"course_added": query.data}

@app.delete(
    "cart/remove",
    description="Remove course from user cart"
)
def remove_course_from_cart(cart: UserCart):
    try:
        query = supabase_client.table('cart').delete().eq('email', cart.email).eq('course_id', cart.course_id).execute()
    except supabase.PostgrestAPIError as e:
        print(e)
        return JSONResponse({"message": "Postgres Error"}, status_code=500)
    
    return {"course_deleted": query.data}

@app.delete(
    "cart/remove_all",
    description="Empty user cart"
)
def empty_cart(user: User):
    try:
        query = supabase_client.table('cart').delete().eq('email', user.email).execute()
    except supabase.PostgrestAPIError as e:
        print(e)
        return JSONResponse({"message": "Postgres Error"}, status_code=500)
    
    return {"courses_deleted": query.data}

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
        "status": "pending",
        "date_created": datetime.now(),
        "course_ids": [t["id"] for t in transaction["item_details"]]
    }
    try:
        supabase_client.table(TRANSACTION_TABLE_NAME) \
                    .insert(transactionInDB).execute()
        
        return JSONResponse(transaction_response)
    except supabase.PostgrestAPIError as e:
        print(e)
        return JSONResponse({"message": "Postgres Error"}, status_code=500)
    



@app.post(
    "transaction/midtrans-notification", 
    description="Handle incoming notification from midtrans"
)
async def handle_notification(request: Request):
    # Parse the request body as JSON
    notification_data = await request.json()

    is_valid = verify_signature(notification_data)

    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid notification signature")

    transaction_id = notification_data["order_id"]
    transaction_status = notification_data["transaction_status"]
    updates = {"status": transaction_status}

    # Update your database or perform actions based on the transaction status
    if transaction_status == "capture" or transaction_status == "settlement":
        updates["date_paid"] = datetime.now()
        try:
            query = supabase_client.table(TRANSACTION_TABLE_NAME) \
                .select("email, course_ids") \
                .eq("order_id", transaction_id) \
                .execute()
        except supabase.PostgrestAPIError as e:
            print("Retrieve data error at Handling Notification")  
            return JSONResponse({"message":"Internal server error"}, status_code=500)
        
        email = query.data["email"]
        course_ids = query.data["course_ids"]
        new_courses = [{"email": email, "course_id": course_id} for course_id in course_ids]
        try:
            supabase_client.table(COURSE_OWNED_TABLE_NAME) \
                .insert(new_courses) \
                .eq(order_id=transaction_id) \
                .execute()
            return {"message": "Notification received successfully"}

        except supabase.PostgrestAPIError as e:
            print("Update data Error at Handling Notification")  
            return JSONResponse({"message":"Internal server error"}, status_code=500)


    try:
        supabase_client.table(TRANSACTION_TABLE_NAME) \
            .update(updates) \
            .eq(order_id=transaction_id) \
            .execute()
        return {"message": "Notification received successfully"}

    except supabase.PostgrestAPIError as e:
        print("Update data Error at Handling Notification")  
        return JSONResponse({"message":"Internal server error"}, status_code=500)


@app.get(
    "/course/owned", 
    description="""Get list of owned courses"""
)
def get_transaction_status(user: User):
    try:
        query = supabase_client.table(COURSE_OWNED_TABLE_NAME) \
                    .select("*").eq('email', user.email).execute()
    except supabase.PostgrestAPIError as e:
        print(e)
        return JSONResponse({"message": "Error Acquiring Data"}, status_code=500)
    return JSONResponse({"course_list":query.data})


@app.get(
    "/transaction/status/{order_id}", 
    description="""Get detail of a transaction"""
)
def get_transaction_status(order_id: str):
    try:
        query = supabase_client.table(TRANSACTION_TABLE_NAME) \
                    .select("*").eq('order_id', order_id).execute()
    except supabase.PostgrestAPIError as e:
        print(e)
        return JSONResponse({"message": "Error Acquiring Data"}, status_code=500)
    return JSONResponse({"transaction_status":query.data})



@app.get(
    "/transaction/status/", 
    description="""Get all transaction made by user"""
)
def get_all_transaction(user: User):
    try:
        query = supabase_client.table(TRANSACTION_TABLE_NAME) \
                    .select("*").eq('email', user.email).execute()
    except supabase.PostgrestAPIError as e:
        print(e)
        return JSONResponse({"message": "Error Acquiring Data"}, status_code=500)
    
    return JSONResponse({"transaction_list":query.data})

if (not PRODUCTION) and (__name__ == "__main__"):
    uvicorn.run("main:app", port=8888, log_level="info")

