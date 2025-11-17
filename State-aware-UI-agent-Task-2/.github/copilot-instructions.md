# Copilot Behavioral Rules

## 1. Code-Length Restriction
Copilot must not generate code blocks longer than **50 lines** at a time.  
If the request requires more than 50 lines, Copilot must:
- Break the output into smaller chunks, OR
- Ask the user whether to continue before generating more.

## 2. Reasons for Enforcing This Limit
These limitations are important for my workflow:
- Easier debugging
- Clearer and more readable code
- Higher accuracy with fewer errors
- Prevent hallucination and unnecessary boilerplate
- Better context control