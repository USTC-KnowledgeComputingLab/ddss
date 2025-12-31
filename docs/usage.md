# Usage

The usage, command-line options, and interactive syntax are identical regardless of the implementation language used.

## Basic Usage

Run DDSS with a temporary SQLite database:

```bash
ddss
```

## Specifying a Database

DDSS supports multiple database backends using the `-a` or `--addr` option:

```bash
# SQLite (persistent)
ddss --addr sqlite:///path/to/database.db

# MySQL
ddss --addr mysql://user:password@host:port/database

# MariaDB
ddss --addr mariadb://user:password@host:port/database

# PostgreSQL
ddss --addr postgresql://user:password@host:port/database
```

## Selecting Components

By default, DDSS runs with all interactive components (`input`, `output`, `ds`, `egg`). You can select specific components using the `-c` or `--component` option:

```bash
# Run only input and output (no inference engines)
ddss --component input output

# Run with only the forward-chaining engine
ddss --component input output ds

# Run with only the E-graph engine
ddss --component input output egg
```

Available components:
- `input`: Interactive input interface
- `output`: Real-time display of facts and ideas
- `ds`: Forward-chaining deductive search engine
- `egg`: E-graph based equality reasoning engine
- `load`: Batch import facts from standard input
- `dump`: Export all facts and ideas to output

## Interactive Usage

After starting, input facts and rules at the `input:` prompt. The syntax follows the format `premise => conclusion`:

### Example 1: Simple Inference

Input a fact stating `a` is true:
```
input: => a
```

Input a rule stating if `a` then `b`:
```
input: a => b
```

The system automatically derives and displays `=> b`:
```
fact: => b
```

### Example 2: Equality Reasoning

Input an equality relation `a == b`:
```
input: => a == b
```

Input an idea for `b == a` by creating a rule that requires it:
```
input: b == a => target
```

The system will derive both the idea and facts:
```
idea: => b == a
fact: => b == a
fact: => target
```
