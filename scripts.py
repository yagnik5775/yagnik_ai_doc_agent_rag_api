import json
import numpy as np

# Generate a random 384-dimensional vector
dummy_vector = np.random.rand(384).tolist()

# Create the payload dictionary
payload = {
    "query_vector": dummy_vector,
    "top_k": 5
}

# Print as pretty JSON
print(json.dumps(payload, indent=2))
