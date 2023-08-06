# Copyright 2020 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Error Handler function
"""

import functools
from exceptions.invalid_parameter import InvalidParamException
from exceptions.unknown_error import UnknownException
#from exceptions.contract_error import ContractFailed


def error_handler(f):
    @functools.wraps(f)
    def func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        
        except InvalidParamException as e:
            return e.error
#        except ContractFailed as e:
#            return e.error
        except Exception as e:
            msg = 'Caught an exception in '+ f.__name__
            err = UnknownException(msg, e)
            return err.error
    return func

