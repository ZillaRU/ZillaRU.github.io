# C++编译链接与构建系统详解：从g++到Make和CMake

> g++ 是编译器，直接处理代码的编译和链接；make 是一个构建工具，自动化了使用 g++ 的构建过程；而 CMake 是一个构建系统生成器，它可以创建用于不同平台和构建工具的构建文件，使得跨平台构建和项目维护更加容易。在复杂项目中，CMake 和 make 通常一起使用，CMake 生成 Makefile，然后 make 根据这些文件来编译和链接项目。

## C++编译与链接过程
C++的编译过程可以分为四个主要步骤：预处理、编译、汇编和链接。
- 预处理：预处理器处理源代码文件，处理所有以#开头的指令，如宏定义和文件包含。
- 编译：编译器将预处理后的代码转换成汇编指令。
- 汇编：汇编器将汇编指令转换为机器可读的二进制指令（目标代码）。
- 链接：链接器将多个目标代码文件合并，并解决代码之间的引用和依赖，生成最终的可执行文件。

## g++：GNU C++编译器
g++是GNU项目的C++编译器，它可以自动完成上述的编译链接过程。一个简单的使用示例如下：

```bash
g++ -c source1.cpp -o source1.o
g++ -c source2.cpp -o source2.o
g++ source1.o source2.o -o application
```
这里，-c标志告诉g++仅进行编译不进行链接，生成.o目标文件；最后一个命令则进行链接，生成可执行文件application。

* 常用的选项：
    - `-c`：只编译和汇编，但不链接。
    - `-g`：包含调试信息，这对于使用gdb等调试工具很有用。
    - `-Wall`、`-Wextra`、`-Werror`：打开额外的警告，将警告视为错误。
    - `-O0`、`-O1`、`-O2`、`-O3`：设置不同的优化级别。
    - `-std=c++11`、`-std=c++14`、`-std=c++17`：指定使用特定的C++标准。
* 例子
    - 编译单个文件：`g++ -c file.cpp`，只编译file.cpp，生成file.o目标文件，但不进行链接。
    - 编译并链接多个文件：`g++ file1.cpp file2.cpp -o app`，编译并链接file1.cpp和file2.cpp，生成可执行文件app。
    - 设置优化级别：`g++ -O2 file.cpp -o app`，-O2选项启用了中等优化，通常用于生产编译，以保证代码执行的效率。
    - 启用所有警告并处理警告为错误：`g++ -Wall -Werror file.cpp -o app`，-Wall打开所有的警告，-Werror将所有警告当作错误处理。
    - 指定标准库版本：`g++ -std=c++17 file.cpp -o app`，-std=c++17指定使用C++17标准进行编译。
    - 链接库文件：`g++ file.cpp -o app -L/lib/dir -lname`，-L用于指定库文件搜索目录，-l用于指定链接的库名。

## make：自动化构建工具
在简单的项目中，你可以直接使用 g++ 命令来编译和链接你的程序，但这种方法在项目变得更加复杂时会变得难以管理。Make工具和Makefile脚本可以自动化编译和链接过程。

Make 是一个工具，它使用一个名为 Makefile 的文件，该文件定义了如何编译和链接程序。Makefile 包含了一系列的规则和依赖关系，告诉 make 如何构建目标（如可执行文件或库）。

使用 make 的优势包括：
- 自动化构建：你只需输入 make 命令，它就会根据 Makefile 中的规则自动编译和链接源代码。
- 增量构建：make 可以检测哪些文件被修改，并且只重新编译那些改变了的文件，这可以节省大量的构建时间。
- 定制化构建规则：你可以在 Makefile 中编写复杂的规则，以处理特殊的构建需求。

### make工具常用命令
- 运行默认目标：`make`
- 运行特定目标：`make target_name`
- 清理构建产物：`make clean`

### Makefile的常见写法
Makefile 是 Make 工具使用的文件，用于自动化编译和链接程序。它定义了一系列的规则来指定如何生成目标文件和执行任务。

* 基本组成
    - 目标（Targets）：通常是文件名，代表了构建系统需要创建的文件。
    - 依赖（Dependencies）：目标文件依赖的文件列表，这些文件是生成目标所需的。
    - 规则（Rules）：如何从依赖生成目标的具体命令。

* 格式
    ```makefile
    target: dependencies
        recipe
    ```
    - target：你想要生成的文件。
    - dependencies：生成该目标所需要的文件或目标。
    - recipe：生成目标所需执行的命令，必须以一个Tab键开始。

* 一个例子
    ```makefile
    # 变量定义
    CC=gcc
    CFLAGS=-I.

    app: main.o utils.o
        $(CC) main.o utils.o -o app # 使用变量 $(varname)

    main.o: main.c
        $(CC) -c main.c

    utils.o: utils.c
        $(CC) -c utils.c

    clean:
        rm -f *.o app
    ```
    在这个例子中，目标 app 依赖于 main.o 和 utils.o。`make app`会编译这两个对象文件，并链接它们生成最终的可执行文件 app。`make clean`会清理所有构建生成的文件。

## CMake：跨平台构建系统
编写和维护 Makefile 可能会变得复杂，尤其是在跨平台的项目中。CMake是一个更高级别的构建系统，它使用平台无关的 CMakeLists.txt 文件来描述构建过程，并且可以生成适用于不同平台的 Makefile 或其他构建脚本。

