// 初始事实
Father(Alice, Bob)   // Alice 是 Bob 的父亲（此处沿用代码逻辑）
Brother(Bob, Carie)  // Bob 是 Carie 的兄弟
Brother(Mark, Dick)  // Mark 是 Dick 的兄弟
Father(Mark, Bob)    // Mark 是 Bob 的父亲

// 规则 R1: 如果 X 是 Y 的父亲且 Y 是 Z 的兄弟，则 X 是 Z 的叔伯
Father(`X, `Y), Brother(`Y, `Z) => Uncle(`X, `Z)

// 规则 R2: 如果 X 和 Y 都是 Z 的父亲，则 X 和 Y 是同胞
Father(`X, `Z), Father(`Y, `Z) => Sibling(`X, `Y)

// 规则 R3: 如果 X 是 Z 的叔伯且 X 与 Y 是同胞，则 Y 也是 Z 的叔伯
Uncle(`X, `Z), Sibling(`X, `Y) => Uncle(`Y, `Z)

// 查询：Mark 是谁的叔伯？
Uncle(Mark, `X) => Query(`X)
