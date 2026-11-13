from src.agent import app

print("\n--- TEST 1: A question IN the document ---")
inputs_1 = {"question": "How many days can I work remotely?", "tenant_id": "acme_corp", "retry_count": 0}
for output in app.stream(inputs_1):
    for key, value in output.items():
        if "generation" in value:
            print(f"ANSWER: {value['generation']}")

print("\n--- TEST 2: A question NOT in the document (Hallucination Test) ---")
inputs_2 = {"question": "What is the CEO's salary?", "tenant_id": "acme_corp", "retry_count": 0}
for output in app.stream(inputs_2):
    for key, value in output.items():
        if "generation" in value:
            print(f"ANSWER: {value['generation']}")

print("\n--- TEST 3: A different tenant trying to read ACME's document (Security Test) ---")
inputs_3 = {"question": "How many days can I work remotely?", "tenant_id": "evil_corp", "retry_count": 0}
for output in app.stream(inputs_3):
    for key, value in output.items():
        if "generation" in value:
            print(f"ANSWER: {value['generation']}")