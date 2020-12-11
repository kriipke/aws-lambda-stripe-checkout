import os
import logging
import boto3
import stripe
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client("secretsmanager")
keys = json.loads(
    client.get_secret_value(
        SecretId = os.environ["SECRET_ARN"],
    )["SecretString"]
)

def lambda_handler(event, context):
    try:
        stripe.api_key = keys[os.environ["SECRET_DICT_KEY"]]
        price_id = event['queryStringParameters'][os.environ["QUERY_PARAM"]]

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                  "price": "price_" + price_id,
                  "quantity": 1,
                },
            ],
            mode="payment",
            success_url= os.environ['DOMAIN'] + os.environ['SUCCESS_PAGE'],
            cancel_url= os.environ['DOMAIN'] + os.environ['CANCEL_PAGE'],
        )
        return {"id": checkout_session.id}
    except Exception as e:
        return {"error": str(e), "response": "403"}
