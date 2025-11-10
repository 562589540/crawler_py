@echo off
echo 🔧 开始修复Camoufox安装问题...

REM 检查Python版本
python --version

REM 卸载并重新安装camoufox
echo 📦 卸载现有camoufox...
pip uninstall camoufox -y

echo 🧹 清理pip缓存...
pip cache purge

echo 📥 重新安装camoufox...
pip install camoufox>=0.2.0 --force-reinstall --no-cache-dir

echo 📥 安装playwright浏览器...
python -m playwright install

echo 🧪 运行诊断脚本...
python fix_camoufox.py

echo ✅ 修复完成！
pause
