from orchestrator.process_input import process_input
from core.shared_memory import shared_memory
import json
import sys
print("Using Python from:", sys.executable)



def print_result(result, title="RESULT"):
    print(f"\n=== {title} ===")
    print(json.dumps(result, indent=2))
    print()

if __name__ == "__main__":
#     test_json = {
#   "sender": "john@example.com",
#   "subject": "Order Request",
#   "body": "Please send 10 laptops and monitors.",
#   "date": "-2024-06-01"
# }

    
#     result = process_input(json.dumps(test_json), clear_memory=True)
#     print_result(result, "JSON PROCESSING")

    # # Sample JSON
    # with open("examples/sample_inputs/sample.json") as f:
    #     js = json.load(f)
    # result = process_input(json.dumps(js), clear_memory=True)
    # print_result(result, "JSON PROCESSING")

    # Sample PDF
    try:
        with open("examples/sample_inputs/sample.pdf", "rb") as f:
            pdf_bytes = f.read()
        result = process_input(pdf_bytes, clear_memory=True)
        print_result(result, "PDF PROCESSING")
    except FileNotFoundError:
        print("PDF file not found.")


#     test_email = """From: procurement@glotechindustries.com  
# To: sales@vendorcorp.com  
# Subject: RFQ for Industrial Sensors  

# Dear VendorCorp Team,

# We are looking to procure 500 units of industrial-grade temperature sensors (model TS-500) for our upcoming IoT deployment. Please provide a detailed quotation including:

# - Unit price
# - Delivery timelines
# - Warranty details
# - Bulk order discount options

# Required delivery: Q3 2025  
# Budget Approval ID: BUDG-8493-ZXA

# Looking forward to your prompt response.

# Best regards,  
# Rakesh Mehra  
# Senior Procurement Officer  
# GloTech Industries

    
#     """
    
#     result = process_input(test_email, clear_memory=True)
#     print_result(result, "EMAIL PROCESSING")