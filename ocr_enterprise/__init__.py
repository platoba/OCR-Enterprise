"""
OCR Enterprise - Production-Ready OCR Service

基于PaddleOCR深度二开的企业级OCR服务
"""

from .core.engine import OCREngine
from .core.client import OCRClient

__version__ = "1.0.0"
__all__ = ["OCREngine", "OCRClient"]
