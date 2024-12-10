import os
from typing import List

import mammoth
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from markdownify import markdownify as md2txt

from vector_db.vector_database import VectorDBData


# 将 docx 转换为 markdown
def convert_docx_to_markdown(docx_path) -> str:
    """
    将 docx 文件转换为 markdown 格式
    1. 首先使用 mammoth 将 docx 转换为 HTML
    2. 然后使用 markdownify 将 HTML 转换为 Markdown
    """
    # 配置 mammoth 转换选项
    style_map = """
        p[style-name='Quote'] => blockquote:fresh
        p[style-name='Code'] => pre:fresh
    """

    try:
        with open(docx_path, "rb") as docx_file:
            # 步骤1：转换为HTML
            result = mammoth.convert_to_html(docx_file, style_map=style_map)
            html = result.value

            # 输出任何警告信息
            if result.messages:
                print("转换警告：")
                for message in result.messages:
                    print(message)

            # 步骤2：将HTML转换为Markdown
            # heading_style可以是"ATX"（使用#）或"SETEXT"（使用=和-）
            markdown_text = md2txt(
                html,
                heading_style="ATX",  # ATX 样式的标题 (### 这种)
                bullets="-",  # 无序列表使用 -
                strip=['script', 'style'],  # 移除script和style标签
                code_language="python"  # 代码块的默认语言
            )

            return markdown_text

    except Exception as e:
        print(f"转换过程中出现错误: {str(e)}")
        raise


def dedoc_metadata_to_vector_metadata(metadata: dict) -> dict:
    return {
        "title": metadata.get("title", ""),
        "type": metadata.get("type", ""),
        "text_as_html": metadata.get("text_as_html", ""),
    }


# 文档解析器
class DocumentParser:

    # 初始化
    def __init__(self, path: str):
        self.path = path
        if not path:
            raise Exception("文件路径不能为空")
        if not os.path.exists(path):
            raise Exception("文件不存在")

    # 解析文档
    def parse(self) -> List[VectorDBData]:
        # 判断文件的类型
        if self.path.endswith(".docx"):
            # docx 文件解析
            # 1. 将 docx 文件转换为 markdown
            markdown_text = convert_docx_to_markdown(self.path)
            # 2. 配置分割器
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""],
                keep_separator=True
            )
            # 4. 使用转换的md内容，创建 Document 对象用于分块
            document_data = Document(page_content=markdown_text)
            # 5. 使用分割器实现文本分块
            chunks = text_splitter.split_documents([document_data])
            # 6. 将分块转换为 VectorDBData 用于储存到向量数据库中
            vector_db_data_list: List[VectorDBData] = list()
            for index, chunk in enumerate(chunks):
                print(f"块 {index} 长度：{len(chunk.page_content)}")
                if len(chunk.page_content) <= 0:
                    continue
                vector_db_data_list.append({
                    "id": f"{index}",
                    "data": chunk.page_content,
                })
            print(f"分块数为：{len(vector_db_data_list)}")
            return vector_db_data_list
        else:
            raise Exception("不支持的文件类型")
