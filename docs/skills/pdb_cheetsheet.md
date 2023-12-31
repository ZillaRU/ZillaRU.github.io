# pdb调试方法及高级使用技巧

## 使用场景
相比较pdb调试，IDE调试可视化更好。
使用pdb调试的场景也有很多，比如：
1. IDE调试不方便，比如在服务器上调试，或者在远程服务器上调试，或者在docker容器中调试。
2. 大项目调试，比如django项目，需要在多个文件中调试，IDE调试不方便。

## 用法

1. **侵入式**：不用额外修改源代码，在命令行下直接`python3 -m pdb filename.py`就能调试
2. **非侵入式**：需要在被调试的代码中添加一行`import pdb;pdb.set_trace()`然后再正常运行代码

当你在命令行看到`(Pdb)`这个提示符时，说明已经正确进入了pdb，就使用下面这些命令了。

## pdb常用命令
### 断点 (建议使用绝对地址)
前一个xxx是py文件的**路径**，后一个xxx是**行号**。
1. 打断点
   - 输入`b xxx.py:xxx`设置断点。
   - 输入`b funcname`在函数执行的第一行设置断点。
   - 输入`b xxx.py:xxx if xxx`设置**条件断点**，需要说明的是这是pdb.set_trace()很难直接做到的。
   - 输入`tbreak xxx.py:xxx`设置**临时断点**，这个断点会在第一次触发后自动删除。

2. 清除断点
    - 输入`cl xxx.py:xxx`清除断点。
    - 输入`cl all`清除所有断点。

3. 查看堆栈信息`bt`,用 ↑ 和 ↓ 按键可以在堆栈中移动。
4. 查看当前执行的源码周围10行代码`l` (list)
5. 查看变量、保存变量等各种操作
   - `p expression`： expression是Python语句，可以用来查看变量，保存中间结果用于复现
     - 比如p img.save('test.png')、p np.save('latents.npy',latents)
   - 打印变量类型`whatis expression`
   - 查看函数参数和参数的值`a`
  
6. 逐行调试命令
    ```
    s   //执行下一行（能够进入函数体）
    n   //next 执行下一行（不会进入函数体）
    r   //执行下一行（在函数中时会直接执行到函数返回处）
    ```
7. 非逐行调试命令
    ```
    c           //持续执行下去，直到遇到一个断点
    unt lineno  //持续执行直到运行到指定行（或遇到断点）
    j  lineno   //直接跳转到指定行（注意，被跳过的代码不执行）
    ```
8. 退出pdb：`q`

## 高级技巧
- 调试多线程：针对多线程，需要在每个线程中都添加断点，然后在进入pdb时，输入`thread xxx`切换到指定线程。
- 查看变量是否具有某个或者某些属性：在进入pdb时，输入`hasattr(xxx, 'xxx')`查看变量是否具有某个或者某些属性。或者使用`dir(xxx)`查看变量的所有属性。
- `t=lambda x:fun(x)：（lambda）` 执行lambda表达式一行出结果，但是需要考虑到pdb中的lambda之间不具有上下文语义，所以需要使用lambda x:fun(x)的形式，lambda不要串联。