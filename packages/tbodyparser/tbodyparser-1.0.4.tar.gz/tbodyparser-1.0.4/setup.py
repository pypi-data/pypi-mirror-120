import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tbodyparser",  # 项目名称
    version="1.0.4",  # 项目版本
    author="MrBigB",  # 项目作者
    author_email="lowbeeland@163.com",  # 作者邮箱
    description="web table body parser based on pyquery",  # 项目描述
    long_description=long_description,  # 项目详细描写
    long_description_content_type="text/markdown",  # 项目详细描述文件类型
    url="https://github.com/MrBigBlake/tbodyparser",  # 项目地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # python版本要求
    install_requires=["pyquery"]  # 项目其他依赖
)
