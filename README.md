# Schedule-I-Simplified-Chinese-Patch
Schedule I简中汉化补丁

[安装教程视频](https://www.bilibili.com/video/BV1WL22BQE33)

[Youtube教程视频](https://www.youtube.com/playlist?list=PLzb7p3e2nBdWsR347u1H2mteFL4VkXw_2)


# 最新版汉化补丁
注：运行Font_SC.exe会自动备份sharedassets0.assets文件 (bak文件)
先备份原来的schedule1_data文件的sharedassets0.assets文件，再解压缩汉化补丁

如果汉化失败则使用原sharedassets0.assets文件，再运行字体替换工具Font.exe,确保字体替换成功（出现“字体替换完成 操作成功完成”提示），检查schedule 1_data文件夹的sharedassets0.assets文件是否替换成功（看文件大小和文件日期是否改变）

如果字体替换失败等问题，删掉font_SC.exe生成的sharedassets0.assets（也有可能发生错误导致没有），将font_SC.exe生成的sharedassets0.assets.bak文件的.bak后缀去掉，再次运行Font_SC.exe

# 通用版汉化补丁
由于多人反馈最新版本的补丁安装汉化失败，闪退，粉屏等问题，故上传了个通用版汉化补丁，目前各版本通用

该补丁为打包好的通用版（无schedule 1_data文件夹的sharedassets0.assets文件，增加了字体替换工具和字体文件）

安装后直接运行font_SC.exe选择字体文件替换即可，确保字体替换成功（出现“字体替换完成 操作成功完成”提示），检查schedule 1_data文件夹的sharedassets0.assets文件是否替换成功（看文件大小和文件修改时间是否改变）

每次更新就运行一次，就可以解决因为更新导致的缺字问题了，不过新内容的翻译需要新补丁了（不过放心，通用版补丁也会随游戏更新！）

注：这个字体替换工具会备份游戏原文件里的sharedassets0.asset文件（生成.bak文件），如果出问题要还原的话把替换好的sharedassets0.asset文件删掉，再把备份文件的.bak后缀删掉就可以了

font_SC.exe是用繁中字体替换工具源代码制作的简中字体替换工具，经过测试可以正常使用，如有问题请使用繁中字体替换工具，二者功能一样，仅仅运行时候显示的字体不一样

# 原理
Schedule 1_data文件夹的sharedassets0.assets文件是Unity游戏资产文件，包含游戏字体文件，但是英文字体和中文字体（包括简中和繁中）是不一样的，xuntiy-translator插件若要翻译英文成中文就需要中文字体文件，否则就会字体缺失出现仍然是英文或者口口口的情况，这也就是为什么每次游戏更新旧汉化补丁都会失效，游戏更新也更新了sharedassets0.assets文件，又变回英文字体了，这个字体替换程序就能把资产文件的英文字体替换成中文字体了，并且简繁中都适用！

替换资产字体文件也可以用这个[工具](https://github.com/HanFengRuYue/XUnityToolkit)

# 参考
[繁中补丁原帖](https://forum.gamer.com.tw/C.php?page=1&bsn=82540&snA=6)

[繁中补丁链接](https://github.com/XoF-eLtTiL/Tang-Family-Server/releases/tag/SI)

[翻译插件](https://github.com/bbepis/XUnity.AutoTranslator)

[字体替换提出方案](https://forum.gamer.com.tw/Co.php?bsn=82540&sn=35)

[繁中字体替换工具及源代码](https://drive.google.com/drive/folders/1YUBnhHULnlY8l48rvEkuJR_zOGbtH9WT)
