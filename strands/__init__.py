"""Mock strands package for testing"""

class Agent:
    def __init__(self, name=None, model=None, system_prompt=None, tools=None, **kwargs):
        self.name = name or 'MockAgent'
        self.model = model
        self.system_prompt = system_prompt
        self.tools = tools or []

    def __call__(self, prompt):
        """Mock agent execution"""
        return type('Result', (), {
            'message': f'Mock {self.name} response: Completed task - {prompt[:100]}',
            'metrics': type('Metrics', (), {
                'total_tokens': 150,
                'latency_ms': 500
            })()
        })()

    async def stream_async(self, prompt):
        """Mock async streaming"""
        yield {'type': 'start', 'message': f'{self.name} starting'}
        yield {'type': 'content', 'message': f'Processing: {prompt[:50]}'}
        yield {'type': 'end', 'message': 'Complete'}

def tool(func):
    """Mock tool decorator"""
    return func

class BedrockModel:
    def __init__(self, model_id=None, region_name=None, temperature=0.3,
                 max_tokens=4096, streaming=True, **kwargs):
        self.model_id = model_id
        self.region_name = region_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.streaming = streaming