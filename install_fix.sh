#!/bin/bash
# Camoufox安装修复脚本

echo "🔧 开始修复Camoufox安装问题..."

# 检查Python版本
python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
echo "Python版本: $python_version"

# 卸载并重新安装camoufox
echo "📦 卸载现有camoufox..."
pip uninstall camoufox -y

echo "🧹 清理pip缓存..."
pip cache purge

echo "📥 重新安装camoufox..."
pip install camoufox>=0.2.0 --force-reinstall --no-cache-dir

echo "📥 安装playwright浏览器..."
python3 -m playwright install

echo "🧪 运行诊断脚本..."
python3 fix_camoufox.py

echo "✅ 修复完成！"
