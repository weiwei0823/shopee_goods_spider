## 简介
本指南提供了部署一个专注于Python 3.7-3.8的网络爬虫工具的说明。该工具需要安装以下几个依赖：fake_useragent、httpx、redis、requests、threadpool和tqdm。

## 环境设置
### 激活虚拟环境
在根目录下，通过以下命令在终端中激活虚拟环境：

```bash
.\venv\Scripts\activate
```

### 安装必要的依赖
通过以下命令在终端中安装所需的依赖：

```bash
pip install -r requirements
```

## 部署步骤
按照以下步骤部署网络爬虫工具：

1. **配置配置文件：** 在配置文件中指定主机和检查点参数。

2. **启用IP支持（可选）：** 启动change_ip_windows_timely.py脚本以启用IP支持。如果不需要IP支持，可以修改配置文件。

3. **运行工具：** 在终端中运行以下命令启动工具：

```bash
python main_get_products_by_cat.py --host sg
```

使用可选的`--check_point`参数从上一次运行中恢复进度。

*注意：除非更新分类，否则不需要执行步骤A和B。*

## 更新分类
如果需要更新分类，请执行以下步骤：

A. **获取分类**

- 运行1.get_third(facet)_category.py以收集所有原始分类信息。
- 运行2.create_tree_last.py根据自定义JSON逻辑解析信息。

B. **手动修改分类信息**

- 在代码中修改网络请求URL，方法是打开Shopee网站的主页和单个分类页面。
- 将生成的spider_categories.json文件手动放入根目录下的category_info文件夹中。

## 目录结构

```
E:.
├─catagories
│  ├─category_info        # 存储所有与站点相关的分类信息；请勿修改或启动此文件夹
│  ├─check_point          # 进度检查点存储
│  ├─data
│  │  ├─products          # 存储与关键词相关的店铺级别产品信息
│  │  │  ├─polymerization_products # 以下是每个平台的信息存储
│  ├─external_api         # 监控API接口
│  ├─tools                # 工具包
│  ├─main_get_products_by_cat.py # 主文件
│  ├─1.get_third(facet)_category.py # 获取原始分类信息
│  ├─2.create_tree_last.py # 根据原始分类信息进行解析
│  ├─3.ac_cert_d.txt      # Cookie；当此参数无效时更新
│  ├─change_ip_windows_timely.py # 自动更新脚本
│  ├─get_backups.py       # 获取后端提供的分类任务
│  ├─selenium_capture    # 与Super English CAPTCHA对接的文件
│  ├─...
│  └─...
└─venv                    # 虚拟环境文件
   └─Lib                  # 虚拟环境依赖
      └─site-packages
```

## 版本历史
- V1.0.0：实现了跨所有平台的正常采集。注意：处理验证码是必要的，但在采集少量数据时可以忽略。台湾站点的IP代理比较复杂。

请注意，目录结构和文件名可能根据实际实现而变化。在部署过程中，请确保相应地进行调整。
