from openai import OpenAI


class AI:

    def __init__(self, opanai_api_key: str = None):
        self.openai_api_key = opanai_api_key
        self.model = "gpt-3.5-turbo"

        if isinstance(self.openai_api_key, str):
            self.oa = OpenAI(api_key=self.openai_api_key)
        else:
            self.oa = None

    def system(self) -> str:
        return "You are a helpful AI assistant"

    def ask(self, prompt: str, sysmsg: str = None, model: str = None) -> str:
        
        if not sysmsg:
            sysmsg = self.system()
        
        if not model:
            model = self.model

        response = self.oa.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": sysmsg},
                {"role": "user", "content": prompt}
            ]
            # n=1,
            # stop=None,
            # temperature=0.7,
        )
        return response.choices[0].message.content