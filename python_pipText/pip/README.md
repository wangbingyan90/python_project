### 发布项目到pip
1. 注册一个pypi账号
https://pypi.org/

2.编写一个自己的python 项目

    项目文档
        setup.py
        .pypirc
        项目名称文档
            _init_.py
            项目文件

3.本地打包项目文件

    python setup.py sdist

4.上传项目到pypi服务器

    twine upload dist/。。

5.使用

    pip install 项目名