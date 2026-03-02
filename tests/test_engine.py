"""
测试OCR引擎
"""
import pytest
import tempfile
from pathlib import Path
from PIL import Image
from ocr_enterprise.core.engine import OCREngine, OCRResult


@pytest.fixture
def test_image():
    """创建测试图片"""
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
        img = Image.new('RGB', (800, 600), color='white')
        img.save(f.name)
        yield f.name
        Path(f.name).unlink(missing_ok=True)


def test_engine_initialization():
    """测试引擎初始化"""
    engine = OCREngine(use_gpu=False, language="ch")
    assert engine.use_gpu == False
    assert engine.language == "ch"


def test_recognize(test_image):
    """测试识别"""
    engine = OCREngine()
    result = engine.recognize(test_image)
    
    assert isinstance(result, OCRResult)
    assert result.text is not None
    assert result.confidence > 0
    assert len(result.boxes) > 0


def test_batch_recognize(test_image):
    """测试批量识别"""
    engine = OCREngine()
    results = engine.batch_recognize([test_image, test_image])
    
    assert len(results) == 2
    assert all(isinstance(r, OCRResult) for r in results)


def test_recognize_idcard(test_image):
    """测试身份证识别"""
    engine = OCREngine()
    result = engine.recognize_idcard(test_image)
    
    assert "name" in result
    assert "id_number" in result
    assert "address" in result


def test_recognize_bankcard(test_image):
    """测试银行卡识别"""
    engine = OCREngine()
    result = engine.recognize_bankcard(test_image)
    
    assert "card_number" in result
    assert "expiry_date" in result


def test_recognize_plate(test_image):
    """测试车牌识别"""
    engine = OCREngine()
    result = engine.recognize_plate(test_image)
    
    assert "plate_number" in result
    assert "color" in result


def test_recognize_table(test_image):
    """测试表格识别"""
    engine = OCREngine()
    result = engine.recognize_table(test_image)
    
    assert isinstance(result, list)
    assert len(result) > 0
