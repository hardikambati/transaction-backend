import jwt
import uuid

from main.settings import SECRET_KEY


def request_from_args(args):
    '''
    return 'request' from parameters
    '''
    try:
        return args[1]
    except:
        return args[0]
    

def pop_from_data(pop_list: list, data: list):
    '''
    pop values from data and return data
    '''
    for item in pop_list:
        if item in data:
            data.pop(item)
    return data


def generate_key(size: int):
    '''
    generates key of length 'size'
    
    NOTE: max limit of size should be 35
    '''
    key_str = str(uuid.uuid4())
    return key_str[:size]


def encode_data(attributes: dict) -> str:
    return jwt.encode(attributes, SECRET_KEY, algorithm="HS256")


def decode_data(data: str) -> dict:
    return jwt.decode(data, SECRET_KEY, algorithms=["HS256"])

