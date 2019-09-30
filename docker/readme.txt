


https://www.docker.com/
https://docs.docker.com

----------------------------------------------------------------------------------------------------
https://www.docker.com/resources/what-container

What is a Container?
  A standardized unit of software
  // 标准化的软件单元



                    containerized applications:

                  +----------------------------+
                  | appA | appB | appC | appD  |
                  |----------------------------|
                  |          Docker            |
                  |----------------------------|
                  |   Host Operating System    |
                  |----------------------------|
                  |      Infrastructure        |
                  +----------------------------+


    Package Software into Standardized Units for Development, Shipment and Deployment
    // 将 Software 打包 进 标准单元 中 以用于 Development, Shipment and Deployment

    A container is a standard unit of software that packages up code and all its dependencies
    so the application runs quickly and reliably from one computing environment to another.
    A Docker container image is a lightweight, standalone, executable package of software
    that includes everything needed to run an application: code, runtime, system tools, system libraries and settings.
    // A container 是 一个 标准的 软件单元, 其对 code 和 其所有 依赖(dependencies)进行了打包.
    // 因此 the application 可以 快速 并 可靠 地 从 one computing environment 跑/运行(runs) 到 另一个计算环境.
    // A Docker container image 是一个 lightweight, standalone, 可执行的 软件包,
    // 其包含了 run an application 所需要的 everything: code, runtime, system tools, system libraries and settings.


    Container images become containers at runtime and in the case of Docker containers-
    images become containers when they run on Docker Engine. Available for both Linux
    and Windows-based applications, containerized software will always run the same,
    regardless of the infrastructure. Containers isolate software from its environment
    and ensure that it works uniformly despite differences for instance between development and staging.
    // Container images 在 运行时成为 containers, 而 对于 Docker containers 来说,
    // images 会在 其 运行在 Docker Engine 上是 成为 containers. 不管 infrastructure 如何,
    // containerized software 对于 基于 Linux 和 Windows 的 applications 都是可用的, 其总是运行相同(一致),
    // Containers 将 software 与其 environment 隔离(isolate) 开来, 并 确保 其 一致地运行 而 无视
    // differences for instance between development and staging.


Docker containers that run on Docker Engine:

    - Standard: Docker created the industry standard for containers, so they could be portable anywhere

    - Lightweight: Containers share the machine’s OS system kernel and therefore do not require an OS per application,
                   driving higher server efficiencies and reducing server and licensing costs

    - Secure: Applications are safer in containers and Docker provides the strongest default isolation capabilities in the industry


Comparing Containers and Virtual Machines(Containers 和 Virtual Machines 的比较)

    Containers and virtual machines have similar resource isolation and allocation benefits,
    but function differently because containers virtualize the operating system instead of hardware.
    Containers are more portable and efficient.
    // Containers 和 virtual machines 具有相似的 资源隔离 和 分配优势,
    // 但 功能(function)不同, 因为 containers 是 虚拟化 the operating system 而非 hardware.
    // Containers are more portable and efficient.

        containerized applications         +----VM-----+----VM-----+----VM------+
      +----------------------------+       |           |           |            |
      | appA | appB | appC | appD  |       |  appA     |   appB    |    appC    |
      |----------------------------|       | --------  | --------  |  --------  |
      |          Docker            |       | Guest OS  | Guest OS  |  Guest OS  |
      |----------------------------|       |------------------------------------|
      |   Host Operating System    |       |            Hypervisor              |
      |----------------------------|       |------------------------------------|
      |      Infrastructure        |       |          Infrastructure            |
      +----------------------------+       +------------------------------------+


Containers
    Containers are an abstraction at the app layer that packages code and dependencies together.
    Multiple containers can run on the same machine and share the OS kernel with other containers,
    each running as isolated processes in user space. Containers take up less space than VMs
    (container images are typically tens of MBs in size),
    can handle more applications and require fewer VMs and Operating systems.

Virtual Machines
    Virtual machines (VMs) are an abstraction of physical hardware turning one server into many servers.
    The hypervisor allows multiple VMs to run on a single machine. Each VM includes a full copy
    of an operating system, the application, necessary binaries
    and libraries - taking up tens of GBs. VMs can also be slow to boot.


Containers and Virtual Machines Together
    Containers and VMs used together provide a great deal of flexibility in deploying and managing app





----------------------------------------------------------------------------------------------------



