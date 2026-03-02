"""
CLI命令
"""
import click
import json
from pathlib import Path
from ..core.engine import OCREngine


@click.group()
def cli():
    """OCR Enterprise CLI"""
    pass


@cli.command()
@click.argument('image_path')
@click.option('--language', '-l', default='ch', help='语言')
@click.option('--output', '-o', help='输出文件')
def recognize(image_path, language, output):
    """识别单张图片"""
    engine = OCREngine(language=language)
    
    result = engine.recognize(image_path, language)
    
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)
        click.echo(f"✅ 结果已保存: {output}")
    else:
        click.echo(f"文本: {result.text}")
        click.echo(f"置信度: {result.confidence:.2%}")


@cli.command()
@click.argument('image_paths', nargs=-1)
@click.option('--language', '-l', default='ch', help='语言')
@click.option('--output', '-o', help='输出目录')
def batch_recognize(image_paths, language, output):
    """批量识别"""
    engine = OCREngine(language=language)
    
    results = engine.batch_recognize(list(image_paths), language)
    
    if output:
        Path(output).mkdir(parents=True, exist_ok=True)
        
        for i, result in enumerate(results):
            output_file = Path(output) / f"result_{i}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)
        
        click.echo(f"✅ {len(results)} 个结果已保存到: {output}")
    else:
        for i, result in enumerate(results):
            click.echo(f"\n[{i+1}] {result.text}")


@cli.command()
@click.argument('image_path')
def idcard(image_path):
    """识别身份证"""
    engine = OCREngine()
    result = engine.recognize_idcard(image_path)
    
    click.echo("身份证信息:")
    for key, value in result.items():
        click.echo(f"  {key}: {value}")


@cli.command()
@click.argument('image_path')
def bankcard(image_path):
    """识别银行卡"""
    engine = OCREngine()
    result = engine.recognize_bankcard(image_path)
    
    click.echo("银行卡信息:")
    for key, value in result.items():
        click.echo(f"  {key}: {value}")


@cli.command()
@click.argument('image_path')
def plate(image_path):
    """识别车牌"""
    engine = OCREngine()
    result = engine.recognize_plate(image_path)
    
    click.echo("车牌信息:")
    for key, value in result.items():
        click.echo(f"  {key}: {value}")


if __name__ == '__main__':
    cli()
