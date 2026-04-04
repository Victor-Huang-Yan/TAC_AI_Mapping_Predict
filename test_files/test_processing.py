print("Testing processing logic with semantic matching...")

import pandas as pd
import os
from fuzzywuzzy import fuzz
from datetime import datetime

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
use_semantic_matching = True

# 创建测试数据
def create_test_data():
    # 创建主数据集
    master_data = {
        'MATERIAL_NAME': ['MATERIAL_NAME', 'MATERIAL_A'],
        'SUB_MATERIAL_NAME': ['PnP Scrap', 'Assembly'],
        'UOM': ['EA', 'PC'],
        'TRANSACTION_TYPE': ['ADJUSTMENT', 'ORDERS'],
        'IMLUI_Billable Date': ['2024-01-01', '2024-01-01'],
        'IMLUI_Billable Qty': [10, 5],
        'IMLUI_Document ID': ['DOC-001', 'DOC-002']
    }
    
    # 创建用户数据集
    user_data = {
        'MATERIAL_NAME': ['MATERIAL_NAME', 'MATERIAL_A'],
        'SUB_MATERIAL_NAME': ['PnP Destroy', 'Assemble'],
        'UOM': ['EA', 'PC'],
        'TRANSACTION_TYPE': ['', ''],
        'IMLUI_Billable Date': ['2024-01-02', '2024-01-02'],
        'IMLUI_Billable Qty': [2, 3],
        'IMLUI_Document ID': ['DOC-003', 'DOC-004']
    }
    
    df_master = pd.DataFrame(master_data)
    df_user = pd.DataFrame(user_data)
    
    return df_master, df_user

