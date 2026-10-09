import os
# 1. Point to your new custom folder location
os.environ["HF_HOME"] = "G:/HuggingFace"
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("BAAI/bge-small-en-v1.5")

# The chunk that SHOULD answer the question
chunk = "Notes: Fix confirmed in build v0.9.1. Icon now correctly gated behind product page navigation. Regression test passed."

# Five different ways of asking the same thing
questions = [
    "What should a tester verify after the fix in build v0.9.1?",
    "Was the chatbot icon bug fixed?",
    "regression test v0.9.1 result",
    "icon fix confirmed",
    "Fix confirmed build v0.9.1",
]

chunk_vec = model.encode([chunk], normalize_embeddings=True)

for q in questions:
    q_vec = model.encode([q], normalize_embeddings=True)
    diff = chunk_vec[0] - q_vec[0]
    dist = np.sqrt(np.dot(diff, diff))
    print(f"{dist:.4f}  |  {q}")