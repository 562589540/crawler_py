#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Camoufox浏览器安装诊断和修复脚本
解决 "manifest.json is missing" 错误
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
from loguru import logger

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    logger.info(f"Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        logger.error("需要Python 3.8或更高版本")
        return False
    return True

def check_camoufox_installation():
    """检查camoufox安装状态"""
    try:
        import camoufox
        logger.info(f"Camoufox版本: {camoufox.__version__}")
        return True
    except ImportError:
        logger.error("Camoufox未安装")
        return False

def check_playwright_installation():
    """检查playwright安装状态"""
    try:
        import playwright
        logger.info(f"Playwright版本: {playwright.__version__}")
        return True
    except ImportError:
        logger.error("Playwright未安装")
        return False

def get_camoufox_path():
    """获取camoufox浏览器路径"""
    try:
        import camoufox
        # 尝试获取camoufox的安装路径
        camoufox_module_path = Path(camoufox.__file__).parent
        logger.info(f"Camoufox模块路径: {camoufox_module_path}")
        
        # 查找可能的浏览器路径
        possible_paths = [
            camoufox_module_path / "firefox",
            camoufox_module_path / "browser",
            camoufox_module_path / "camoufox-browser",
        ]
        
        for path in possible_paths:
            if path.exists():
                logger.info(f"找到浏览器路径: {path}")
                return path
        
        logger.warning("未找到camoufox浏览器文件")
        return None
        
    except Exception as e:
        logger.error(f"获取camoufox路径失败: {e}")
        return None

def check_camoufox_browser_files():
    """检查camoufox浏览器文件完整性"""
    browser_path = get_camoufox_path()
    if not browser_path:
        return False
    
    # 检查关键文件
    critical_files = [
        "manifest.json",
        "firefox" if platform.system() != "Windows" else "firefox.exe",
        "application.ini",
    ]
    
    missing_files = []
    for file_name in critical_files:
        file_path = browser_path / file_name
        if not file_path.exists():
            missing_files.append(file_name)
            logger.error(f"缺少关键文件: {file_path}")
        else:
            logger.info(f"找到文件: {file_path}")
    
    if missing_files:
        logger.error(f"缺少关键文件: {missing_files}")
        return False
    
    return True

def reinstall_camoufox():
    """重新安装camoufox"""
    logger.info("开始重新安装camoufox...")
    
    try:
        # 卸载现有版本
        logger.info("卸载现有camoufox...")
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "camoufox", "-y"], 
                      check=True, capture_output=True, text=True)
        
        # 清理缓存
        logger.info("清理pip缓存...")
        subprocess.run([sys.executable, "-m", "pip", "cache", "purge"], 
                      check=False, capture_output=True, text=True)
        
        # 重新安装
        logger.info("重新安装camoufox...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", "camoufox>=0.2.0", "--force-reinstall"], 
                               check=True, capture_output=True, text=True)
        
        logger.info("Camoufox安装输出:")
        logger.info(result.stdout)
        
        if result.stderr:
            logger.warning("安装警告:")
            logger.warning(result.stderr)
        
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"重新安装camoufox失败: {e}")
        logger.error(f"错误输出: {e.stderr}")
        return False

def install_playwright_browsers():
    """安装playwright浏览器"""
    logger.info("安装playwright浏览器...")
    
    try:
        result = subprocess.run([sys.executable, "-m", "playwright", "install"], 
                               check=True, capture_output=True, text=True)
        
        logger.info("Playwright浏览器安装输出:")
        logger.info(result.stdout)
        
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"安装playwright浏览器失败: {e}")
        logger.error(f"错误输出: {e.stderr}")
        return False

def test_camoufox():
    """测试camoufox是否能正常工作"""
    logger.info("测试camoufox功能...")
    
    try:
        import asyncio
        from playwright.async_api import async_playwright
        from camoufox import AsyncNewBrowser
        
        async def test_browser():
            playwright = await async_playwright().start()
            try:
                browser = await AsyncNewBrowser(
                    playwright,
                    headless=True,
                    args=['--no-sandbox', '--disable-dev-shm-usage']
                )
                
                context = await browser.new_context()
                page = await context.new_page()
                
                await page.goto("https://www.google.com", timeout=10000)
                title = await page.title()
                
                logger.success(f"测试成功，页面标题: {title}")
                
                await browser.close()
                await playwright.stop()
                
                return True
                
            except Exception as e:
                logger.error(f"浏览器测试失败: {e}")
                await playwright.stop()
                return False
        
        return asyncio.run(test_browser())
        
    except Exception as e:
        logger.error(f"测试camoufox失败: {e}")
        return False

def main():
    """主函数"""
    logger.info("🔍 开始诊断Camoufox安装问题...")
    logger.info("=" * 60)
    
    # 1. 检查Python版本
    logger.info("1. 检查Python版本")
    if not check_python_version():
        return False
    
    # 2. 检查依赖安装
    logger.info("\n2. 检查依赖安装")
    playwright_ok = check_playwright_installation()
    camoufox_ok = check_camoufox_installation()
    
    if not playwright_ok:
        logger.error("请先安装playwright: pip install playwright>=1.40.0")
        return False
    
    if not camoufox_ok:
        logger.error("请先安装camoufox: pip install camoufox>=0.2.0")
        return False
    
    # 3. 检查浏览器文件
    logger.info("\n3. 检查浏览器文件完整性")
    if not check_camoufox_browser_files():
        logger.warning("Camoufox浏览器文件不完整，尝试重新安装...")
        
        # 4. 重新安装camoufox
        logger.info("\n4. 重新安装Camoufox")
        if not reinstall_camoufox():
            logger.error("重新安装失败")
            return False
        
        # 5. 安装playwright浏览器
        logger.info("\n5. 安装Playwright浏览器")
        if not install_playwright_browsers():
            logger.warning("Playwright浏览器安装失败，但可能不影响camoufox")
        
        # 6. 重新检查文件
        logger.info("\n6. 重新检查文件完整性")
        if not check_camoufox_browser_files():
            logger.error("重新安装后文件仍不完整")
            return False
    
    # 7. 功能测试
    logger.info("\n7. 功能测试")
    if test_camoufox():
        logger.success("✅ Camoufox安装和配置正常！")
        logger.info("\n🎉 修复完成，现在可以正常使用项目了")
        return True
    else:
        logger.error("❌ 功能测试失败")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            logger.error("\n❌ 修复失败，请检查错误信息或联系技术支持")
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("\n用户中断操作")
        sys.exit(0)
    except Exception as e:
        logger.error(f"\n修复脚本执行失败: {e}")
        sys.exit(1)
