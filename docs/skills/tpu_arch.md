# 加速模型推理：理解TPU架构中的关键概念

> 参考：[TPUKernel 用户开发文档 【Sophgo doc】](https://doc.sophgo.com/sdk-docs/v23.05.01/docs_latest_release/docs/tpu_kernel/reference/html/index.html)
在人工智能的快速发展中，专用硬件的需求日益增长。为了加速深度学习模型的训练和推理，出现了各种专用处理器，如TPU（Tensor Processing Unit）和NPU（Neural Processing Unit）。这些处理器专为机器学习任务优化，提供了比传统CPU和GPU更高效的计算能力。

## 基本概念

- **GDMA (Generic Direct Memory Access)**
通用直接内存访问（GDMA）是一种*允许某些硬件子系统直接访问主内存*的技术，绕过CPU进行数据传输，从而降低延迟并提高数据传输效率。在TPU架构中，GDMA可以快速地将数据*从主存储器传输到TPU*，或者*在TPU的不同部分之间传输数据*，这对于提高推理速度至关重要。

- **DDR (Double Data Rate)**
双倍数据速率（DDR）内存是一种常见的随机存取存储器技术，它能够在每个时钟周期传输两次数据，从而提高带宽。在TPU系统中，*DDR内存通常用作外部存储器*，*存放模型参数和中间数据*。尽管它*比片上内存慢*，但提供了更大的存储空间。

- **PCIe (Peripheral Component Interconnect Express)**
PCIe是一种*高速串行计算机扩展总线标准*，用于*连接主板上的TPU等高速硬件*。PCIe的速度对于整体推理性能至关重要，因为它影响数据从主机内存传输到TPU的速度。如果PCIe带宽不足，即使TPU计算能力很强，也可能会因为数据传输延迟而导致性能瓶颈。

- **本地编译 v.s. 交叉编译**
交叉编译是指在一个平台（称为宿主机）上生成另一个不同平台（称为目标机）上运行的代码的过程。这种编译方式是相对于本地编译来说的。
    - 本地编译（Native Compilation）
    在本地编译中，编译器在同一个类型的机器上生成代码，该代码将在同一类型的机器上执行。例如，使用x86架构的计算机编译出来的程序，旨在在同一架构的计算机上运行。编译器和目标可执行文件都是为同一平台设计的。
    - 交叉编译（Cross Compilation）
    与本地编译不同，交叉编译器在一个平台上生成为另一个平台运行的代码。这通常用于嵌入式系统开发，因为这些系统可能没有足够的资源（如处理能力、内存等）来编译复杂的软件。例如，开发者可能在一台功能强大的x86架构的PC上编译出运行在ARM架构的嵌入式设备上的程序。它允许开发者利用宿主机的强大资源来编译软件，同时生成能够在资源受限的目标机上运行的代码。它还可以加快编译过程，因为宿主机通常比目标机更强大快速。为了进行交叉编译，开发者需要一个交叉编译器，这是一个能够生成目标机代码的编译器。交叉编译器通常包括编译器本身、链接器和库，它们都是为生成在目标平台上运行的代码而优化的。


- 概念之间关联
    - 内存带宽与推理速度：如果TPU的计算速度非常快，但内存带宽不足以提供必要的数据，那么推理速度会受到限制。
    - PCIe与数据传输：PCIe的速度决定了数据从主存储器到TPU的传输速度，这直接影响到模型推理的启动时间。
    - GDMA与效率：GDMA能够提高数据传输的效率，减少CPU的负担，从而允许CPU处理其他任务或节省能源。
    - DDR与存储容量：DDR内存提供了存储大型模型所需的容量，但其速度可能会影响到模型参数的加载时间。

## TPU架构和工作方式（以Sophgo 1684x的TPU架构为例）

![BM1684x芯片TPU架构](assets/image.png)

- **TPU**是一种*多个计算核*的架构设计，每一个核被称之为 **NPU**（Neural network Processing Unit）。
- TPU按照*单指令多数据*（Single Instruction Multiple Data，SIMD）的模式进行计算， 即在某一时刻所有的NPU都会执行同样的计算指令，但是每一个NPU操作的数据不一样。
- 每一个*NPU内部*存储数据的内存被称之为*Local Memory*， 每个NPU的计算单元只能访问Local Memory。

### 内存分类
该TPU架构下，数据主要存在于以下的内存中：
1. 系统内存（System Memory）
    - Global Memory： TPU芯片外的内存，DDR。
    - L2-SRAM： 片上内存，作为缓存。
2. Local Memory ： 片上内存，BDC计算单元直接访问的内存类型。

### TPU执行计算加速的过程
TPU进行计算加速通常分为以下几步：
1. host >> device：将数据从*主机端内存*搬运到*TPU的系统内存（Global Memory）*当中;
2. device内，DDR >> NPU：将数据从*系统内存（Global memory）*再搬运到*NPU的Local Memory*当中;
3. NPU内：驱动计算单元对Local Memory当中的数据进行计算，并将计算结果返回Local Memory;
4. NPU >> DDR：将计算结果从Local Memory搬运回Global Memory;
5. device >> host：将Global Memory中的计算结果搬运回主机端内存。

### TPU的工作模式
根据主控单元（主机端Host）的不同，TPU对应有两种不同的运行模式，分别被称为PCIe模式和SOC模式。

- *PCIe模式*:该模式下对应的产品形态为板卡。板卡通过PCIe接口连接到主机服务器上，主机服务器作为主控单元（Host）控制板卡的运行。

- *SoC（System on Chip）模式*:该模式下对应的产品形态为边缘推理设备。推理设备上的包含一个8核的A53处理器作为设备的主控单元（Host）控制板卡的运行。

### 异构计算模型
由于TPU是一个异构的架构设计，由**主机端发送指令**，**设备端接收指令按指令执行指定操作**。 因此，驱动TPU的进行指定计算需要分别完成主机端和设备端的两部分代码：

- 主机端(Host): 主机端代码，运行在主机侧，发送控制TPU运行的命令。
- 设备端(Device): 设备端代码，运行在设备侧，通常调用TPU的各种指令运行相应的运算。

主机端和设备端的代码由于目标设备不同，因此需要使用不同的编译器对代码进行编译。对于Device端代码，编译的过程可以被看作是动态链接库更新的过程。
- PCIe模式下，主机端代码编译用本地的cpp编译器，设备端代码编译需要交叉编译。
- SoC模式下，主机端代码编译用本地的cpp编译器或交叉编译，设备端代码编译需要交叉编译。


### 与GPU编程的异同
#### 相同点
- 异构计算模型：TPU和Nvidia GPU都遵循异构计算模型，即计算任务在主机端和设备端之间分配。主机端负责控制流、任务调度和高层次的逻辑处理，而设备端负责执行密集的数值计算。
- 主机端和设备端代码：在TPU和GPU的编程模型中，都需要编写主机端代码和设备端代码。主机端代码运行在CPU上，负责管理设备端的执行，包括数据的准备和传输。设备端代码（如CUDA代码在GPU上，而TPU专有的指令集代码在TPU上）运行在设备上，执行具体的数值计算任务。
- 不同的编译器：由于主机端和设备端的处理器架构不同，它们的代码需要使用不同的编译器。例如，Nvidia GPU使用CUDA或者OpenCL等编程模型，并需要相应的Nvidia编译器（nvcc）来编译设备端代码，而主机端代码通常使用标准C/C++编译器。

#### 不同点
硬件架构、指令集和编程模型、生态系统和工具链、内存访问和数据传输...