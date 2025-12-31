# Introduction

Distributed Deductive System Sorts (DDSS) is a distributed deductive system with a scalable architecture, providing identical implementations in both **Python** and **TypeScript**. It currently supports distributed engines including forward-chaining, E-graph, and more.

## Design Philosophy

DDSS adopts a modular architecture that decomposes the deductive system into independent but collaborative sub-systems:

1. **Separation of Concerns**: Each module focuses on a specific reasoning task.
2. **Concurrent Execution**: All modules collaborate asynchronously through a shared database, fully utilizing system resources.
3. **Persistent Storage**: Uses a database to store facts and ideas, ensuring data consistency.

### Central Hub Logic

The system uses a database as the central hub, with two tables (`facts` and `ideas`) for interaction between sub-systems:

- **Eager engines** (e.g., forward-chaining): Read facts and eagerly produce new facts. They also add ideas to broadcast "I want this XXX" - indicating what new facts they need to produce more results.

- **Lazy engines** (e.g., E-graph): Could produce too many facts if eager, so they quietly accept facts without producing many. They only produce facts when they see ideas from other engines that they can (partially) fulfill.