CMake 的优势包括：
- 跨平台支持：CMake 可以为多种平台生成构建文件，包括 Unix、Windows 和 macOS。
- 易于维护：CMakeLists.txt 文件通常比 Makefile 更简洁、更易于理解和维护。
- 高级功能：CMake 提供了高级功能，如自动查找库依赖、生成安装脚本、进行测试等。
- IDE集成：许多集成开发环境（IDE）支持 CMake，可以直接从 CMakeLists.txt 文件中导入项目。

### 常用命令
- 生成构建系统文件：`cmake path_to_source`
- 构建项目（在构建目录中）：`cmake --build .`
- 指定构建类型（例如：Release或Debug）：`cmake -DCMAKE_BUILD_TYPE=Release path_to_source`

### CMakeLists.txt写法
CMakeLists.txt文件用于定义构建过程。

#### 基本命令
- `cmake_minimum_required`、`project`、`set` 等命令用于设置项目的基本信息。
- 指定C++标准：`set`命令用于指定所需的C++标准。
- 添加可执行文件：
- `add_executable` 命令用于定义一个从源文件构建的可执行文件。
- 添加库文件：
`add_library` 命令用于创建一个库（动态或静态）。
- 链接库：
`target_link_libraries` 命令用于指定可执行文件或库需要链接的其他库。

#### 高级功能
- 定义变量：使用set命令可以定义一个变量。`set(MY_VARIABLE "SomeValue")`；之后，你可以使用`${MY_VARIABLE}`来引用这个变量的值。
- 使用条件语句进行条件编译或配置：
    ```cmake
    if(MY_VARIABLE STREQUAL "Hello, CMake!")
        message(STATUS "Variable is set correctly.")
    else()
        message(STATUS "Variable is not set correctly.")
    endif()
    ```
- 定义函数：CMake允许你定义自己的函数，这对于复用代码非常有用。
    ```cmake
    function(my_function arg1 arg2)
        message(STATUS "Calling my_function with arguments: ${arg1} and ${arg2}")
        # 函数内部的其他命令...
    endfunction()
    ```
    然后，你可以像这样调用你的函数：
`my_function(Value1 Value2)`

- 命令行设置参数：在命令行中，你可以通过传递-D选项给cmake命令来设置参数。
`cmake -DMY_VARIABLE=MyValue path_to_source`，这将在CMake的配置阶段设置MY_VARIABLE为MyValue。


### 处理嵌套文件夹和多个CMakeLists.txt文件
当你的项目结构变得更加复杂，包含多个目录时，你通常会在每个目录中放置一个CMakeLists.txt文件。CMake支持在主CMakeLists.txt文件中使用add_subdirectory命令来包含这些子目录。

每个子目录的CMakeLists.txt将定义该目录中的构建规则。这样，你可以组织代码和构建逻辑，使它们局部化和模块化。

假设你有一个项目，它的结构如下：
```bash
/MyProject
  CMakeLists.txt
  /src
    CMakeLists.txt
    main.cpp
  /lib
    CMakeLists.txt
    mylib.cpp
```

在根目录的CMakeLists.txt中，你会包含src和lib目录：

```cmake
cmake_minimum_required(VERSION 3.10)
project(MyProject VERSION 1.0)

# 添加子目录
add_subdirectory(src)
add_subdirectory(lib)
```

在src目录的CMakeLists.txt中，你可能会添加一个可执行文件：

```cmake
add_executable(program main.cpp)

# 假设我们想链接在lib目录中定义的库
target_link_libraries(program PRIVATE mylib)
```
在lib目录的CMakeLists.txt中，你可以添加一个库：
```cmake
add_library(mylib STATIC mylib.cpp)
```
CMake会递归地处理这些CMakeLists.txt文件，根据每个目录中定义的规则来构建项目。

### .cmake 文件
.cmake 文件是CMake的模块或脚本文件，它包含了可以被CMake进程所使用的CMake命令和宏定义。这些文件通常用于以下几个目的：

- 模块(Module): CMake模块是包含了一组预先定义的函数和宏的文件，这些可以被其他CMake脚本通过`include()`或`find_package()`命令所使用。模块通常用于查找库文件、程序、线程等，并且可以设置必要的编译器标志或变量。

- 包配置文件(Package Configuration): 这些.cmake文件提供了包的配置信息，使得其他项目可以通过`find_package()`命令找到并正确链接使用这些包。

- 工具链文件(Toolchain Files): 当进行交叉编译时，工具链文件包含了必须由CMake使用的编译器和工具的信息。

- 包含文件(Include Files): 与编程语言中的头文件类似，.cmake文件可以被其他CMake脚本包含，以复用代码和逻辑。

- 脚本(Scripts): .cmake 文件也可以包含可以独立执行的CMake脚本，这些脚本可以执行特定任务，如安装脚本、测试脚本等。

在项目中，.cmake 文件通常被组织在项目的cmake目录下，并且在`主CMakeLists.txt`文件或`其他CMakeLists.txt`文件中通过相应的命令引入。这样做可以提高项目的可维护性和模块化水平，也便于共享和重用CMake代码。