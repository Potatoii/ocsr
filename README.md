## 简介

一个后台OCSR（Optical Chemical Structure Recognition）服务器程序，专门为识别和抽取PDF或者图片文件中的化学结构式服务。

集成了**Kohulan**的DECIMER功能

[Kohulan/DECIMER-Image-Segmentation: Chemical structure detection and segmentation tool for Journal articles. (github.com)](https://github.com/Kohulan/DECIMER-Image-Segmentation)

[Kohulan/DECIMER-Image_Transformer: DECIMER: Deep Learning for Chemical Image Recognition using Efficient-Net V2 + Transformer (github.com)](https://github.com/Kohulan/DECIMER-Image_Transformer)

## 功能

1. 文件上传接口，接受图片或PDF文件，并且返回一个包含文件信息的JSON对象。
2. 识别分析接口，利用OCSR技术分析图片或PDF文件，识别和抽取化学结构式并生成一个Html文件作为结果，返回这个Html的路径。

## 开始使用

#### python虚拟环境

1. 使用任意方式创建python虚拟环境

2. ```shell
   pip install -r requirements.txt
   ```

3. ```shell
   python main.py
   ```

4. 前往http://127.0.0.1:5000/openapi.json查看接口文档

5. 使用postman之类的工具请求接口

#### Docker部署（推荐）

1. 前往https://www.python.org/ftp/python/3.10.12/Python-3.10.12.tgz下载python3.10.12压缩包并放到项目根目录

2. 如果有GPU：

   ```shell
   docker-compose -f docker-compose-gpu.yml up -d
   ```

   如果没有GPU：

   ```shell
   docker-compose up -d
   ```

3. 前往http://127.0.0.1:5000/openapi.json查看接口文档

4. 使用postman之类的工具请求接口

