# bash脚本编程速成

## 命令格式
shell命令基本都是`command [ arg1 ... [ argN ]]`这种形式的。`command`是某个命令或是一个可执行文件，后面的`arg`是可选参数。通常`command --help`可以看有哪些可选参数和含义。

比如
```bash
$ ls -l
```
这里ls是命令，-l是参数。
有些参数（比如这个-l）命令的*配置项*，配置项一般有长（--list）、短（-l）两种形式。

再比如
```bash
$ ls -lhta
```
配置项合并书写了。

### 多行的命令
Bash 单个命令一般都是一行，用户按下回车键，就开始执行。有些命令比较长，写成多行会有利于阅读和编辑，这时可以在**每行结尾加上`\`**，Bash 就会将下一行跟当前行放在一起解释。
```bash
$ echo foo bar

# 等同于
$ echo foo \
bar
```

### 空格
Bash 使用空格（或 Tab 键）区分不同的参数。
如果参数之间有多个空格，Bash 会自动忽略多余的空格。

### 分号
分号`;`是命令的结束符，使得一行可以放置多个命令，这一个命令执行结束后，再执行下一个。
使用分号时，命令总是顺序执行，**不管前面的命令执行成功或失败**。

### 命令组合符 `&&`和`||`
- `command1 && command2`: 先执行1，若成功则执行2；若1失败了，则不执行2。
- `command1 || command2`: 先执行1，若成功则不执行2；若1失败，则执行2。

## `type`判断命令来源
Bash 本身内置了很多命令，同时也可以执行外部程序。怎么知道一个命令是内置命令，还是外部程序呢？`type`可以判断命令是内置的还是外部的。
```bash
$ type echo
echo is a shell builtin # echo是内部命令
$ type ls
ls is hashed (/bin/ls) # ls是外部程序
$ type type
type is a shell builtin # type是内部命令
```

- `-a`:查看一个命令的所有定义。
    ```bash
    $ type -a echo
    echo is shell builtin
    echo is /usr/bin/echo
    echo is /bin/echo
    ```
    echo命令既是内置命令，也有对应的外部程序。

- `-t`:返回命令的类型，包括：别名（alias），关键词（keyword），函数（function），内置命令（builtin）和文件（file）。
    ```bash
    $ type -t bash
    file
    $ type -t if
    keyword
    ```
    上面例子中，bash是文件，if是关键词。

## 快捷键
- `Ctrl + L`：清除屏幕并将当前行移到页面顶部。
- `Ctrl + C`：中止当前正在执行的命令。
- `Shift + PageUp`：向上滚动。
- `Shift + PageDown`：向下滚动。
- `Ctrl + U`：从光标位置删除到行首。
- `Ctrl + K`：从光标位置删除到行尾。
- `Ctrl + W`：删除光标位置前一个单词。
- `Ctrl + D`：关闭 Shell 会话。
- `↑，↓`：浏览已执行命令的历史记录。
- 命令和路径自动补全：命令、路径输到一半的时候，按`Tab`键Bash会补全剩下的部分。如果有多个可能的选择，按两次Tab，Bash会显示所有可能的选项。

## `echo`输出
原样输出一行文本
```bash
$ echo hello world
hello world
```
输出多行文本要加单/双引号。

- `-n`
echo输出的文本末尾默认有一个换行符，加上`-n`可以取消换行符。
```bash
$ echo -n my name $USER; echo hhhhhhh
my name zhongying.ruhhhhhhh
```
- `-e`解释引号内的的特殊字符（比如换行符\n）。如果不使用-e参数，即默认情况下，引号会让特殊字符变成普通字符，echo不解释它们，原样输出。
```bash
$ echo "my name \n$USER"; echo -e "hhhhhhh\n233333"
my name \nzhongying.ru
hhhhhhh
233333
```
## 

