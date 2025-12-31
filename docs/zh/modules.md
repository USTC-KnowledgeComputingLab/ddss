# 模块说明

系统由以下模块组成，在 `ddss/*.py` 和 `ddss/*.ts` 中进行了对称实现：

- **Input** (`ddss/input.py`, `ddss/input.ts`)：具有 BNF 语法解析功能的交互式输入接口。
- **Output** (`ddss/output.py`, `ddss/output.ts`)：实时显示数据库中的事实和想法。
- **Load** (`ddss/load.py`, `ddss/load.ts`)：从标准输入批量导入事实。
- **Dump** (`ddss/dump.py`, `ddss/dump.ts`)：将所有事实和想法导出到输出。
- **DS** (`ddss/ds.py`, `ddss/ds.ts`)：前向链接演绎搜索引擎。
- **Egg** (`ddss/egg.py`, `ddss/egg.ts`)：基于 E-graph 的等式推理引擎。
