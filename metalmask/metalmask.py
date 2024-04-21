from typing import Any
from pathlib import Path
from string import ascii_letters, digits
from metalmask.config import MMConfig
from metalmask.ai import AI
import json


class MaskMode:
    all = "all"
    sensitive_only = "sensitive_only"

class MetalMask:
    CHAR_REPLACE_LIST = ascii_letters + digits
    DEFAULT_SENSITIVE_DATA = """
- social security number
- email
- phone number
- credit card number
- bank account number
- passport number
- driver's license number
- username
- password
- ip address
- street address
"""

    def __init__(self, 
                 openai_api_key: str = None,
                 openai_model: str = None
                 ):

        if openai_api_key is None:
            openai_api_key = MMConfig.openai_api_key

        if openai_model is None:
            openai_model = AI.models.GPT_3_5_TURBO

        self.oa = AI(openai_api_key, openai_model)
        

    def _mask(self, 
              value: Any, 
              replace_num_char: str = 'N', 
              replace_alpha_char: str = 'C',
              only_sensitive: bool = False,
              types=None
              ) -> str:

        if not types:
            types = self.DEFAULT_SENSITIVE_DATA

        v_text = str(value)
        
        if only_sensitive:
            sys_msg = f"""
<YOUR PURPOSE>
You are an AI assistant that masks sensitive data in a given string. 
Your job is to analyze the <DATA> the user provides and return the masked version of the data, replacing sensitive characters. always return json data with the fields in the <RESPONSE FORMAT> section below.
</YOUR PURPOSE>

<PROTOCAL RULES TO FOLLOW>
- RULE-1: use C to mask alpha characters and N to mask digits
- RULE-2: verify your reasoning in the response field "step_by_step".
- RULE-3a: if <ONLY_SENSITIVE>TRUE</ONLY_SENSITIVE>, only mask sensitive data as defined in <SENSITIVE_TYPES> with character replacements defined in rule-1 
- RULE-3b: if <ONLY_SENSITIVE>FALSE</ONLY_SENSITIVE> mask all alphanumeric characters according to rule-1
</PROTOCAL RULES TO FOLLOW>

<SENSITIVE_TYPES>
{types}
</SENSITIVE_TYPES>

<RESPONSE FORMAT>
{{
    "masked_data": "<MASKED TEXT>",
    "step_by_step": "<TEXT>"
}}
</RESPONSE FORMAT>
"""
            prompt = f"<DATA>{value}</DATA><ONLY_SENSITIVE>{only_sensitive}</ONLY_SENSITIVE>"
            response = self.oa.ask(prompt=prompt, sysmsg=sys_msg, json_mode=True)
            return response["masked_data"]
        else:
            for c in v_text:
                if c in self.CHAR_REPLACE_LIST:
                    if c.isdigit():
                        v_text = v_text.replace(c, replace_num_char)
                    elif c.isalpha():
                        v_text = v_text.replace(c, replace_alpha_char)

            return v_text
    
    def mask(self, 
             src: str, 
             mode: MaskMode = MaskMode.all,
             replace_num_char: str = 'N', 
             replace_alpha_char: str = 'C'
             ) -> str:

        data = None

        # -- PREPARE DATA
        if isinstance(src, str):
            data = src
        elif isinstance(src, Path) and src.exists():
            with open(src, 'r') as f:
                data = f.read()
            
        # -- MASK DATA
        if mode == MaskMode.all:
            return self._mask(data, replace_num_char, replace_alpha_char, only_sensitive=False)
        elif mode == MaskMode.sensitive_only:
            return self._mask(data, replace_num_char, replace_alpha_char, only_sensitive=True)


    def is_sensitive(self, value: Any, types=None) -> bool:

        if not types:
            types = self.DEFAULT_SENSITIVE_DATA

        system_message = f"""
<YOUR PURPOSE>
You are an AI assistant that determines if a given value contains sensitive information.
your job is to analyze the <DATA> the user gives to return json data with the fields in the <RESPONSE FORMAT> section below.
</YOUR PURPOSE>

<PROTOCAL RULES TO FOLLOW>
- RULE-1: if the data is masked it will use C for alpha characters and N for digits.
- RULE-2: verify your reasoning in the response field "step_by_step".
- RULE-3: "contains_sensitive_data" should be true if the raw data or pattern of the <DATA> looks like a sensitive datatype, and false otherwise.
- RULE-4: "data_mode" should be "raw" if the <DATA> is not masked, and "masked" if the <DATA> is masked.
- RULE-5: ONLY consider the datatypes in the <SENSITIVE_TYPES> section as sensitive unless <SENSITIVE_TYPES> is simply <ANY>, then use your own judgement
- RULE-6: "type" should always contain what you think the datatype is even if its not sensitive
</PROTOCAL RULES TO FOLLOW>

<SENSITIVE_TYPES>
{types}
</SENSITIVE_TYPES>

<RESPONSE FORMAT>
{{
    "contains_sensitive_data": <RESULT>True</RESULT>,
    "data_mode": "<CHOICE of 'raw' or 'masked'>",
    "type": "<TEXT>",
    "step_by_step": "<TEXT>"
}}
</RESPONSE FORMAT>
        """

        prompt = f"<DATA>{value}</DATA>"
        return self.oa.ask(prompt=prompt, sysmsg=system_message, json_mode=True)