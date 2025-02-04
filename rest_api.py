# import requests

# # Triton server URL
# url = "http://localhost:8000/v2/models/bert/infer"

# # Input text payload
# payload = {
#     "inputs": [
#         {
#             "name": "text_input",
#             "shape": [4],  # Batch size of 4
#             "datatype": "BYTES",
#             "data": [
#                 "What is your name?",
#                 "How is the weather today?",
#                 "Tell me about Triton server.",
#                 "hello"
#             ]
#         }
#     ],
#     "outputs": [
#         {
#             "name": "output"
#         }
#     ]
# }

# # Send request to Triton server
# response = requests.post(url, json=payload)

# # Parse response
# result = response.json()
# if "outputs" in result:
#     predicted_label = result["outputs"][0]["data"][0]
#     print("Predicted label:", predicted_label)
# else:
#     print("Error:", result.get("error", "Unknown error"))


import requests

# Triton server URL
url = "http://localhost:8000/v2/models/bert/infer"

# Batch input texts payload
payload = {
    "inputs": [
        {
            "name": "text_input",
            "shape": [4],  # Batch size of 4 (example)
            "datatype": "BYTES",  # Ensure this matches TYPE_STRING
            "data": [
                "What is your name?",
                "How is the weather today?",
                "Tell me about Triton server.",
                "hello"
            ]
        }
    ],
    "outputs": [
        {
            "name": "output"
        }
    ]
}

# Send request to Triton server
response = requests.post(url, json=payload)

# Parse response
result = response.json()
if "outputs" in result:
    # Extract batch results
    predicted_labels = result["outputs"][0]["data"]
    print("Predicted labels:")
    for i, label in enumerate(predicted_labels):
        print(f"Input {i + 1}: {label}")
else:
    print("Error:", result.get("error", "Unknown error"))

