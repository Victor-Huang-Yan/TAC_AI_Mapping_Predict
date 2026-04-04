"""Script to verify matching results

Check why "PnP Destroy" matches to "PnP Cleaning" instead of "PnP Scrap".
Uses the same calculation method as the application to compare semantic similarity and fuzzy matching scores.
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from fuzzywuzzy import fuzz

# 加载本地模型
print("Loading local model...")
model = SentenceTransformer('models/all-MiniLM-L6-v2')
print("Model loaded successfully!")

# 测试术语
input_term = "PnP Destroy"
target_terms = ["PnP Scrap", "PnP Cleaning"]

print(f"\nTesting matching for: '{input_term}'")
print("=" * 60)

# 计算输入术语的嵌入
input_embedding = model.encode(input_term)

# 计算每个目标术语的得分
for target_term in target_terms:
    # 计算语义相似度
    target_embedding = model.encode(target_term)
    semantic_similarity = np.dot(input_embedding, target_embedding) / \
                        (np.linalg.norm(input_embedding) * np.linalg.norm(target_embedding))
    semantic_score = semantic_similarity * 100
    
    # 计算模糊匹配得分
    fuzzy_score = fuzz.token_sort_ratio(input_term, target_term)
    
    # 计算加权平均得分（与应用中相同的权重）
    weighted_score = (semantic_score * 0.8 + fuzzy_score * 0.2)
    
    print(f"Target: '{target_term}'")
    print(f"  Semantic Score: {semantic_score:.2f}")
    print(f"  Fuzzy Score: {fuzzy_score:.2f}")
    print(f"  Weighted Score: {weighted_score:.2f}")
    print()

print("=" * 60)

# 分析结果
target_embeddings = model.encode(target_terms)
semantic_scores = []
fuzzy_scores = []
weighted_scores = []

for i, target_term in enumerate(target_terms):
    # 计算语义相似度
    semantic_similarity = np.dot(input_embedding, target_embeddings[i]) / \
                        (np.linalg.norm(input_embedding) * np.linalg.norm(target_embeddings[i]))
    semantic_score = semantic_similarity * 100
    semantic_scores.append(semantic_score)
    
    # 计算模糊匹配得分
    fuzzy_score = fuzz.token_sort_ratio(input_term, target_term)
    fuzzy_scores.append(fuzzy_score)
    
    # 计算加权平均得分
    weighted_score = (semantic_score * 0.8 + fuzzy_score * 0.2)
    weighted_scores.append(weighted_score)

# 找出最高分的术语
best_idx = weighted_scores.index(max(weighted_scores))
best_term = target_terms[best_idx]
best_score = weighted_scores[best_idx]

print(f"Best match: '{best_term}' with score: {best_score:.2f}")
print(f"Semantic score: {semantic_scores[best_idx]:.2f}")
print(f"Fuzzy score: {fuzzy_scores[best_idx]:.2f}")

# 分析为什么会这样
print("\nAnalysis:")
if best_term == "PnP Cleaning":
    print("The model considers 'PnP Destroy' more similar to 'PnP Cleaning' than 'PnP Scrap'.")
    print("This could be because:")
    print("1. The semantic representation of 'Destroy' is closer to 'Cleaning' than 'Scrap'")
    print("2. The fuzzy matching score might also be contributing to this result")
else:
    print("The model correctly identifies 'PnP Destroy' as more similar to 'PnP Scrap'.")

print("\nNote: This is based on the pre-trained all-MiniLM-L6-v2 model's understanding of these terms.")
print("For more accurate domain-specific matching, you might consider fine-tuning the model with domain-specific data.")