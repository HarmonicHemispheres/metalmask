![alt text](banner.png)

# 🛡️✨ MetalMask ✨🛡️
A Data Masking framework that ai can understand. DataMask includes tools for masking sensitive data as well as searching strings for data that is sensitive. 

<br>

# Python Package

```python
from metalmask import MetalMask, AI_MODELS, MaskMode

# -- setup
metal = MetalMask(
    openai_api_key = "sk-.........",
    openai_model = AI_MODELS.GPT_4_TURBO
)

# -----------------
# MASK (BASIC)
# NOTE.... simply masks the data locally. alpha chars with C and digits with N.
# -----------------
v = "243-45-4433"
v_mask = metal.mask(v)
# v_mask RESULT => "NNN-NN-NNNN"

# -----------------
# MASK (ONLY SENSITIVE DATA)
# -----------------
v = "here is a string where i have a ssn to mask: 243-45-4433"
v_mask = metal.mask(v, mode=MaskMode.sensitive_only)
# v_mask RESULT => "here is a string where i have a ssn to mask: NNN-NN-NNNN"

# -----------------
# IS_SENSITIVE
# -----------------
v = "2300 Harrison St, San Francisco, CA 94110"
is_pii = metal.is_sensitive(v, types=metal.DEFAULT_SENSITIVE_DATA)
# is_pii RESULT =>
# {
#    "contains_sensitive_data": true,
#    "data_mode": "raw",
#    "type": "street address",
#    "step_by_step": "The provided data '2300 Harrison St, San Francisco, CA 94110' resembles a typical street address format with a street name, city, and zip code. Cross-referencing with the sensitive types list in the protocol, 'street address' is listed as sensitive information. The data is not masked as it contains readable text."
# }

```

<br>


# RULES
### Framework
-  convert all non-alpha-numeric values to x
-  preserve length of original value
-  
-  


### System Prompt
```
```
