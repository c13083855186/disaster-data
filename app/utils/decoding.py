# app/utils/decoding.py

import base64

def decode_content_text(encoded_content: str) -> str:
    """
    对编码后的文本内容进行解码
    """
    decoded_bytes = base64.b64decode(encoded_content)
    return decoded_bytes.decode('utf-8')

def decode_content_file(encoded_content: str, data_type: str) -> bytes:
    """
    对编码后的文件内容进行解码
    """
    if data_type in ['image', 'audio', 'video']:
        decoded_bytes = base64.b64decode(encoded_content)
        return decoded_bytes
    else:
        raise ValueError("Unsupported data type for decoding")
