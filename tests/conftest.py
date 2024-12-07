from dotenv import load_dotenv


def pytest_configure(config):
    # 加载 .env 文件
    print("Loading .env file")
    load_dotenv(".env.local")
    load_dotenv(".env")
