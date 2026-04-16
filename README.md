# 🎓 AI-Assisted GIS Practice Teaching

> A human-AI collaborative teaching model for GIS spatial analysis courses in higher education

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.XXXXXXX-orange.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)

---

## 📖 Overview

This repository contains the teaching case study and open-source resources for **"AI-Assisted GIS Practice Teaching in Higher Education"**. The project demonstrates how to integrate generative AI tools (like ChatGPT) into GIS practical teaching, using the **Zhaoqing Duanzhou District Ecological Logistics Park Site Selection** as a real-world teaching example.

### 🎯 Key Features

- 🤖 **Human-AI Collaboration** - AI as a "technical collaborator" in GIS teaching
- 🗺️ **Real Case Study** - Authentic geospatial data from Zhaoqing, Guangdong
- 📚 **Complete Teaching Workflow** - 4-stage pedagogical model
- 💻 **Runnable Code** - Python scripts with AI-generated prompts

---

## 🏗️ Project Structure

```
AI-GIS-Practice-Teaching/
├── README.md              # 📌 You are here
│
├── 📁 prompts/           # 💬 AI Prompts for Teaching
│   └── AI_Prompts_for_GIS_Practice.md
│       ├── Phase 1: Problem Definition
│       ├── Phase 2: Data Acquisition
│       ├── Phase 3: Spatial Modeling
│       └── Phase 4: Results & Reflection
│
├── 📁 code/              # 💻 Python Scripts
│   ├── GIS_Practice_Workflow.py      # Complete workflow
│   ├── complete_analysis.py          # Multi-factor evaluation
│   └── quick_fix.py                 # Visualization
│
├── 📁 results/          # 📊 Analysis Results
│   ├── zhaoqing_publication_figures.png
│   ├── zhaoqing_multi_factor_analysis.png
│   └── ...
│
└── 📁 data/             # 🗺️ DEM Data (user download)
    └── README_DATA.md   # Instructions for SRTM data download
```

---

## 🎓 Teaching Model: 4-Stage Human-AI Collaboration

```
┌─────────────────────────────────────────────────────────────────────┐
│                   Human-AI Collaborative Teaching                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│    ┌─────────┐         ┌─────────┐         ┌─────────┐              │
│    │ Teacher │◄──────►│   AI    │◄──────►│ Student │              │
│    │ (Design)│        │ (Coding)│        │ (Active)│              │
│    └────┬────┘         └────┬────┘         └────┬────┘              │
│         │                    │                    │                   │
│         ▼                    ▼                    ▼                   │
│    ┌─────────────────────────────────────────────────────────────┐  │
│    │              4-Stage Teaching Process                        │  │
│    │                                                              │  │
│    │   ① Problem Definition ──► ② Data Acquisition ──►          │  │
│    │         │                         │                          │  │
│    │         ▼                         ▼                          │  │
│    │   ③ Spatial Modeling ──► ④ Results & Reflection            │  │
│    │                                                              │  │
│    └─────────────────────────────────────────────────────────────┘  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Stage 1: Problem Definition (8 class hours)
> Students collaborate with AI to design analysis framework

### Stage 2: Data Acquisition (8 class hours)
> AI generates code for OSM road network & SRTM DEM extraction

### Stage 3: Spatial Modeling (12 class hours)
> AI-assisted multi-factor weighted overlay & sensitivity analysis

### Stage 4: Results & Reflection (8 class hours)
> Report writing & critical reflection on AI limitations

---

## 🗺️ Case Study: Zhaoqing Logistics Park Site Selection

### Study Area
- **Location**: Duanzhou District, Zhaoqing City, Guangdong Province
- **Coordinates**: N22.95-23.25°, E112.35-112.70°
- **Terrain**: Northern hills, southern alluvial plain

### Evaluation Index System

| Criterion | Factor | Weight | Classification |
|-----------|--------|--------|----------------|
| 🚗 Traffic | Highway distance | 20% | 5-level suitability |
| ⛰️ Terrain | Slope | 25% | 0-3°/3-8°/8-15°/15-25°/>25° |
| 🌿 Ecology | Water body exclusion | 15% | Distance-based |
| 📊 Land | Land use compatibility | 10% | Industrial/Construction/Farm |

---

## 📊 Results Visualization

### Multi-factor Suitability Analysis

![Analysis Results](results/zhaoqing_multi_factor_analysis.png)

*Figure: Multi-factor weighted overlay analysis results showing suitability levels*

### Road Network Classification

![Road Network](results/zhaoqing_road_network.png)

*Figure: OpenStreetMap road network classification in Zhaoqing Duanzhou District*

---

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/ZZhangsyx/AI-GIS-Practice-Teaching.git
cd AI-GIS-Practice-Teaching
```

### 2. Install Dependencies
```bash
pip install osmnx geopandas rasterio numpy scipy matplotlib
```

### 3. Download DEM Data
```bash
# Download SRTM 90m tile from:
# https://srtm.csi.cgiar.org/
# Tile: srtm_59_08.tif (covers 110-115°E, 20-25°N)
# Place in: data/srtm_59_08.tif
```

### 4. Run Analysis
```bash
cd code
python GIS_Practice_Workflow.py
```

---

## 💬 Example AI Prompts

### Prompt 1: Analysis Framework Design
```
请为"肇庆市端州区生态友好型物流园区"GIS选址分析设计一个完整的技术框架，
包括：数据需求清单、分析步骤流程、评价指标体系、权重确定方法。
```

### Prompt 2: Data Acquisition
```
如何使用Python从OpenStreetMap获取肇庆市端州区的道路网数据？
请给出使用osmnx库的完整代码示例。
```

### Prompt 3: Weighted Overlay
```
请写Python代码实现多因子加权叠加分析，输入5个重分类栅格（值域1-5），
权重[0.20, 0.15, 0.25, 0.10, 0.30]，计算加权求和并分5级输出。
```

*See [prompts/AI_Prompts_for_GIS_Practice.md](prompts/AI_Prompts_for_GIS_Practice.md) for all 13 prompts*

---

## 📚 Teaching Evaluation

| Dimension | Weight | Description |
|-----------|--------|-------------|
| 📝 AI Interaction Log | 20% | Question precision, logic, critical thinking |
| 💻 Code Debugging | 20% | Code understanding, error correction |
| 📊 Site Selection Report | 30% | Scientific rigor, innovation, cartography |
| 🤔 Reflection Report | 20% | Depth of reflection on AI collaboration |

---

## 🔬 Innovation Points

1. **Paradigm Shift**: From "operation-oriented" to "thinking-oriented" teaching
2. **"Dual-Teacher" Model**: Teacher + AI collaborative instruction
3. **Human-AI Literacy**: Cultivating critical AI use for future geographers

---

## 📖 Citation

If you use this teaching case or code in your research, please cite:

```bibtex
@misc{AIGISPracticeTeaching2026,
  title = {AI-Assisted GIS Practice Teaching: A Human-AI Collaborative Model},
  author = {Zhang, S. Y.},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/ZZhangsyx/AI-GIS-Practice-Teaching}
}
```

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a pull request.

---

## 📧 Contact

- **GitHub**: [ZZhangsyx/AI-GIS-Practice-Teaching](https://github.com/ZZhangsyx/AI-GIS-Practice-Teaching)
- **Email**: zzhangsyx@example.edu

---

<p align="center">
  <strong>⭐ Star this repo if you find it useful!</strong>
</p>
