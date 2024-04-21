from openai import OpenAI
import json

class AI:

    class models:
        GPT_3_5_TURBO = "gpt-3.5-turbo"
        GPT_4 = "gpt-4"
        GPT_4_TURBO = "gpt-4-turbo"

    def __init__(self, opanai_api_key: str = None, model: str = "gpt-3.5-turbo"):
        self.openai_api_key = opanai_api_key
        self.model = model

        if isinstance(self.openai_api_key, str):
            self.oa = OpenAI(api_key=self.openai_api_key)
        else:
            self.oa = None

    def system(self) -> str:
        return "You are a helpful AI assistant"

    def ask(self, prompt: str, sysmsg: str = None, model: str = None, json_mode: bool = False) -> str:
        
        if not sysmsg:
            sysmsg = self.system()
        
        if not model:
            model = self.model

        mode = None
        if json_mode:
            mode = { "type": "json_object" }

        response = self.oa.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": sysmsg},
                {"role": "user", "content": prompt}
            ],
            response_format=mode,

            # n=1,
            # stop=None,
            # temperature=0.7,
        )

        if json_mode:
            return json.loads(response.choices[0].message.content)
        else:
            return response.choices[0].message.content