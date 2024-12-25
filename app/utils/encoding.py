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
    
    Args:
        content: 需要编码的字节内容
        data_type: 数据类型 ('0':文字, '1':图像, '2':音频, '3':视频, '4':其他)
    
    Returns:
        str: Base64编码后的字符串
    
    Raises:
        ValueError: 当数据类型不支持或内容为空时抛出
    """
    if not content:
        raise ValueError("文件内容不能为空")
        
    if not isinstance(content, bytes):
        raise ValueError(f"内容类型必须是bytes，当前类型为: {type(content)}")
        
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
        encoded_bytes = base64.b64encode(content)
        return encoded_bytes.decode('utf-8')
    except Exception as e:
        raise ValueError(f"Base64编码失败: {str(e)}")
