# 一键启动
在安装好docker和docker-compose后(安装方法见根目录README)，
使用命令行`cd`到当前目录下(`crawl/`)

使用命令一键启动python和mysql服务（`$` 代表命令行）

    $ docker-compose up -d --build

等镜像和容器构建成功，服务便自动运行。可以使用如下命令查看所有已经启动的容器。

    $ docker ps
    
如果python和mysql服务都正常启动，那么爬取已经自动开始。

# 查看输出
为了监控python的一些输出内容，在crawl目录下，使用如下命令可以查看实时输出：

    $ docker-compose logs -ft python
    
# 关闭
使用如下命令可以关闭所有容器：

    $ docker rm -f $(docker ps -qa)

删除所有镜像：

    $ docker rmi $(docker images -qa)
    
