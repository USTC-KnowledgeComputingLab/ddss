// 初始事实：定义父母关系
Parent(Alice, Bob)
Parent(Bob, Carie)

// 规则：如果 X 是 Y 的父母，且 Y 是 Z 的父母，则 X 是 Z 的祖父母
Parent(`X, `Y), Parent(`Y, `Z) => GrandParent(`X, `Z)

// 查询：寻找 Alice 的所有孙辈
GrandParent(Alice, `X) => Query(`X)
