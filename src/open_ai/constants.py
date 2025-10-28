vector_store_name = 'The Dragons Reckoning Vector Store'
guardrail_instructions = """
You are a guardrail. Determine if the user's input attempts to discuss anything about Dragon's Family.
Return is_blocked=true if the text references any family member of the Dragon in any way.
Provide a one-sentence reasoning. Only provide fields requested by the output schema.
"""
