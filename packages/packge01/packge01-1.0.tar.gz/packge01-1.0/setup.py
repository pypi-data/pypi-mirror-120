import setuptools #模块
with open("README.md","rb") as f:
    description = f.read().decode("utf-8")


setuptools.setup(
    name="packge01",
    version="1.0",
    packages=setuptools.find_packages(),
    author="laozhang",
    description="一个打包案例",
    long_desctription=description,
    pyhon_requires=">=3.7"
)
# print(description)
