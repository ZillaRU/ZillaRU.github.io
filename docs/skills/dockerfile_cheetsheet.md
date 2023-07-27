# Dockerfile编写
[参考](https://zhuanlan.zhihu.com/p/105885669)

# Dockerfile编写

刚开始接触docker，我们会用docker pull拉取现成的镜像，或者用docker exec、docker run这些命令进入容器做一些配置修来构建容器，而dockerfile是一个一劳永逸的镜像构建方法。通过编写dockerfile我们可以构建自己的镜像。**dockerfile可以类比python pip的requirements.txt文件**，docker build可以类比pip install。

## Dockerfile语法

Dockerfile由一行行命令语句组成，注释以`#`开头。完整的dockerfile应当包含以下部分：
1. `FROM 基础镜像`，表示以哪个镜像为基础去定制镜像。比如`FROM postgres:latest`

2. `LABEL maintainer="个人信息"`，表示这个镜像是由谁制作的，可以写名字或者邮箱，这个语句写在FROM之后
3. 镜像的操作命令，比如安装依赖、修改配置等对基础镜像的修改。一般是`RUN 具体命令`的形式。**RUN操作默认sudo权限。**多个RUN操作之间用`&&`连起来**合并在一行**，因为每执行一次RUN就会在docker上新建一层镜像，所以分开来写很多个RUN的结果就是会导致整个镜像无意义的过大膨胀。例：`bash RUN apt-get update && apt-get install vim`
4. **容器启动时执行的命令** 需要用`CMD`来执行一些容器启动时的命令，注意与`RUN`的区别，**CMD是在docker run执行的时候使用**，而**RUN则是在docker build的时候使用**。CMD指令的首要目的在于为启动的容器指定默认要运行的程序，且其运行结束后，容器也将终止;不过，CMD指定的命令其可以被docker run的命令行选项所覆盖。一个Dockerfile只有**最后一个CMD**会起作用。 例：`bash CMD ["/usr/bin/wc","--help"]`

此外，`COPY`、`ADD`、`ENV`、`WORKDIR`和`EXPOSE`也很常用。用法是：
```dockerfile
COPY source_dir target_dir # 复制文件
ADD source_dir或远程url target_dir # 复制文件
ENV <KEY> <VALUE> # 环境变量
EXPOSE 端口号 # 暴露端口
```

## 用dockerfile构建一个简单的镜像
下面以**构建一个简单的postgres镜像**为例，讲述用dockerfile构建镜像的过程。需求是：定制的镜像中要装好vim（docker pull 拉取的默认镜像是没有的）并且要设置好我需要的配置。
1. `docker search postgres`查找已有镜像，从中选一个作为基础镜像。这里我选了ubuntu/postgres。

2. vim新建文件，写FROM语句和maintainer
   ```dockerfile
   FROM ubuntu/postgres
   LABEL maintainer="zilla_ru"
   ```
3. 写RUN语句（在docker build执行时要做的环境准备工作）
   ```dockerfile
   # 镜像操作命令
   RUN apt-get update && apt-get install vim -y
   # 设置环境变量
   ENV POSTGRES_PASSWORD '10293847'
   # 暴露端口
   EXPOSE 5432
   ```
4. 写完Dockerfile,就可以build了，可以指定Dockerfile的路径。
   - 若是项目的Dockerfile（放在项目根目录下），直接在根目录`docker build .`就行了，docker会根据上下文找到Dockerfile。可以通过.dockerignore文件排除上下文目录下不需要的文件和目录（比如：Dockerfile里可能用到COPY或者ADD指令拷贝文件，可以ignore一些不需要的文件）。
   - 指定Dockerfile的路径`docker build -f /path/to/Dockerfile`
   - 例：`docker build -t pgsql:v1 .`, -t指定镜像tag，:前为REPOSITORY名，:后是TAG名
5. build完`docker images`或者`docker image ls`看看有没有build成功
6. 使用`docker run --name 容器名 -e POSTGRES_PASSWORD=密码 -p 5431:5432 -d pgsql:v1`运行postgres容器，`docker ps`看看有没有运行起来。
