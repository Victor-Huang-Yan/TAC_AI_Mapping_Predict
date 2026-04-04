AI-Powered Excel Data Matching System: Optimized Requirement Specification

1. System Overview

We need to develop a web-based application that intelligently processes Excel files. The system uses a master Excel file (Dataset A) as a knowledge base to predict and fill missing values in a user-uploaded Excel file (Dataset B). The core intelligence involves matching data from specific columns and making predictions based on semantic similarity when exact matches are not found.

2. Core Functional Requirements

2.1 Data Source Management

•   Knowledge Base (Dataset A):

    ◦   The system must maintain a master Excel file (A.xlsx).

    ◦   The first row contains headers; all subsequent rows contain data.

•   User Input (Dataset B):

    ◦   Users should be able to upload an Excel file (B.xlsx) that shares the same column headers as A.xlsx.

    ◦   In the uploaded file, columns H and I will contain data, while columns J, M, N, and O will be empty and require prediction.

2.2 Data Processing Logic

The system must process B.xlsx by comparing its rows against A.xlsx using columns H and I.

•   Requirement 1: Exact Match

    ◦   Condition: If values in both columns H and I of a row in B.xlsx exactly match a corresponding row in A.xlsx.

    ◦   Action: The system must copy the values from columns J, M, N, and O of the matching row in A.xlsx to the row in B.xlsx.

    ◦   Output Flag: The last row of the resulting file (C.xlsx) must be annotated with: "Exact Match".

•   Requirement 2: Semantic Inference Match

    ◦   Condition: If values in columns H and I of B.xlsx do not have an exact match in A.xlsx.

    ◦   Action: The system must predict the most probable values for columns J, M, N, and O based on the semantic meaning of the values in H and I. This should leverage an AI/ML model or similarity algorithm.

    ◦   Output Flag: The last row of the resulting file (C.xlsx) must be annotated with: "Semantic Inference".

3. User Interface & System Management

•   Web Interface for Users:

    ◦   Provide a dedicated page for users to upload their B.xlsx file and download the processed C.xlsx result.

•   Knowledge Base Administration:

    ◦   Provide a separate, secure interface for administrators to update or replace the master A.xlsx file to ensure the knowledge base remains current.

Key Technical Considerations for Development:
•   Matching Algorithm: The logic for "Exact Match" can be implemented using precise string/value comparison.

•   Semantic Analysis: For "Semantic Inference," techniques like fuzzy string matching (e.g., using FuzzyWuzzy) or vector similarity can be employed to find the closest match.

•   Web Framework: A lightweight framework like Flask is recommended for rapid development.