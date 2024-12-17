# app/utils/encoding.py

import base64

def encode_content_text(content: str) -> str:
    """
    对文本内容进行编码，采用 Base64 编码
    """
    encoded_bytes = base64.b64encode(content.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

def encode_content_file(content: bytes, data_type: str) -> str:
    """
    对文件内容进行编码，采用 Base64 编码
    """
    if data_type in ['image', 'audio', 'video']:
        encoded_bytes = base64.b64encode(content)
        return encoded_bytes.decode('utf-8')
    else:
        raise ValueError("Unsupported data type for encoding")
