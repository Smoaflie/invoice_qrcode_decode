<p align="center">
  <img src="static/images/logo.png" alt="Logo" width="80" height="80">
  <h3 align="center">发票二维码识别工具(分组工具)</h3>
  <p align="center">
    通过调用手机摄像头扫描发票二维码，将数据传回上位机，通过GUI界面对发票进行分组
    <br />
    <br />
    <a href="https://github.com/Smoaflie/invoice_qrcode_decode/issues">报告Bug</a>
    ·
    <a href="https://github.com/Smoaflie/invoice_qrcode_decode/issues">提出新特性</a>
  </p>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

### 介绍

大部分代码借助LLM生成

该仓库主要是作为另一个项目[发票收集工具](https://github.com/Smoaflie/invoice_collection)的辅助工具

### 界面展示

![pc](static\images\pc.png)

![app](static\images\app.png)

###### **使用方法**

1. 编译或在Release页下载.apk文件,安装到手机上并启动

2. 授予APP相机权限

3. 启动服务端

   ```bash
   git clone https://github.com/Smoaflie/invoice_qrcode_decode
   cd invoice_qrcode_decode
   pip install -r requirements
   python server.py
   ```

   观察启动消息

   ```bash
   ...
    * Running on all addresses (0.0.0.0)
    * Running on http://127.0.0.1:5000
    * Running on http://192.168.2.53:5000
   Press CTRL+C to quit
   ```

   将 192.168.2.53:5000 填到APP相应项内

4. enjoy

###### **操作说明**

- ~~GUI和APP的操作办法应该够直观了~~

- GUI上分好组后的发票导出后的格式包含很多无关信息，需通过`extract.py`脚本二次处理

  ```bash
  python extract.py xxx.json {这里填你希望生成的标签名}
  ```

  相关发票数据会按照如下格式存储到`xxx_extract.json`文件

  ```json
  [
    {
      "24312000000358032546": "ABC_1"
    },
    {
      "25442000000336446142": "ABC_2",
      "25312000000175737045": "ABC_2",
      "25952000000090584189": "ABC_2",
      "25322000000178192752": "ABC_2",
      "15809330": "ABC_2"
    }
  ]
  ```

  经过简单的修改，就能作为[发票收集工具](https://github.com/Smoaflie/invoice_collection)分组功能的参数文件

### 文件目录说明

```
invoice_QRcode_decode/
├── QRCodeDecode/              # 📦 Android Studio项目
├── server.py                  # 服务端
├── extract.py                 # 格式化工具(配合项目invoice_qrcode_decode)
├── README.md                  # 项目说明文档

```


### 作者

[@smoaflie](https://github.com/Smoaflie)

mail: smoaflie@outlook.com

qq: 1373987167  

### 鸣谢

- [Best_README_template](https://github.com/shaojintian/Best_README_template)
- [Img Shields](https://shields.io)
- [Choose an Open Source License](https://choosealicense.com)
- [Freepik](https://www.flaticon.com/authors/freepik) - The author of logo

### 版权说明

该项目签署了MIT 授权许可，详情请参阅 [LICENSE](https://github.com/Smoaflie/invoice_qrcode_decode/blob/master/LICENSE)



<!-- links -->

[contributors-shield]: https://img.shields.io/github/contributors/Smoaflie/invoice_qrcode_decode.svg?style=flat-square
[contributors-url]: https://github.com/Smoaflie/invoice_qrcode_decode/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Smoaflie/invoice_qrcode_decode.svg?style=flat-square
[forks-url]: https://github.com/Smoaflie/invoice_qrcode_decode/network/members
[stars-shield]: https://img.shields.io/github/stars/Smoaflie/invoice_qrcode_decode.svg?style=flat-square
[stars-url]: https://github.com/Smoaflie/invoice_qrcode_decode/stargazers
[issues-shield]: https://img.shields.io/github/issues/Smoaflie/invoice_qrcode_decode.svg?style=flat-square
[issues-url]: https://img.shields.io/github/issues/Smoaflie/invoice_qrcode_decode.svg
[license-shield]: https://img.shields.io/github/license/Smoaflie/invoice_qrcode_decode.svg?style=flat-square
[license-url]: https://github.com/Smoaflie/invoice_qrcode_decode/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/shaojintian

