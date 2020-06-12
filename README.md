# Background
该项目是数据科学导论作业，根据课程学习内容对bilibili部分信息进行爬取、处理、分析、展示。本项目仅为学术研究。

# Install
项目主要使用python撰写，所需python包均会导出在代码目录下requirements.txt中。安装所需包请使用

    $ pip install -r requirements.txt

在爬虫部分`./codes/crawl-preprocess-storage/crawl`使用docker部署了python和mysql服务，
并在程序中设置了定时任务。为了运行crawl部分代码，请安装docker和docker-compose

[windows docker 安装教程](https://www.runoob.com/docker/windows-docker-install.html)

[Mac docker 安装教程](https://www.runoob.com/docker/macos-docker-install.html)

安装toolbox后已经自带docker-compose，如果没有docker-compose需要自行安装

具体使用见crawl文件夹下`README.md`

