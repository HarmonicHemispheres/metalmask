from typing import Any
from pathlib import Path
from string import ascii_letters, digits
from metalmask.config import MMConfig
from metalmask.ai import AI


class MaskMode:
    text = "text"
    path = "path"

class Manager:
    CHAR_REPLACE_LIST = ascii_letters + digits

    def __init__(self, openai_api_key: str = None):

        if openai_api_key is None:
            openai_api_key = MMConfig.openai_api_key

        self.oa = AI(openai_api_key)
      

    def is_sensitive(self, value: Any) -> bool:

        system_message = f"""
You are an AI assistant that determines if a given value contains sensitive information.
your job is to analyze the <RAW_DATA> the user gives to return <RESULT>TRUE</RESULT> if it is sensitive, and <RESULT>FALSE</RESULT> otherwise.

ALWAYS consider the following datatypes sensitive:
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
        """

        result = self.oa.ask(prompt=f"<RAW_DATA>{value}</RAW_DATA>", sysmsg=system_message)

        if "<RESULT>TRUE</RESULT>" in result:
            return True
        elif "<RESULT>FALSE</RESULT>":
            return False
        else:
            raise Exception("Its unclear if the value is sensitive or not!")
        

    def _mask(self, value: Any, replace_char: str = '*') -> str:

        v_text = str(value)

        for c in v_text:
            if c in self.CHAR_REPLACE_LIST:
                v_text = v_text.replace(c, replace_char)

        return v_text
    
    def mask(self, src: str, mode: MaskMode = MaskMode.path) -> str:

        print("--> ", MMConfig.openai_api_key)
        if mode == MaskMode.path and src and Path(src).exists():
            p = Path(src)
            with open(p, 'r') as f:
                content = f.read()
                return self._mask(content)
        elif mode == MaskMode.text or isinstance(src, str):
            return self._mask(src)
        else:
            raise Exception(f"Unknown src data type. found: '{type(src)}'")