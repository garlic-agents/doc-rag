import os
from typing import List

from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from markitdown import MarkItDown

from vector_db.vector_database import VectorDBData


def new_docx_to_markdown(docx_path: str) -> str:
    markitdown = MarkItDown()
    result = markitdown.convert(docx_path)
    return result.text_content


def parse_docx_file(path: str) -> list[VectorDBData]:
    # docx 文件解析
    # 1. 将 docx 文件转换为 markdown
    markdown_text = new_docx_to_markdown(path)
    # 2. 配置分割器
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""],
        keep_separator=True
    )
    # 3. 使用转换的md内容，创建 Document 对象用于分块
    document_data = Document(page_content=markdown_text)
    # 4. 使用分割器实现文本分块
    chunks = text_splitter.split_documents([document_data])
    # 5. 将分块转换为 VectorDBData 用于储存到向量数据库中
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
            return parse_docx_file(self.path)
        else:
            raise Exception("不支持的文件类型")
