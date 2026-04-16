# AI赋能GIS实践教学 - 开源资源

本仓库包含《AI赋能高校地理科学专业GIS实践课的创新案例设计》论文配套的开源资源。

## 目录结构

```
open_source/
├── README.md                      # 本说明文件
├── README_CN.md                   # 中文说明
├── code/
│   ├── GIS_Practice_Workflow.py   # 完整GIS分析工作流
│   ├── complete_analysis.py        # 多因子评价分析
│   └── quick_fix.py               # 可视化脚本
├── data/
│   └── srtm_59_08.tif            # SRTM DEM数据（肇庆地区）
├── prompts/
│   └── AI_Prompts_for_GIS_Practice.md  # AI辅助教学Prompt清单
└── results/
    ├── zhaoqing_publication_figures.png   # 分析结果图
    ├── zhaoqing_multi_factor_analysis.png # 多因子评价图
    └── ...
```

## 内容说明

### 1. AI教学Prompt清单 (prompts/)
包含四个教学阶段的AI辅助Prompt示例：
- 阶段一：问题定义
- 阶段二：数据获取
- 阶段三：空间建模
- 阶段四：成果表达

### 2. Python代码 (code/)
可运行的Python脚本，包括：
- 道路网数据获取（OSM）
- DEM数据分析
- 多因子加权叠加评价
- 敏感性分析

### 3. 分析结果 (results/)
教学案例分析结果图件

### 4. DEM数据 (data/)
**注意**：由于SRTM数据文件较大（约72MB），数据文件未上传至GitHub。请从以下来源自行下载：

- SRTM 90m 数据: https://srtm.csi.cgiar.org/
- 研究区使用Tile: srtm_59_08.tif (覆盖东经110-115°, 北纬20-25°)
- 或从NASA下载: https://www2.jpl.nasa.gov/srtm/

## 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/ZZhangsyx/AI-GIS-Practice-Teaching.git
```

### 2. 安装依赖
```bash
pip install osmnx geopandas rasterio numpy scipy matplotlib
```

### 3. 运行代码
```bash
cd code
python GIS_Practice_Workflow.py
```

## 研究案例

本教学案例以"肇庆市端州区生态友好型物流园区选址"为例，构建了四阶段人机协同教学模式：

1. **问题定义** - 学生与AI协作确定选址目标和评价指标
2. **数据获取** - AI生成代码获取OSM道路网和SRTM地形数据
3. **空间建模** - AI辅助多因子加权叠加分析与敏感性分析
4. **成果表达** - AI辅助报告撰写与教学反思

## 数据来源

### 道路网数据
- **来源**: OpenStreetMap (https://www.openstreetmap.org/)
- **方法**: 通过osmnx库下载
- **覆盖范围**: 肇庆市端州区 (N22.95-23.25, E112.35-112.70)
- **统计**: 节点10,031个，道路21,230条

### DEM数据
- **来源**: SRTM 90m (https://srtm.csi.cgiar.org/)
- **高程范围**: 1.0m - 960.0m
- **平均高程**: 114.3m

## 引用

如果使用本教学案例或数据，请引用：

```
AI-Assisted GIS Practice Teaching Case: Ecological Logistics Park Site Selection
in Zhaoqing Duanzhou District
```

## 许可证

MIT License

## 联系方式

GitHub: https://github.com/ZZhangsyx/AI-GIS-Practice-Teaching
