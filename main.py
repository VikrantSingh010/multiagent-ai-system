from orchestrator.process_input import process_input
from core.shared_memory import shared_memory
import json

def print_result(result, title="RESULT"):
    print(f"\n=== {title} ===")
    print(json.dumps(result, indent=2))
    print()

if __name__ == "__main__":
    # test_json = {
    #     "invoice_id": "INV-2024-001",
    #     "customer": "Tech Corp",
    #     "amount": 15000,
    #     "items": ["Laptops", "Monitors", "Keyboards"]
    # }
    
    # result = process_input(json.dumps(test_json), clear_memory=True)
    # print_result(result, "JSON PROCESSING")

    # # Sample JSON
    # with open("examples/sample.json") as f:
    #     js = json.load(f)
    # result = process_input(json.dumps(js), clear_memory=True)
    # print_result(result, "JSON PROCESSING")

    # Sample PDF
    # try:
    #     with open("examples/regulation.pdf", "rb") as f:
    #         pdf_bytes = f.read()
    #     result = process_input(pdf_bytes, clear_memory=True)
    #     print_result(result, "PDF PROCESSING")
    # except FileNotFoundError:
    #     print("PDF file not found.")


    test_email = """
    From: customer@example.com
    Subject: Product Complaint - Urgent

    Dear Support Team,

    I recently purchased a laptop from your store (order ID: 45321). 
    The screen started flickering within 3 days of use. This is unacceptable for a new product.

    Please resolve this issue urgently.

    Regards,
    John Doe
    """
    
    result = process_input(test_email, clear_memory=True)
    print_result(result, "EMAIL PROCESSING")