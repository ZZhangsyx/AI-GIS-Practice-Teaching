# 🎓 AI赋能GIS实践教学

> 高校地理科学专业GIS实践课的人机协同教学模式

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)

---

## 📖 项目概述

本仓库包含《AI赋能高校地理科学专业GIS实践课的创新案例设计》论文配套的开源资源。项目以**肇庆市端州区生态友好型物流园区选址**为教学案例，探索将生成式AI（如ChatGPT）融入GIS实践教学的人机协同模式。

### 🎯 核心特色

- 🤖 **人机协同** - AI作为GIS教学的"技术协作者"
- 🗺️ **真实案例** - 基于广东省肇庆市的真实地理数据
- 📚 **完整教学流程** - 四阶段递进式教学模式
- 💻 **可运行代码** - 配套Python脚本与AI提示词

---

## 🏗️ 项目结构

```
AI-GIS-Practice-Teaching/
├── README.md              # 📌 英文说明
├── README_CN.md           # 📌 中文说明（你在这里）
│
├── 📁 prompts/           # 💬 AI教学提示词
│   └── AI_Prompts_for_GIS_Practice.md
│       ├── 阶段一：问题定义
│       ├── 阶段二：数据获取
│       ├── 阶段三：空间建模
│       └── 阶段四：成果表达
│
├── 📁 code/              # 💻 Python代码
│   ├── GIS_Practice_Workflow.py      # 完整工作流
│   ├── complete_analysis.py          # 多因子评价
│   └── quick_fix.py                 # 可视化脚本
│
├── 📁 results/          # 📊 分析结果
│   ├── zhaoqing_publication_figures.png
│   ├── zhaoqing_multi_factor_analysis.png
│   └── ...
│
└── 📁 data/             # 🗺️ DEM数据（需下载）
    └── README_DATA.md    # 数据下载说明
```

---

## 🎓 教学模式：四阶段人机协同

```
┌─────────────────────────────────────────────────────────────────────┐
│                    人机协同GIS实践教学模式                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│    ┌─────────┐         ┌─────────┐         ┌─────────┐              │
│    │ 教师    │◄───────►│   AI    │◄───────►│ 学生    │              │
│    │(教学设计)│        │(技术协作者)│        │(主动建构)│              │
│    └────┬────┘         └────┬────┘         └────┬────┘              │
│         │                    │                    │                   │
│         ▼                    ▼                    ▼                   │
│    ┌─────────────────────────────────────────────────────────────┐  │
│    │                    四阶段教学流程                              │  │
│    │                                                              │  │
│    │   ①问题定义 ──► ②数据获取 ──►                              │  │
│    │         │                │                                    │  │
│    │         ▼                ▼                                    │  │
│    │   ③空间建模 ──► ④成果表达                                    │  │
│    │                                                              │  │
│    └─────────────────────────────────────────────────────────────┘  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 阶段一：问题定义（8课时）
> 学生与AI协作确定选址目标和评价指标体系

### 阶段二：数据获取（8课时）
> AI生成代码获取OSM道路网和SRTM地形数据

### 阶段三：空间建模（12课时）
> AI辅助多因子加权叠加分析与敏感性分析

### 阶段四：成果表达（8课时）
> AI辅助报告撰写与教学反思

---

## 🗺️ 教学案例：肇庆物流园区选址

### 研究区概况
- **位置**：广东省肇庆市端州区
- **坐标**：北纬22.95-23.25°，东经112.35-112.70°
- **地形**：北部丘陵山地，南部珠江三角洲冲积平原

### 评价指标体系

| 准则层 | 因子层 | 权重 | 分类标准 |
|-------|-------|------|---------|
| 交通可达性 | 距高速公路 | 20% | 5级适宜性 |
| 地形条件 | 坡度 | 25% | 0-3°/3-8°/8-15°/15-25°/>25° |
| 生态友好性 | 水体避让 | 15% | 距水体距离 |
| 土地适应性 | 用地兼容性 | 10% | 工业/建设/耕地 |

---

## 📊 分析结果可视化

### 多因子适宜性评价

![分析结果](results/zhaoqing_multi_factor_analysis.png)

*图：多因子加权叠加分析结果，示适宜性等级分布*

### 道路网络分类

![道路网](results/zhaoqing_road_network.png)

*图：OpenStreetMap肇庆市端州区道路网络分类*

---

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/ZZhangsyx/AI-GIS-Practice-Teaching.git
cd AI-GIS-Practice-Teaching
```

### 2. 安装依赖
```bash
pip install osmnx geopandas rasterio numpy scipy matplotlib
```

### 3. 下载DEM数据
```bash
# 从以下地址下载SRTM 90m数据：
# https://srtm.csi.cgiar.org/
# 瓦片：srtm_59_08.tif (覆盖东经110-115°, 北纬20-25°)
# 放置于：data/srtm_59_08.tif
```

### 4. 运行代码
```bash
cd code
python GIS_Practice_Workflow.py
```

---

## 💬 AI提示词示例

### 提示词1：分析框架设计
```
请为"肇庆市端州区生态友好型物流园区"GIS选址分析设计一个完整的技术框架，
包括：数据需求清单、分析步骤流程、评价指标体系、权重确定方法。
```

### 提示词2：数据获取
```
如何使用Python从OpenStreetMap获取肇庆市端州区的道路网数据？
请给出使用osmnx库的完整代码示例。
```

### 提示词3：加权叠加分析
```
请写Python代码实现多因子加权叠加分析，输入5个重分类栅格（值域1-5），
权重[0.20, 0.15, 0.25, 0.10, 0.30]，计算加权求和并分5级输出。
```

*完整13个提示词见 [prompts/AI_Prompts_for_GIS_Practice.md](prompts/AI_Prompts_for_GIS_Practice.md)*

---

## 📚 教学评价体系

| 评价维度 | 权重 | 评价要点 |
|---------|------|---------|
| AI交互日志 | 20% | 提问的精准性、逻辑性、批判性 |
| 代码调试记录 | 20% | 代码理解、错误修正、创新改进 |
| 选址方案报告 | 30% | 科学性、创新性、图件规范性 |
| 反思报告 | 20% | 反思深度、实践关联、未来展望 |

---

## 🔬 教学创新点

1. **范式转变**：从"操作导向"到"思维导向"
2. **双师协同**：教师与AI协同的教学模式重构
3. **人机协同素养**：培养批判性使用AI工具的能力

---

## 📖 引用

```bibtex
@misc{AIGISPracticeTeaching2026,
  title = {AI赋能GIS实践教学：人机协同教学模式},
  author = {张, 三},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/ZZhangsyx/AI-GIS-Practice-Teaching}
}
```

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 🤝 贡献

欢迎提交Issue或Pull Request！

---

## 📧 联系方式

- **GitHub**: [ZZhangsyx/AI-GIS-Practice-Teaching](https://github.com/ZZhangsyx/AI-GIS-Practice-Teaching)

---

<p align="center">
  <strong>⭐ 如果这个项目对你有帮助，请给个Star！</strong>
</p>
