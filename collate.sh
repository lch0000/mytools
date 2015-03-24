#!/bin/bash
shellpath=`dirname $0`
echo $shellpath
cd $shellpath
mv *.pdf *.txt *.wps *.doc *.xls *.xlsx *.ppt *.chm -t ./资料
mv *.png ./屏幕截图
mv *.rar *.zip *.tar.gz -t ./压缩包
mv *.html ./网页收藏夹备份
mv *.app *.apk ./app
mv *.jpg *.gif -t ./图片
if [ -z "$1" ]; then
    printf "无参数，只整理默认后缀文件"
else
    mkdir ./$1 && mv *.$1 -t ./$1
fi
