# Oil Well Macro Control Chart 2.0

油井宏观控制图 2.0 是一个用于油井供采匹配、能效评价、措施潜力识别和液量供给状态分析的示例工程。仓库包含方法说明、样例数据、指标计算脚本、绘图脚本、Streamlit 演示应用和 Notebook 示例。

## Project Structure

```text
oil-well-macro-control-chart-2.0/
├── docs/        # 方法、图谱、指标、流程和引用声明
├── data/        # 样例油井数据
├── src/         # 数据生成、指标计算、绘图和应用入口
├── notebooks/   # Notebook 演示
├── examples/    # 示例图表
└── assets/      # 框架图等静态资源
```

## Quick Start

```bash
pip install -r requirements.txt
python src/generate_sample_data.py --rows 500 --output data/sample_wells_500.csv
python src/plot_macro_control_chart.py --input data/sample_wells_500.csv --output-dir examples --asset-dir assets
streamlit run src/app.py
```

## Data

`data/sample_wells_500.csv` 是基于固定随机种子的模拟样例数据，包含 500 口井的生产、能耗、液面、供采匹配和措施潜力字段。样例数据仅用于方法演示，不代表任何实际油田资产。

## Main Outputs

- `examples/supply_production_matching.png`
- `examples/energy_value_chart.png`
- `examples/measure_potential_chart.png`
- `examples/liquid_supply_status_chart.png`
- `assets/framework_diagram.png`

## License

当前 `LICENSE` 文件为占位声明。正式开源或商业授权条款应由仓库所有者确认后更新。
