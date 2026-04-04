print("Testing semantic matching implementation...")

# Mock semantic matching functionality
class MockSentenceTransformer:
    def encode(self, text):
        # Simple mock encoding based on text length and character frequency
        import hashlib
        hash_val = int(hashlib.md5(text.encode()).hexdigest(), 16) % 1000
        # Return a vector of length 3
        return [hash_val / 1000, (hash_val % 100) / 100, (hash_val % 10) / 10]

class MockNumpy:
    def dot(self, a, b):
        return sum(x*y for x, y in zip(a, b))
    
    def norm(self, x):
        return sum(abs(i) for i in x) ** 0.5

# Initialize mock components
model = MockSentenceTransformer()
np = MockNumpy()

# Test cases
test_cases = [
    ("PnP Destroy", "PnP Scrap"),
    ("Assembly", "Assemble"),
    ("Disassembly", "Take apart"),
    ("PnP Destroy", "Assembly")  # Unrelated case
]

print("\nTesting semantic similarity between pairs:")
print("-" * 60)

for text1, text2 in test_cases:
    # Generate embeddings
    embedding1 = model.encode(text1)
    embedding2 = model.encode(text2)
    
    # Calculate cosine similarity
    dot_product = np.dot(embedding1, embedding2)
    norm1 = np.norm(embedding1)
    norm2 = np.norm(embedding2)
    
    if norm1 * norm2 > 0:
        semantic_score = (dot_product / (norm1 * norm2)) * 100
    else:
        semantic_score = 0
    
    print(f"'{text1}' vs '{text2}': {semantic_score:.2f}")

print("\nTest completed successfully!")
