#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# 整体代码说明：
# 本代码主要用于对学生成绩数据进行分析与可视化展示。功能包括读取学生成绩数据文件，进行数据预处理（如备份原始数据、多种方式处理缺失值、汉化列名、数据合并与清洗等），
# 接着对数据进行更精炼的分析（计算不同维度下的平均成绩等），最后通过多种图表（箱型图、饼图、直方图、散点图等）对数据进行可视化展示，并将这些可视化图表保存为HTML文档，同时对可视化结果进行逻辑清晰的分析论述。
# 代码使用了多个常用的数据处理和可视化相关的Python库，如pandas、matplotlib、seaborn以及mpld3等。

# @Time    : 2024/4/10
# @Author  : ChangYou Dou
# @File    : main.py
# @Software: PyCharm
# @Description: 学生成绩数据可视化展示
# @Email: dcyyd_kcug@yeah.net
# @Blog: https://www.kfufys.top
# @GitHub: https://github.com/dcyyd
# @Copyright (C) 2024-2024 ChangYou Dou. All Rights Reserved.
# @License：本代码遵循MIT许可证，允许在遵守许可证条款的情况下自由使用、修改和分发。
"""
import mpld3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib as mpl

# 定义数据源文件夹和备份文件夹的全局变量（这种全局变量使用方式不推荐，这里为了方便演示暂保留这种形式）
_src_folder = 'data_source'
_dst_folder = 'data_backup'

import os
import pandas as pd
import matplotlib as mpl

# 定义数据源文件夹和备份文件夹的全局变量
_src_folder = 'data_source'
_dst_folder = 'data_backup'


def preprocess_data(file_path, output_dir):
    """
    函数功能：对给定路径的学生成绩数据文件进行预处理操作，包括多种方式的数据清洗、合并操作，并备份原始数据集。
    参数：
    - file_path：数据文件的路径，类型为字符串，指向包含学生成绩数据的CSV文件。
    - output_dir：输出文件夹路径，类型为字符串，用于保存处理后的数据文件以及后续生成的可视化相关文件。
    返回值：
    经过预处理后的学生成绩数据，类型为pandas的DataFrame。
    """
    # 设置matplotlib的字体和负号显示
    mpl.rcParams['font.family'] = 'SimHei'
    mpl.rcParams['axes.unicode_minus'] = False

    # 读取CSV文件
    data = pd.read_csv(file_path)

    # 备份原始数据集
    backup_path = os.path.join(_dst_folder, 'StudentsPerformance_backup.csv')
    os.makedirs(_dst_folder, exist_ok=True)  # 确保备份文件夹存在
    data.to_csv(backup_path, index=False)

    # 将列名换成中文，方便后续查看和理解数据
    data.columns = ['性别', '种族/民族', '父母教育水平', '午餐', '备考课程', '数学成绩', '阅读成绩', '写作成绩']

    # 创建预处理数据文件夹
    preprocess_output_dir = os.path.join(output_dir, "预处理数据")
    os.makedirs(preprocess_output_dir, exist_ok=True)

    # 将数据基本信息保存到文件
    info_file_path = os.path.join(preprocess_output_dir, 'data_info.txt')
    with open(info_file_path, 'w', encoding='utf-8') as f:
        f.write('数据基本信息：\n')
        data.info(buf=f)

    # 查看数据集行数和列数
    rows, columns = data.shape
    if rows < 100 and columns < 20:
        # 将全部数据内容信息保存到文件
        full_data_file_path = os.path.join(preprocess_output_dir, 'full_data.txt')
        with open(full_data_file_path, 'w', encoding='utf-8') as f:
            f.write('数据全部内容信息：\n')
            f.write(data.to_markdown(numalign='left', stralign='left'))
    else:
        # 将前几行数据内容信息保存到文件
        head_data_file_path = os.path.join(preprocess_output_dir, 'head_data.txt')
        with open(head_data_file_path, 'w', encoding='utf-8') as f:
            f.write('数据前几行内容信息：\n')
            f.write(data.head().to_markdown(numalign='left', stralign='left'))

    # 处理缺失值
    for col in ['数学成绩', '阅读成绩', '写作成绩']:
        median_val = data[col].median()
        data[col].fillna(median_val, inplace=True)

    mode_lunch = data['午餐'].mode()[0]
    data['午餐'].fillna(mode_lunch, inplace=True)

    edu_level_mapping = {
        '本科及以上': '有备考课程',
        '高中': '无备考课程'
    }
    data['备考课程'].fillna(data['父母教育水平'].map(edu_level_mapping), inplace=True)

    supplementary_file_path = os.path.join(_src_folder, 'supplementary_data.csv')
    if os.path.exists(supplementary_file_path):
        supplementary_data = pd.read_csv(supplementary_file_path)
        data = pd.merge(data, supplementary_data, on='学生编号', how='left')

    # 数据清洗：去除重复行
    data.drop_duplicates(inplace=True)

    # 将处理后的数据保存到输出文件夹下指定的文件中
    output_file_path = os.path.join(preprocess_output_dir, 'StudentsPerformance_processed.csv')
    data.to_csv(output_file_path, index=False, encoding='utf-8-sig')

    return data


def analyze_data(data, output_dir):
    """
    函数功能：对预处理后的学生成绩数据进行分析，计算不同维度（种族、性别、教育水平、午餐类型、测试准备课程）下的平均成绩以及成绩的标准差，更全面地了解数据分布情况。
    参数：
    data：经过预处理后的学生成绩数据，类型为pandas的DataFrame。
    output_dir：输出文件夹路径，类型为字符串。
    返回值：无，将不同维度下的平均成绩以及标准差结果保存到文件。
    """
    dimensions = ['种族/民族', '性别', '父母教育水平', '午餐', '备考课程']
    score_cols = ['数学成绩', '阅读成绩', '写作成绩']

    # 确保output目录存在
    analyze_output_dir = os.path.join(output_dir, "数据分析结果")
    os.makedirs(analyze_output_dir, exist_ok=True)

    for dim in dimensions:
        mean_scores = data.groupby(dim).mean()[score_cols]
        std_scores = data.groupby(dim).std()[score_cols]

        # 使用 _ 替换文件名中的 / 防止路径错误
        safe_dim = dim.replace('/', '_').replace('\\', '_')
        mean_file_path = os.path.join(analyze_output_dir, f"{safe_dim}维度平均成绩结果.txt")
        std_file_path = os.path.join(analyze_output_dir, f"{safe_dim}维度成绩标准差结果.txt")

        with open(mean_file_path, 'w', encoding='utf-8') as f_mean:
            f_mean.write(mean_scores.to_string(index=True) + "\n")

        with open(std_file_path, 'w', encoding='utf-8') as f_std:
            f_std.write(std_scores.to_string(index=True) + "\n")


def visualize_data(data, output_dir):
    """
    函数功能：对学生成绩数据进行多种可视化展示，包括箱型图、饼图、直方图、散点图等，并将这些可视化图表转换为HTML文档保存到指定的输出文件夹中，同时对每种可视化结果进行简单分析论述。
    参数：
    - data：经过预处理后的学生成绩数据，类型为pandas的DataFrame。
    - output_dir：输出文件夹路径，类型为字符串，用于保存生成的可视化相关的HTML文件。
    返回值：无，直接将可视化图表保存为HTML文件到指定输出文件夹中。
    """
    # 创建visualize_data函数对应的输出文件夹
    visualize_output_dir = os.path.join(output_dir, "可视化结果")
    if not os.path.exists(visualize_output_dir):
        os.makedirs(visualize_output_dir)

    # 种族与分数的箱型图
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='种族/民族', y='数学成绩', data=data)
    plt.title('按种族/族裔分类的数学成绩箱型图')
    plt.xticks(rotation=45)
    # 分析论述：通过箱型图可以直观看到不同种族/民族间数学成绩的中位数、上下四分位数以及是否存在异常值等情况，对比各箱型的位置和长度，能大致了解成绩的分布差异。
    html = mpld3.fig_to_html(plt.gcf())
    boxplot_file_path = os.path.join(visualize_output_dir, "按种族分类数学成绩箱型图.html")
    with open(boxplot_file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    plt.show()

    # 性别与分数的箱型图
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='性别', y='数学成绩', data=data)
    plt.title('按性别分类的数学成绩箱型图')
    # 分析论述：从此箱型图可以观察到不同性别学生在数学成绩上的分布差异，比如中位数是否有明显不同，箱型的宽窄反映了成绩的离散程度，有助于分析性别因素对数学成绩的影响。
    html = mpld3.fig_to_html(plt.gcf())
    gender_boxplot_file_path = os.path.join(visualize_output_dir, "按性别分类数学成绩箱型图.html")
    with open(gender_boxplot_file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    plt.show()

    # 父母教育水平与分数的箱型图
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='父母教育水平', y='数学成绩', data=data)
    plt.title('按父母教育水平分类的数学成绩箱型图')
    plt.xticks(rotation=45)
    # 分析论述：该箱型图展示了不同父母教育水平下学生数学成绩的分布状况。从中可以看出，不同教育水平对应的成绩中位数、四分位数范围有所不同，能帮助分析家庭背景中的父母教育程度对学生数学成绩的潜在影响，比如父母教育水平较高的情况下，学生成绩的整体水平和离散程度可能呈现出特定的规律。
    html = mpld3.fig_to_html(plt.gcf())
    parent_boxplot_file_path = os.path.join(visualize_output_dir, "按父母教育水平分类数学成绩箱型图.html")
    with open(parent_boxplot_file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    plt.show()

    # 午餐类型与分数的箱型图
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='午餐', y='数学成绩', data=data)
    plt.title('按午餐类型分类的数学成绩箱型图')
    # 分析论述：通过此箱型图可观察不同午餐类型对应的学生数学成绩分布，了解午餐这一因素是否与成绩存在关联，例如是否享用特定午餐的学生在成绩上有更集中或离散的表现等。
    html = mpld3.fig_to_html(plt.gcf())
    lunch_boxplot_file_path = os.path.join(visualize_output_dir, "按午餐类型分类数学成绩箱型图.html")
    with open(lunch_boxplot_file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    plt.show()

    # 测试准备课程与分数的箱型图
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='备考课程', y='数学成绩', data=data)
    plt.title('按备考课程分类的数学成绩箱型图')
    # 分析论述：从该箱型图能看出参加不同备考课程的学生在数学成绩上的差异，有助于判断备考课程对成绩提升是否有明显作用，以及不同备考课程下成绩的稳定性情况。
    html = mpld3.fig_to_html(plt.gcf())
    prep_course_boxplot_file_path = os.path.join(visualize_output_dir, "按备考课程分类数学成绩箱型图.html")
    with open(prep_course_boxplot_file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    plt.show()

    # 饼图：平均成绩的优、良、中、及格和不及格的分布
    plt.figure(figsize=(8, 8))
    labels = ['不及格', '及格', '中', '良', '优']
    # 根据成绩范围划分等级，并统计各等级的数量，按照等级顺序排序
    sizes = pd.cut(data['数学成绩'], bins=[0, 60, 70, 80, 90, 100],
                   labels=['不及格', '及格', '中', '良', '优']).value_counts().sort_index()
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140,
            colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0'])
    plt.title('平均成绩等级分布')
    plt.axis('equal')
    # 分析论述：饼图清晰展示了成绩各个等级所占的比例，能直观了解整体成绩的优劣分布情况，比如可以看出成绩集中在哪些等级范围，对整体成绩水平有一个宏观把握。
    html = mpld3.fig_to_html(plt.gcf())
    pie_file_path = os.path.join(visualize_output_dir, "平均成绩等级分布饼图.html")
    with open(pie_file_path, 'w', encoding='utf-8') as f:
        f.write(html)

    # 直方图：数学成绩分布
    plt.figure(figsize=(10, 6))
    sns.histplot(data['数学成绩'], bins=20, kde=True)
    plt.title('数学成绩分布')
    plt.xlabel('数学成绩')
    plt.ylabel('频数')
    # 分析论述：直方图呈现了数学成绩的具体分布形态，如是否近似正态分布，峰值所在位置反映了成绩的集中趋势，通过观察不同区间的频数情况，可进一步分析成绩的离散程度和集中范围。
    html = mpld3.fig_to_html(plt.gcf())
    hist_file_path = os.path.join(visualize_output_dir, "数学成绩分布直方图.html")
    with open(hist_file_path, 'w', encoding='utf-8') as f:
        f.write(html)


# 主函数
def main():
    """
    主函数，程序的入口点，用于协调各个功能模块的调用，完成数据处理、分析和可视化的整体流程。
    返回值：无，按顺序调用相关函数执行相应操作。
    """
    # 创建输出文件夹，如果不存在的话
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 构建数据文件的完整路径
    file_path = os.path.join(_src_folder, 'StudentsPerformance.csv')

    data = preprocess_data(file_path, output_dir)
    analyze_data(data, output_dir)
    visualize_data(data, output_dir)


if __name__ == '__main__':
    main()