def process_excel(df_master, df_user):
    """Process the user file against the master file"""
    try:
        # Create a dictionary for quick lookup of exact matches
        master_dict = {(row['MATERIAL_NAME'], row['SUB_MATERIAL_NAME'], row['UOM']): (row['TRANSACTION_TYPE'], row['IMLUI_Billable Date'], row['IMLUI_Billable Qty'], row['IMLUI_Document ID']) 
                       for _, row in df_master.iterrows() if pd.notna(row['UOM'])}
        
        # Dictionary to track the matching method used for each row
        matching_methods = {}
        # Dictionary to track the best match scores for each row
        best_match_scores = {}
        # Dictionary to track semantic scores for each row
        semantic_scores = {}
        # Dictionary to track fuzzy scores for each row
        fuzzy_scores = {}
        # Dictionary to track matched master_sub_material for each row
        matched_master_sub_materials = {}
        
        # Process each row in user file
        for index, row in df_user.iterrows():
            # Check if MATERIAL_NAME, SUB_MATERIAL_NAME and UOM have values
            if pd.notna(row['MATERIAL_NAME']) and pd.notna(row['SUB_MATERIAL_NAME']) and pd.notna(row['UOM']):
                material_name = row['MATERIAL_NAME']
                sub_material_name = row['SUB_MATERIAL_NAME']
                uom = row['UOM']
                
                print(f"\nProcessing row {index}: {material_name}, {sub_material_name}, {uom}")
                
                # Check for exact match first
                if (material_name, sub_material_name, uom) in master_dict:
                    transaction_type, billable_date, billable_qty, document_id = master_dict[(material_name, sub_material_name, uom)]
                    df_user.at[index, 'TRANSACTION_TYPE'] = transaction_type
                    print(f"Exact match found: {transaction_type}")
                else:
                    # Perform semantic matching using fuzzy string matching
                    best_match = None
                    best_score = 0
                    best_semantic_score = 0
                    best_fuzzy_score = 0
                    best_master_sub_material = ""
                    best_matching_method = ""
                    
                    print(f"No exact match, performing semantic matching for '{sub_material_name}'")
                    
                    for (master_material, master_sub_material, master_uom), values in master_dict.items():
                        # Calculate combined similarity score
                        # For MATERIAL_NAME and UOM, use exact match or character similarity
                        material_score = fuzz.token_sort_ratio(str(material_name), str(master_material))
                        uom_score = fuzz.token_sort_ratio(str(uom), str(master_uom))
                        
                        # For SUB_MATERIAL_NAME, use both semantic similarity and fuzzy matching
                        current_fuzzy_score = fuzz.token_sort_ratio(str(sub_material_name), str(master_sub_material))
                        current_semantic_score = 0
                        
                        if use_semantic_matching:
                            try:
                                # Generate embeddings for both strings
                                embedding1 = model.encode(str(sub_material_name))
                                embedding2 = model.encode(str(master_sub_material))
                                # Calculate cosine similarity
                                
                                dot_product = np.dot(embedding1, embedding2)
                                norm1 = np.norm(embedding1)
                                norm2 = np.norm(embedding2)
                                
                                current_semantic_score = (dot_product / (norm1 * norm2)) * 100 if (norm1 * norm2) > 0 else 0
                                # Use weighted average of semantic and fuzzy scores
                                sub_material_score = (current_semantic_score * 0.8 + current_fuzzy_score * 0.2)
                                matching_method = 'AISemanticMapping'  # Using semantic mapping
                                print(f"  Semantic matching with '{master_sub_material}': semantic={current_semantic_score:.2f}, fuzzy={current_fuzzy_score}, combined={sub_material_score:.2f}")
                            except Exception as e:
                                print(f"  Error in semantic matching: {str(e)}")
                                # Fallback to fuzzy matching only if semantic similarity fails
                                sub_material_score = current_fuzzy_score
                                matching_method = 'FuzzyMapping'  # Using only fuzzy mapping
                                print(f"  Falling back to fuzzy matching with '{master_sub_material}': {current_fuzzy_score}")
                        else:
                            # Use fuzzy matching only
                            sub_material_score = current_fuzzy_score
                            matching_method = 'FuzzyMapping'  # Using only fuzzy mapping
                        
                        # Give more weight to SUB_MATERIAL_NAME as it's the most important for semantic matching
                        combined_score = (material_score * 0.2 + sub_material_score * 0.6 + uom_score * 0.2)
                        
                        if combined_score > best_score:
                            best_score = combined_score
                            best_match = values
                            best_matching_method = matching_method
                            best_semantic_score = current_semantic_score
                            best_fuzzy_score = current_fuzzy_score
                            best_master_sub_material = master_sub_material
                            print(f"  New best match: '{master_sub_material}' with score {best_score:.2f}")
                    
                    # Use the best match if similarity score is above threshold (e.g., 70)
                    if best_match and best_score > 70:
                        transaction_type, billable_date, billable_qty, document_id = best_match
                        df_user.at[index, 'TRANSACTION_TYPE'] = transaction_type
                        print(f"Best match selected: {transaction_type} (score: {best_score:.2f}, method: {best_matching_method})")
                        
                        # Store the matching method used for this row
                        matching_methods[index] = best_matching_method
                        best_match_scores[index] = best_score
                        semantic_scores[index] = best_semantic_score
                        fuzzy_scores[index] = best_fuzzy_score
                        matched_master_sub_materials[index] = best_master_sub_material
                    else:
                        print(f"No suitable match found (best score: {best_score:.2f})")
        
        # Add new columns at the end
        df_user['Match Type'] = ''
        df_user['Semantic Score'] = ''
        df_user['Fuzzy Score'] = ''
        df_user['Final Combined Score'] = ''
        df_user['Matched Master SUB_MATERIAL_NAME'] = ''
        
        # Check each row and mark as exact match or semantic inference
        for index, row in df_user.iterrows():
            if pd.notna(row['MATERIAL_NAME']) and pd.notna(row['SUB_MATERIAL_NAME']) and pd.notna(row['UOM']):
                material_name = row['MATERIAL_NAME']
                sub_material_name = row['SUB_MATERIAL_NAME']
                uom = row['UOM']
                
                # Determine match type
                if (material_name, sub_material_name, uom) in master_dict:
                    df_user.at[index, 'Match Type'] = "Exact Match"
                    df_user.at[index, 'Semantic Score'] = "-"
                    df_user.at[index, 'Fuzzy Score'] = "-"
                    df_user.at[index, 'Final Combined Score'] = "-"
                    df_user.at[index, 'Matched Master SUB_MATERIAL_NAME'] = sub_material_name
                elif index in matching_methods:
                    # Use the matching method stored during processing
                    df_user.at[index, 'Match Type'] = matching_methods[index]
                    df_user.at[index, 'Semantic Score'] = semantic_scores.get(index, "-")
                    df_user.at[index, 'Fuzzy Score'] = fuzzy_scores.get(index, "-")
                    df_user.at[index, 'Final Combined Score'] = best_match_scores.get(index, "-")
                    df_user.at[index, 'Matched Master SUB_MATERIAL_NAME'] = matched_master_sub_materials.get(index, "-")
                else:
                    df_user.at[index, 'Match Type'] = "Unknown"
                    df_user.at[index, 'Semantic Score'] = "-"
                    df_user.at[index, 'Fuzzy Score'] = "-"
                    df_user.at[index, 'Final Combined Score'] = "-"
                    df_user.at[index, 'Matched Master SUB_MATERIAL_NAME'] = "-"
        
        return df_user, None
        
    except Exception as e:
        print(f"Error in process_excel: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, str(e)

# Test the processing logic
df_master, df_user = create_test_data()

print("Master Data:")
print(df_master)
print("\nUser Data:")
print(df_user)

result, error = process_excel(df_master, df_user)

if error:
    print(f"Error: {error}")
else:
    print("\nProcessing completed successfully!")
    print("\nResult:")
    print(result)
