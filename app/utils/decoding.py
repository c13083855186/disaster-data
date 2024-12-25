# app/utils/decoding.py

import base64

def decode_content_text(encoded_content: str) -> str:
    """
    对文本内容进行解码，采用 Base64 解码
    """
    if not encoded_content:
        raise ValueError("编码内容不能为空")
        
    try:
        decoded_bytes = base64.b64decode(encoded_content.encode('utf-8'))
        return decoded_bytes.decode('utf-8')
    except Exception as e:
        raise ValueError(f"Base64解码失败: {str(e)}")

def decode_content_file(encoded_content: str, data_type: str) -> bytes:
    """
    对文件内容进行解码，采用 Base64 解码
    
    Args:
        encoded_content: Base64编码的字符串
        data_type: 数据类型 ('0':文字, '1':图像, '2':音频, '3':视频, '4':其他)
    
    Returns:
        bytes: 解码后的字节内容
    
    Raises:
        ValueError: 当数据类型不支持或内容为空时抛出
    """
    if not encoded_content:
        raise ValueError("编码内容不能为空")
        
    if not data_type:
        raise ValueError("数据类型不能为空")
        
    data_type_map = {
        '0': '文字',
        '1': '图像',
        '2': '音频',
        '3': '视频',
        '4': '其他'
    }
    
    if data_type not in data_type_map:
        raise ValueError(f"不支持的数据类型: {data_type}。支持的类型包括: {', '.join([f'{k}({v})' for k,v in data_type_map.items()])}")
    
    try:
        decoded_bytes = base64.b64decode(encoded_content)
        return decoded_bytes
    except Exception as e:
        raise ValueError(f"Base64解码失败: {str(e)}")
