def get_analysis_prompt(message, channel="unknown"):
    """Generate structured analysis prompt for LLM"""
    
    return f"""Analyze this customer message and extract structured data.
Message: "{message}"
Channel: {channel}

Extract and respond with JSON format:
{{
    "intent": "buy|question|complaint|inquiry",
    "urgency": "low|medium|high",
    "name": "extracted name or empty string",
    "email": "extracted email or empty string",
    "phone": "extracted phone or empty string",
    "budget": "if mentioned, e.g. '$1000-$5000' or empty string",
    "category": "general|premium|enterprise|support"
}}

Rules:
1. Intent: What does the user want? (buy/question/complaint/inquiry)
2. Urgency: How urgent is this? (low/medium/high)
3. Extract contact info if present (name, email, phone)
4. Detect budget if mentioned
5. Category: Classify the inquiry type

Respond ONLY with valid JSON, no additional text."""