import json

from vector_db.vector_database import VectorDatabase


def test_vector_database():
    vdb = VectorDatabase()
    vdb.insert_datas(
        datas=[
            {"id": "1", "data": "北京是中国的首都，坐落于华北平原的北端"},
            {"id": "2", "data": "首尔是韩国的首都，位于韩国中部"},
            {"id": "3", "data": "东京是日本的首都，位于本州岛东部"},
        ]
    )


def test_vector_query_all():
    vdb = VectorDatabase()
    result = vdb.collection.query(
        query_texts=["测试时间为2024年7月27日（星期六）8:30至14:00"],
        n_results=4,
    )
    # json 格式化，并添加换行
    print(f"\nQuery Result: {json.dumps(result, indent=4, ensure_ascii=False)}\n")
    assert result is not None


def test_vector_delete():
    vdb = VectorDatabase()
    vdb.delete_collection_data()
