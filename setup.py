from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ocr-enterprise",
    version="1.0.0",
    author="Platoba",
    author_email="platobate@gmail.com",
    description="Production-Ready OCR Service Built on PaddleOCR",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/platoba/OCR-Enterprise",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        "fastapi>=0.100.0",
        "uvicorn>=0.23.0",
        "python-multipart>=0.0.6",
        "Pillow>=9.0.0",
        "click>=8.0.0",
        "requests>=2.28.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
        ],
        "gpu": [
            "paddlepaddle-gpu>=2.5.0",
        ],
        "full": [
            "paddleocr>=2.7.0",
            "redis>=4.5.0",
            "boto3>=1.26.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ocr-enterprise=ocr_enterprise.cli.commands:cli",
        ],
    },
)
