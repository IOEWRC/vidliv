from .base import *
from decouple import config

if config('RUNNING_ENVIRON') == 'LOCAL':
    from .local import *
elif config('RUNNING_ENVIRON') == 'PROD':
    from .prod import *
