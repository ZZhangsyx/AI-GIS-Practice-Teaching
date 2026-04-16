# AI Prompts for GIS Practice Teaching

This document contains all AI prompts used in the "Ecological Logistics Park Site Selection" teaching case for Zhaoqing Duanzhou District.

---

## Phase 1: Problem Definition and AI-Assisted Framework Design

### Prompt 1: Analysis Framework Design

```
请为"肇庆市端州区生态友好型物流园区"GIS选址分析设计一个完整的技术框架，
包括：
1. 数据需求清单（应获取哪些空间数据）
2. 分析步骤流程（按先后顺序列出关键技术环节）
3. 评价指标体系（列出各因子及其权重确定方法）
4. 结果验证方法（如何检验选址结果的合理性）
5. 权重确定方法（推荐适合本科教学的方法）

请以结构化方式输出，便于后续实施。

背景信息：
- 研究区：广东省肇庆市端州区
- 人口约75万，以平原和低山丘陵为主
- 需要考虑交通可达性、生态环境、土地利用等多因素
```

### Prompt 2: Index Weight Determination Methods

```
在物流园区选址的多因子加权评价中，常用的权重确定方法有哪些？
各有什么优缺点？请推荐适合本科教学场景的方法，并说明具体操作步骤。
```

### Prompt 3: Ecological Protection Standards

```
请提供国家层面和地方层面的生态保护区划分标准，包括但不限于：
- 自然保护区
- 生态红线
- 湿地保护范围
- 河湖蓝线

哪些区域应设为"绝对排除区"？哪些可以有限利用？
```

---

## Phase 2: Data Acquisition and AI-Assisted Processing

### Prompt 4: OSM Road Network Data Acquisition

```
如何使用Python从OpenStreetMap获取肇庆市端州区的道路网数据？
请给出使用osmnx库的完整代码示例，包括：
1. 如何安装必要库（如osmnx、geopandas）
2. 如何指定研究区范围（经纬度边界）
3. 如何提取不同等级道路（高速、主干路、次干路等）
4. 如何保存为本地文件（GeoJSON或GeoPackage格式）

请提供完整可运行的代码，包含详细注释。
```

### Prompt 5: DEM Slope Analysis

```
请写Python代码实现以下功能：
1. 读取SRTM DEM数据（GeoTIFF格式）
2. 计算坡度（Slope）
3. 将坡度按以下标准重分类为5级：
   - [0-3°) 极平坦（最适宜）
   - [3-8°) 平坦（适宜）
   - [8-15°) 缓坡（中等适宜）
   - [15-25°) 陡坡（较不适宜）
   - [>25°) 极陡（不适宜）
4. 保存重分类结果

请使用rasterio库实现，提供完整代码和注释。
```

### Prompt 6: Buffer Analysis

```
请说明在QGIS中如何创建高速公路的2km缓冲区？
若使用Python代码，应如何使用GeoPandas实现？
请给出具体操作步骤和代码示例。
```

---

## Phase 3: Spatial Modeling and AI-Assisted Optimization

### Prompt 7: Weighted Overlay Analysis

```
请用ArcPy或GeoPandas写一段代码，实现多因子加权叠加分析。
具体要求：
1. 输入5个重分类后的栅格图层（值域1-5，越大越适宜）
2. 各图层权重为[0.20, 0.15, 0.25, 0.10, 0.30]
3. 计算加权求和得到综合适宜性得分
4. 将结果分为5个等级输出

请包含完整注释说明每一步的操作。
```

### Prompt 8: Counterfactual Analysis

```
假设我们把"生态敏感性"因子的权重从0.25提高到0.35，
其他因子权重相应调整，预测选址结果如何变化？
从地理学角度分析说明什么问题？

背景：
- 肇庆市端州区以平原为主，但北部有丘陵山地
- 交通便利区域往往生态用地比例较高
```

### Prompt 9: Cost Distance Analysis

```
物流园区选址还需要考虑交通成本，请说明如何在GIS中实现成本距离（Cost Distance）分析？
如何创建成本表面？请给出Python代码示例。
```

---

## Phase 4: Results Expression and AI-Assisted Reflection

### Prompt 10: Report Framework and Map Standards

```
请提供一份规范的GIS选址分析报告结构框架，包括：
- 摘要（300-500字）
- 关键词
- 引言
- 研究区概况
- 数据与方法
- 结果分析
- 讨论与结论
- 参考文献

同时请说明地图制图的规范要素：
- 标题
- 图例
- 比例尺
- 指北针
- 坐标系统
```

### Prompt 11: Reflection Report Framework

```
提供一个撰写《AI与地理实践》反思报告的结构框架，
引导学生系统性地分析：
1. AI在哪些环节提供了有效帮助？
2. AI在哪些环节可能产生误导或困扰？
3. 人机协同的边界在哪里？
4. 对未来地理研究中AI应用的展望？

请给出具体的分析维度和思考问题。
```

---

## Additional Prompts

### Prompt 12: AI Limitations Analysis

```
请分析在GIS选址分析中，AI工具可能存在哪些局限性或风险？
包括但不限于：
- 数据偏见
- 算法黑箱
- 事实性错误
- 空间尺度问题

如何规避这些风险？
```

### Prompt 13: Secondary School Teaching Activity Design

```
如何将本案例简化为高中地理"必修2：产业区位选择"章节的教学实践活动？
请设计一个约45分钟的学生分组任务，包括：
1. 任务背景（简化版情境描述）
2. 引导性问题（3-5个）
3. 数据与工具（高中生可操作的简化数据）
4. 预期成果（学生应产出什么）
5. 教师指导要点
```

---

*Last updated: 2026-04-15*
*Generated for: AI-Assisted GIS Practice Teaching*
