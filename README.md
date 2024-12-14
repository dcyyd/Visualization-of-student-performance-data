<h1 align="center">基于`Python`的学生成绩数据分析与可视化项目</h1>

## 一、项目概述

本项目旨在对学生成绩数据进行全面的分析与可视化展示。通过读取包含学生各项信息（如性别、种族/民族、父母教育水平、午餐情况、备考课程以及数学、阅读、写作成绩等）的CSV数据文件，实现以下主要功能：

1. **数据预处理**：备份原始数据集，处理数据中的缺失值（采用中位数填充数学、阅读、写作成绩列的缺失值），并将列名汉化，方便查看与理解，最后将处理后的数据保存至指定文件夹。
2. **数据分析**：针对不同维度（种族、性别、父母教育水平、午餐类型、测试准备课程）计算平均成绩，并输出相应的分析结果。
3. **数据可视化**：利用多种图表类型（箱型图、饼图、直方图、散点图等）直观展示数据特征，且所有可视化图表均会转换为HTML文档保存，便于查看与分享。

本项目使用了Python中常用的数据处理与可视化相关库，包括 `pandas`、`matplotlib`、`seaborn` 以及 `mpld3` 等。

## 二、项目结构

```bash
Visualization-of-student-performance-data
project_root/
│
├── .venv/               # 虚拟环境目录
│   ├── Lib/
│   ├── Scripts/
│   ├── ...             # 其他虚拟环境相关文件
│
├── .gitignore           # Git忽略文件配置
├── pyvenv.cfg           # 虚拟环境配置文件
│
├── src/                 # 源代码目录
│   ├── data_backup/     # 数据备份文件夹
│   │   └── StudentsPerformance_backup.csv
│   ├── data_source/    # 数据源文件夹
│   │   └── StudentsPerformance.csv
│   ├── output/         # 输出文件夹
│   │   ├── 可视化结果/  # 存放可视化结果的文件夹
│   │   │   ├── 平均成绩等级分布饼图.html
│   │   │   ├── 按午餐类型分类数学成绩箱型图.html
│   │   │   ├── 按备考课程分类数学成绩箱型图.html
│   │   │   ├── 按性别分类数学成绩箱型图.html
│   │   │   ├── 按种族分类数学成绩箱型图.html
│   │   │   └── 数学成绩分布直方图.html
│   │   ├── 数据分析结果/ # 存放数据分析结果的文件夹
│   │   │   ├── 午餐维度平均成绩结果.txt
│   │   │   ├── 午餐维度成绩标准差结果.txt
│   │   │   ├── 备考课程维度平均成绩结果.txt
│   │   │   ├── 备考课程维度成绩标准差结果.txt
│   │   │   ├── 性别维度平均成绩结果.txt
│   │   │   ├── 性别维度成绩标准差结果.txt
│   │   │   ├── 父母教育水平维度平均成绩结果.txt
│   │   │   ├── 父母教育水平维度成绩标准差结果.txt
│   │   │   ├── 种族_民族维度平均成绩结果.txt
│   │   │   └── 种族_民族维度成绩标准差结果.txt
│   │   └── 预处理数据/ # 存放预处理数据的文件夹
│   │       ├── data_info.txt
│   │       ├── head_data.txt
│   │       └── StudentsPerformance_processed.csv
│   └── main.py         # 主程序文件
│
├── requirements.txt    # 项目依赖文件
├── LICENSE             # 项目许可证文件
├── PIP使用说明.md      # PIP使用说明文件
├── README.md           # 项目说明文件
└── 代码分析.md         # 代码分析文件
```

## 三、技术栈

**本项目使用以下技术栈：**

- **`Python`**: 编程语言，用于数据处理和分析。
- **`Pandas`**: 用于数据操作和分析。
- **`Matplotlib & Seaborn`**: 用于数据可视化。
- **`MPld3`**: 用于将Matplotlib图表转换为HTML格式，便于在网页上展示。
- **`Git`**: 用于版本控制。

## 四、使用方式

1. **克隆项目**:
   ```bash
   git clone https://github.com/dcyyd/Visualization-of-student-performance-data.git
   ```

2. **创建并激活虚拟环境**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. **安装依赖**:
   ```bash
   pip install -r requirements.txt
   ```

4. **运行主程序**:
   ```bash
   python src/main.py
   ```

5. **查看结果**:
   处理后的数据和生成的可视化图表将保存在`src/output`目录下。

## 五、作者

ChangYou Dou (dcyyd_kcug@yeah.net)

## 六、许可证

本项目遵循MIT许可证 - 详见[LICENSE](LICENSE)文件。

## 七、联系和支持

如果您有任何问题或需要帮助，请通过以下方式联系我：

- **Email**: <a href="mailto:dcyyd_kcug@yeah.net">dcyyd_kcug@yeah.net</a>
- **Phone**：<a href="tel:+17633963626">17633963626</a>
- **Blog**: [https://www.kfufys.top](https://www.kfufys.top)
- **GitHub**: [https://github.com/dcyyd](https://github.com/dcyyd)