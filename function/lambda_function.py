import logging
import boto3
import stripe
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

domain = "http://localhost:1313"
client = boto3.client("secretsmanager")
keys = json.loads(
    client.get_secret_value(
        SecretId="arn:aws:secretsmanager:us-east-1:148633485533:secret:dev/msp/stripe-KxWNIM",
    )["SecretString"]
)


def lambda_handler(event, context):
    try:
        stripe.api_key = keys["stripe-secret"]
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": 2000,
                        "product_data": {
                            "name": "Stubborn Attachments",
                            "images": ["https://i.imgur.com/EHyR2nP.png"],
                        },
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=domain + "/#coach",
            cancel_url=domain + "/#about",
        )
        return json.dumps({"id": checkout_session.id})
    except Exception as e:
        return json.dumps({"error": str(e), "response": "403"})
