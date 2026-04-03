# 电商店铺月度利润自动回填工具（MVP）

本工具用于：读取标准化输入表（6 张），按月聚合后回填到利润模板的 `2026`（或指定年份）sheet，并主动修正关键公式，同时输出校验报告。

## 实现方案（简要）

1. **加载层 (`src/loaders.py`)**
   - 从输入目录按约定文件名读取 `xlsx/csv`。
   - 缺失文件不崩溃，按空表处理并写入校验报告。

2. **标准化与校验 (`src/normalizers.py`, `src/validators.py`)**
   - 月份统一标准化为 `1-12`。
   - 金额字段清洗（去 `¥`、`,`、空格），空值按 `0` 并记录 warning。
   - 枚举字段校验，未知值写入报告。
   - 重复主键、缺失必填字段、非法月份/金额写入报告。

3. **聚合层 (`src/aggregators.py`)**
   - 按月份汇总各类指标。
   - 完整覆盖你定义的行映射来源字段。

4. **Excel 回填 (`src/excel_writer.py`)**
   - 回填 `D-O` 月份列。
   - 强制重写关键公式（含 row39/row40 正确逻辑）。
   - 统一防除零：比例项写为 `IF(row6=0,0,...)`。
   - 自动补齐 10~12 月公式。
   - 校验报告写入 `validation_report` sheet。

5. **CLI 入口 (`app.py`)**
   - 一条命令跑通全流程。

## 项目结构

```text
project/
├── app.py
├── requirements.txt
├── README.md
├── config/
│   ├── mappings.py
│   └── settings.py
├── src/
│   ├── aggregators.py
│   ├── excel_writer.py
│   ├── loaders.py
│   ├── models.py
│   ├── normalizers.py
│   ├── utils.py
│   └── validators.py
├── tests/
│   ├── test_aggregators.py
│   ├── test_excel_writer.py
│   └── test_normalizers.py
└── sample_data/
    └── generate_sample_data.py
```

## 安装

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 生成最小示例数据

```bash
python sample_data/generate_sample_data.py
```

会生成：
- `sample_data/template_2026.xlsx`
- `sample_data/input/*.csv`

## 运行

```bash
python app.py \
  --template ./sample_data/template_2026.xlsx \
  --input-dir ./sample_data/input \
  --year 2026 \
  --output ./output/2026电商流水利润_已回填.xlsx
```

## 输出

1. 回填后的 Excel：你指定的 `--output`
2. 校验报告：输出文件中的 `validation_report` sheet
3. 运行日志：命令行 INFO/WARNING

## 税点说明（MVP）

- 当前默认所有输入值视为**不含税金额**。
- 仅保留 `row7 = row6 / (1+tax_rate_income)` 逻辑。
- 税率在 `config/settings.py` 中配置：`tax_rate_income = 0.13`。

## 测试

```bash
pytest -q
```

已覆盖：
- 月份标准化
- 金额清洗
- 枚举校验
- 聚合结果
- Excel 指定单元格回填
- 关键公式写入（含 10~12 月公式）

## 自检清单

- [x] 所有映射行已覆盖（收入/IP授权金/成本/运营/平台）
- [x] row39 已修正为包含授权金合计
- [x] row40 已修正为 `row6-row39`
- [x] 10~12 月公式自动补齐
- [x] 提供基础 pytest 用例
