
# Docker使用

Docker镜像是由 Dockerfile 和一些必要的依赖项组成的，**Docker容器（container）是动态的Docker镜像（image）**。
要使用 Docker 命令，首先明确要处理镜像还是容器。
知道了要处理镜像还是容器，才可以找到正确的命令。

- 在docker1.13之后的版本，Docker CLI 管理命令以**docker**开头，接着是**管理类别**，最后是**命令和可选项**，即`docker <object> <command> <options>`。比如停止容器的命令，`docker container stop`。管理类别可以是container、image、network、volume。也可以不写管理类别使用老版本的命令格式，个别命令可能稍有不同，可以--help具体看。
- 引用特定容器或镜像的命令需要该容器或镜像的**名称或 ID**。

### 容器命令
`docker container [command]`
这些命令后面加`--help`可以看具体有什么option。

- 从镜像**创建**容器 `create`
    
    `docker container create [my_repo]/[my_image]:[my_tag]`
    [my_repo]/[my_image]:[my_tag]可以简写为[my_image]

- **启动**已有镜像 `start`
    
    `docker container start [container_ID or container_name]`
- **重启**已有镜像 `restart`
- **创建新容器并启动**
  - `docker container run [my_image]`或者`docker run [my_image]`，这个命令选项非常多，可参考[LINK](https://www.runoob.com/docker/docker-run-command.html)。常用的有：

    - -t：为容器重新分配一个伪输入终端，通常与 -i 同时使用
    - -i：以交互模式运行容器
    - -m：设置容器使用内存的最大值
    - --expose=[]: 开放一个端口或一组端口
    - -a stdin：指定标准输入输出内容类型，可选 STDIN/STDOUT/STDERR三项
    - -P: 随机端口映射，容器内部端口随机映射到主机的端口
    - -p: 指定端口映射，格式为：主机(宿主)端口:容器端口
    - --name：指定容器名称
    - -d：后台运行容器并返回容器ID
    - --rm：在容器退出时自动清理容器内部的文件系统，等价于在容器退出后执行`docker rm -v`（用于前台运行的容器，和-d同时用没意义）
   
    举几个例子：

    1. `docker container run -i -t -p 1000:8000 --rm my_image`:
        -i 是—interactive 的缩写，即使未连接，也要保持 STDIN 打开；-t 是—tty 的缩写，它会分配一个伪终端，将终端与容器的 STDIN 和 STDOUT 连接起来。你**需要指定-i 和-t 通过终端 shell 与容器交互**。-p 是 –port 的缩写。端口是与外部世界的接口。1000：8000 将 Docker 端口 8000 映射到计算机上的端口 1000。如果你有一个 app 输出了一些内容到浏览器，你可以将浏览器导航到 localhost:1000 并且查看它。–rm 自动删除停止运行的容器。
    2. `docker container run -d my_image`:-d 是—detach 的缩写，指在后台运行容器，允许您在容器运行时将终端用于其他命令。
    3. `docker container run -it my_image sh`:这个命令创建并运行一个容器，并在内部启动一个shell会话。这里的sh也可以换成其他需要在容器内执行的命令。
    4. `docker run --cap-add SYS_ADMIN -itd --restart always -p 1100$num:7019 --device /dev/bmdev-ctl --device=/dev/bm-sophon$device:/dev/bm-sophon0 --log-opt max-size=16g --log-opt max-file=1 -v /home/user/aigc/models/models-01/models:/workspace/models -v /home/user/aigc/aaaigc/aigc:/workspace -w /workspace --name aigc$num sophon/aigc:test bash run.sh` 在docker1.13版之前，只能用这样的命令，-v用于挂载目录，-w指定工作目录
 
- `docker exec`：在运行的容器中执行命令，格式是`docker <object> <command> <options>`。
- `docker container ls`或`docker ps`: 列出（默认是：运行中的）容器,要列出所有容器需要加`-a`。
- 查看容器信息 `docker inspect 容器名称/id`
- 打印日志 `docker logs 容器名称/id`: 日志默认是截止到目前为止的日志。如果想要持续看到新打印出的日志信息，那么可以加上-f。
- `docker stats`: **实时**看容器的**资源占用**情况，默认列出所有运行中容器。
- 停止容器
  - 停止正在运行的容器 `docker stop 容器名称/id`
    - 优雅地停止一个或多个正在运行的容器。在容器关闭之前提供默认 10 秒以完成任何进程。
  - 立即停止容器中的主要进程 `docker kill 容器名称/id`
    - 例：`docker container kill $(docker ps -q)`终止所有运行中的容器
- 删除已经停止的容器 `docker rm 容器名称/id`
  - 例：`docker container rm $(docker ps -a -q)` 删除所有不在运行中的容器`


### 镜像命令

`docker image [command]`
  - 由dockerfile构建镜像 `docker build [OPTIONS] PATH | URL | -`
    - 例：`docker image build -t my_repo/my_image:my_tag .` -t 是 tag 的缩写，是告诉 docker 用提供的标签来标记镜像;`.`是告诉 Docker 根据当前工作目录中的 Dockerfile 构建镜像。
  
  - 推送镜像到远程镜像仓库 `docker image push my_repo/my_image:my_tag`
  - 拉取镜像 `docker image pull [OPTIONS] NAME[:TAG|@DIGEST]`
    - 可以获取指定编译平台的镜像 `docker pull --platform=arm64|amd64... image_name`
  - 列出镜像 `docker image ls`
  - 查看中间镜像信息(大小、创建方式等) `docker image history my_image`
  - 查看镜像信息（包括层等细节） `docker image inspect my_image`
  - 删除指定镜像`docker image rm my_image`,如果镜像被保存在镜像仓库中，那么该镜像在那依旧可用。
    - 例：`docker image rm $(docker images -a -q)` 删除所有镜像。必须小心使用这一命令。已经被推送到远程仓库的镜像依然能够保存，这是镜像仓库的一个优势。

### 其他
- 查看docker版本信息 `docker version`
- 登录到docker镜像仓库 `docker login`,根据提示键入你的用户名和密码。
- 删除所有未使用的容器、网络以及无名称的镜像（虚悬镜像）`docker system prune`。

