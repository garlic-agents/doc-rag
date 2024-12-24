<div align="center">
    <h1>Document RAG Prototype</h1>
</div>

### 更新当前项目包

```shell
pip freeze > requirements.txt
```

### 安装当前项目包

```shell
# 生成当前项目虚拟安装中已安装的包
pip freeze > install_packages.txt
# 卸载当前项目虚拟安装中已安装的包
pip uninstall -r install_packages.txt -y

# 安装当前项目所需的包
pip install -r requirements.txt
```