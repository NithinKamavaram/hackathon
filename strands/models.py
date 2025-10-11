"""Mock models module for strands"""

class BedrockModel:
    def __init__(self, model_id=None, region_name=None, temperature=0.3,
                 max_tokens=4096, streaming=True, **kwargs):
        self.model_id = model_id
        self.region_name = region_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.streaming = streaming