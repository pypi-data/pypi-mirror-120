# sha-accounts
Customized Django Rest Framework Accounting App
### Installation
```bash
pip install sha-accounts
```
### Quick Start
set these variables on `settings.py`
```python
from datetime import timedelta

SHA_ACCOUNTS = {
'DEFAULT_ACTIVATION': True,
'AUTH_USER_PROFILE_MODEL': 'examples.ExampleProfile',
'JWT_ACCESS_TOKEN_EXP': timedelta(days=1),
'JWT_USER_ENCODED_FIELDS': ['id'],
'JWT_AUTH_RAELM':'sample_raelm'
}
```
