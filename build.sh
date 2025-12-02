#!/bin/bash

# 設置錯誤時立即退出
set -e

echo "=== 開始製作字典流程 ==="

# 檢查 Python 3 是否安裝
if ! command -v python3 &> /dev/null; then
    echo "錯誤: 未找到 python3，請先安裝 Python 3。"
    exit 1
fi

# 檢查 zip 是否安裝
if ! command -v zip &> /dev/null; then
    echo "錯誤: 未找到 zip，請先安裝 zip 工具。"
    exit 1
fi

# 檢查必要的腳本是否存在
if [ ! -f "package.py" ]; then
    echo "錯誤: 找不到 package.py 打包腳本。"
    exit 1
fi

if [ ! -f "stardict.py" ]; then
    echo "錯誤: 找不到 stardict.py 函式庫。"
    exit 1
fi

# 檢查資料來源
if [ ! -f "ecdict.csv" ] && [ ! -f "ecdict.mini.csv" ]; then
    echo "錯誤: 找不到 ecdict.csv 或 ecdict.mini.csv 資料檔。"
    exit 1
fi

# 1. 執行 Python 打包腳本生成 .idx, .dict, .ifo
echo "[1/2] 正在生成 StarDict 格式檔案..."
python3 package.py

# 檢查生成結果
if [ -f "ecdict.idx" ] && [ -f "ecdict.dict" ] && [ -f "ecdict.ifo" ]; then
    echo "StarDict 檔案生成成功。"
else
    echo "錯誤: 檔案生成失敗。"
    exit 1
fi

# 2. 打包成 zip 檔
echo "[2/2] 正在壓縮成 ecdict.zip..."

# 如果舊的 zip 存在則刪除
if [ -f "ecdict.zip" ]; then
    rm ecdict.zip
fi

# 執行壓縮
zip ecdict.zip ecdict.idx ecdict.dict ecdict.ifo

echo "=== 完成！ ==="
echo "字典檔已建立於: $(pwd)/ecdict.zip"
ls -lh ecdict.zip
