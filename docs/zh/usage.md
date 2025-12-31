# 使用方法

无论使用哪种语言实现，用法、命令行选项和交互语法都是完全一致的。

## 基础用法

使用临时 SQLite 数据库运行 DDSS：

```bash
ddss
```

## 指定数据库

DDSS 支持多种数据库后端，通过 `-a` 或 `--addr` 选项指定：

```bash
# SQLite (持久化)
ddss --addr sqlite:///path/to/database.db

# MySQL
ddss --addr mysql://user:password@host:port/database

# MariaDB
ddss --addr mariadb://user:password@host:port/database

# PostgreSQL
ddss --addr postgresql://user:password@host:port/database
```

## 选择组件

默认情况下，DDSS 运行所有交互式组件（`input`, `output`, `ds`, `egg`）。您可以使用 `-c` 或 `--component` 选项选择特定组件：

```bash
# 仅运行输入和输出（无推理引擎）
ddss --component input output

# 仅运行前向链接引擎
ddss --component input output ds

# 仅运行 E-graph 引擎
ddss --component input output egg
```

可用组件：
- `input`: 交互式输入接口
- `output`: 实时显示事实和想法
- `ds`: 前向链接演绎搜索引擎
- `egg`: 基于 E-graph 的等式推理引擎
- `load`: 批量导入事实
- `dump`: 导出所有事实和想法

## 交互式使用

启动后，在 `input:` 提示符下输入事实和规则。语法遵循 `前提 => 结论` 的格式：

### 示例 1：简单推理

输入一个事实，声明 `a` 为真：
```
input: => a
```

输入一个规则，声明如果 `a` 为真则 `b` 为真：
```
input: a => b
```

系统会自动推导并显示 `=> b`：
```
fact: => b
```

### 示例 2：等式推理

输入一个等式关系 `a == b`：
```
input: => a == b
```

通过创建一个需要它的规则来输入对 `b == a` 的“想法”（Idea）：
```
input: b == a => target
```

系统将同时推导出想法和事实：
```
idea: => b == a
fact: => b == a
fact: => target
```
