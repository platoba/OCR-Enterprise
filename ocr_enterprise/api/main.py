"""
FastAPI服务入口
"""
from fastapi import FastAPI, File, UploadFile, Header, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Optional
import tempfile
from pathlib import Path

from ..core.engine import OCREngine

app = FastAPI(
    title="OCR Enterprise API",
    description="Production-Ready OCR Service",
    version="1.0.0"
)

# 初始化OCR引擎
engine = OCREngine(use_gpu=False, language="ch")


def verify_api_key(x_api_key: str = Header(...)):
    """验证API密钥"""
    # 简化实现：实际应用中从数据库验证
    if not x_api_key or x_api_key == "":
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


@app.get("/")
async def root():
    """根路径"""
    return {
        "service": "OCR Enterprise",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "healthy"}


@app.post("/api/v1/ocr/recognize")
async def recognize(
    file: UploadFile = File(...),
    language: str = "ch",
    api_key: str = Header(..., alias="X-API-Key")
):
    """识别单张图片"""
    verify_api_key(api_key)
    
    # 保存临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        # 识别
        result = engine.recognize(tmp_path, language)
        return result.to_dict()
    finally:
        Path(tmp_path).unlink(missing_ok=True)


@app.post("/api/v1/ocr/batch")
async def batch_recognize(
    files: List[UploadFile] = File(...),
    language: str = "ch",
    api_key: str = Header(..., alias="X-API-Key")
):
    """批量识别"""
    verify_api_key(api_key)
    
    results = []
    tmp_paths = []
    
    try:
        # 保存临时文件
        for file in files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
                content = await file.read()
                tmp.write(content)
                tmp_paths.append(tmp.name)
        
        # 批量识别
        ocr_results = engine.batch_recognize(tmp_paths, language)
        
        for result in ocr_results:
            results.append(result.to_dict())
        
        return results
    finally:
        for path in tmp_paths:
            Path(path).unlink(missing_ok=True)


@app.post("/api/v1/ocr/idcard")
async def recognize_idcard(
    file: UploadFile = File(...),
    api_key: str = Header(..., alias="X-API-Key")
):
    """识别身份证"""
    verify_api_key(api_key)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        result = engine.recognize_idcard(tmp_path)
        return result
    finally:
        Path(tmp_path).unlink(missing_ok=True)


@app.post("/api/v1/ocr/bankcard")
async def recognize_bankcard(
    file: UploadFile = File(...),
    api_key: str = Header(..., alias="X-API-Key")
):
    """识别银行卡"""
    verify_api_key(api_key)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        result = engine.recognize_bankcard(tmp_path)
        return result
    finally:
        Path(tmp_path).unlink(missing_ok=True)


@app.post("/api/v1/ocr/plate")
async def recognize_plate(
    file: UploadFile = File(...),
    api_key: str = Header(..., alias="X-API-Key")
):
    """识别车牌"""
    verify_api_key(api_key)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        result = engine.recognize_plate(tmp_path)
        return result
    finally:
        Path(tmp_path).unlink(missing_ok=True)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
