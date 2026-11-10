#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""扩展脚本模板。

复制到 `<skill basedir>/../pdfkit-extension/scripts/<命令名>.py` 后修改四个常量
和 handler 即可被 pdfkit 自动发现：

    mkdir -p <skill basedir>/../pdfkit-extension/scripts
    cp <skill basedir>/scripts/pdfkit/extension_template.py \
       <skill basedir>/../pdfkit-extension/scripts/my_script.py

发现逻辑见 scripts/pdfkit.py 的 _discover_extensions()：该目录下所有非 `_` 开头
的 .py 会被按文件路径加载，读取 COMMAND / DESCRIPTION / PARAMS / handler。
文件名应与 COMMAND 一致，缺失 COMMAND 时退回文件名。
"""

COMMAND = "my_extension"              # 命令名
DESCRIPTION = "我的自定义 PDF 扩展"     # 描述
CATEGORY = "extension"                # 分类

PARAMS = [
    {"name": "input",  "type": "str", "required": True,  "help": "输入 PDF"},
    {"name": "output", "type": "str", "required": True,  "help": "输出 PDF"},
]


def handler(params):
    """处理逻辑。

    params 是已按 PARAMS 解析好的 dict，键与 PARAMS 的 name 一致。
    返回 dict；调用方按 JSON 打印结果。
    """
    # 处理逻辑...
    return {"message": "done", "output": params["output"]}
