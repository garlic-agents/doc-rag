from documents import DocumentParser


def test_docx_parser():
    docx_file_path = "./.data/2024年7月27日深市交易结算系统全网测试方案.docx"
    document_parser = DocumentParser(path=docx_file_path)
    parsed_data = document_parser.parse()

    for document in parsed_data:
        print(document)

    assert parsed_data is not None
    assert len(parsed_data) > 0
