# Data

本目录存放油井宏观控制图 2.0 的样例数据。

## Files

- `sample_wells_500.csv`: 500 口模拟油井样例数据。

## Regenerate

```bash
python src/generate_sample_data.py --rows 500 --output data/sample_wells_500.csv
```

样例数据使用固定随机种子生成，可复现实验和图件输出。
