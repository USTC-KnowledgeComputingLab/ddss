# Modules

The system consists of the following modules, implemented symmetrically in `ddss/*.py` and `ddss/*.ts`:

- **Input** (`ddss/input.py`, `ddss/input.ts`): Interactive input interface with BNF syntax parsing
- **Output** (`ddss/output.py`, `ddss/output.ts`): Real-time display of facts and ideas from the database
- **Load** (`ddss/load.py`, `ddss/load.ts`): Batch import of facts from standard input
- **Dump** (`ddss/dump.py`, `ddss/dump.ts`): Export all facts and ideas to output
- **DS** (`ddss/ds.py`, `ddss/ds.ts`): Forward-chaining deductive search engine
- **Egg** (`ddss/egg.py`, `ddss/egg.ts`): E-graph based equality reasoning engine
