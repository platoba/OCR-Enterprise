"""
OCR客户端SDK
"""
from typing import List, Optional
import requests
from .engine import OCRResult


class OCRClient:
    """
    OCR客户端
    
    用于调用OCR Enterprise API
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "http://localhost:8000"
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": api_key
        })
    
    def recognize(
        self,
        image_path: str,
        language: str = "ch"
    ) -> OCRResult:
        """
        识别单张图片
        
        Args:
            image_path: 图片路径
            language: 语言
        
        Returns:
            OCRResult: 识别结果
        """
        url = f"{self.base_url}/api/v1/ocr/recognize"
        
        with open(image_path, "rb") as f:
            files = {"file": f}
            data = {"language": language}
            
            response = self.session.post(url, files=files, data=data)
            response.raise_for_status()
            
            result = response.json()
            return OCRResult(**result)
    
    def batch_recognize(
        self,
        image_paths: List[str],
        language: str = "ch"
    ) -> List[OCRResult]:
        """
        批量识别
        
        Args:
            image_paths: 图片路径列表
            language: 语言
        
        Returns:
            List[OCRResult]: 识别结果列表
        """
        url = f"{self.base_url}/api/v1/ocr/batch"
        
        files = [("files", open(path, "rb")) for path in image_paths]
        data = {"language": language}
        
        try:
            response = self.session.post(url, files=files, data=data)
            response.raise_for_status()
            
            results = response.json()
            return [OCRResult(**r) for r in results]
        finally:
            for _, f in files:
                f.close()
    
    def recognize_idcard(self, image_path: str):
        """识别身份证"""
        url = f"{self.base_url}/api/v1/ocr/idcard"
        
        with open(image_path, "rb") as f:
            files = {"file": f}
            response = self.session.post(url, files=files)
            response.raise_for_status()
            return response.json()
    
    def recognize_bankcard(self, image_path: str):
        """识别银行卡"""
        url = f"{self.base_url}/api/v1/ocr/bankcard"
        
        with open(image_path, "rb") as f:
            files = {"file": f}
            response = self.session.post(url, files=files)
            response.raise_for_status()
            return response.json()
    
    def recognize_plate(self, image_path: str):
        """识别车牌"""
        url = f"{self.base_url}/api/v1/ocr/plate"
        
        with open(image_path, "rb") as f:
            files = {"file": f}
            response = self.session.post(url, files=files)
            response.raise_for_status()
            return response.json()
    
    def get_task_status(self, task_id: str):
        """查询任务状态"""
        url = f"{self.base_url}/api/v1/tasks/{task_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
