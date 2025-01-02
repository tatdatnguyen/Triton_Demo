import triton_python_backend_utils as pb_utils
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import numpy as np

class TritonPythonModel:
    def initialize(self, args):
        """
        Initialize the model. This function is called once when the model is loaded.
        """
        # Load the tokenizer and model
        model_path = "google-bert/bert-base-uncased"  # Use your Hugging Face model path
        self.tokenizer = BertTokenizer.from_pretrained(model_path)
        self.model = BertForSequenceClassification.from_pretrained(model_path)
        self.model.eval()

        # Define label mapping
        self.labels = {0: "Negative sentiment", 1: "Positive sentiment"}

    def execute(self, requests):
        """
        Process inference requests.
        """
        responses = []
        for request in requests:
            # Extract text input
            text_input = pb_utils.get_input_tensor_by_name(request, "text_input").as_numpy()
            text_input = [t.decode("utf-8") for t in text_input.flatten()]
            print("Received text_input:", text_input)
            # Preprocess: Tokenize text
            tokens = self.tokenizer(
                text_input,
                max_length=128,
                truncation=True,
                padding="max_length",
                return_tensors="pt"
            )

            # Perform inference
            with torch.no_grad():
                outputs = self.model(**tokens)
                logits = outputs.logits
                predicted_classes = torch.argmax(logits, dim=1).tolist()

            # Postprocess: Map class indices to labels
            predicted_labels = [self.labels[cls] for cls in predicted_classes]

            # Create output tensor
            output_tensor = pb_utils.Tensor(
                "output",
                np.array(predicted_labels, dtype=object)
            )
            responses.append(pb_utils.InferenceResponse(output_tensors=[output_tensor]))

        return responses

    def finalize(self):
        """
        Clean up resources. This function is called when the model is unloaded.
        """
        print("Cleaning up Triton Python model resources...")
