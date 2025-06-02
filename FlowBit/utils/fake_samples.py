from faker import Faker
import json
import os

def generate_webhook_data():
    fake = Faker()
    webhook_data = {
        "event_id": fake.uuid4(),
        "event_type": fake.random_element(elements=[
            "order_created", "order_updated", "payment_received", "shipment_sent"
        ]),
        "timestamp": fake.iso8601(),
        "customer": {
            "id": fake.uuid4(),
            "name": fake.name(),
            "email": fake.email(),
            "address": fake.address().replace("\n", ", ")
        },
        "order": {
            "order_id": fake.uuid4(),
            "amount": round(fake.pyfloat(left_digits=4, right_digits=2, positive=True), 2),
            "currency": "USD",
            "items": [
                {
                    "item_id": fake.uuid4(),
                    "product_name": fake.word(),
                    "quantity": fake.random_int(min=1, max=5),
                    "price": round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2)
                } for _ in range(fake.random_int(min=1, max=3))
            ]
        },
        "status": fake.random_element(elements=["pending", "completed", "cancelled"])
    }
    return webhook_data
def save_webhook_sample(data, folder="sample_data", filename="webhook_sample.json"):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Sample webhook data saved to {filepath}")

if __name__ == "__main__":
    sample = generate_webhook_data()
    save_webhook_sample(sample)

