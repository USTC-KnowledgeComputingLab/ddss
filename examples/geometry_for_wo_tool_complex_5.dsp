// 初始事实
Collinear(D, F, C)
Collinear(F, B, E)
Perp(F, H, F, G)
Length(A, C) == Length(A, B)
Length(A, D) == Length(A, B)
Length(A, E) == Length(A, B)
Length(G, F) == Length(G, B)
Length(G, D) == Length(G, F)

// 规则 R1: AD=AB, AE=AB, AC=AB => D,B,E,C 共圆
Length(`P1, `P2) == Length(`P1, `P3), Length(`P1, `P4) == Length(`P1, `P3), Length(`P1, `P5) == Length(`P1, `P3) => Cyclic(`P2, `P3, `P4, `P5)

// 规则 R2: 四点共圆 => 圆周角相等 ∠EBD = ∠ECD
Cyclic(`P1, `P2, `P3, `P4) => Degree(`P3, `P2, `P1) == Degree(`P3, `P4, `P1)

// 规则 R3: GF=GB, GD=GF => G 是 △FBD 的外心
Length(`P1, `P2) == Length(`P1, `P3), Length(`P1, `P4) == Length(`P1, `P2) => Circumcenter(`P1, `P2, `P3, `P4)

// 规则 R4: 外心 + 垂直关系 => 弦切角性质 ∠HFB = ∠FDB
Circumcenter(`P1, `P2, `P3, `P4), Perp(`P2, `P5, `P2, `P1) => Degree(`P5, `P2, `P3) == Degree(`P2, `P4, `P3)

// 规则 R5: 综合共线与角度相等推导角度关系 ∠HFD = Angle(EC, DF)
Collinear(`P1, `P2, `P3), Degree(`P4, `P5, `P1) == Degree(`P4, `P3, `P1), Degree(`P6, `P2, `P5) == Degree(`P2, `P1, `P5), Collinear(`P2, `P5, `P4) => Degree(`P6, `P2, `P1) == Angle(`P4, `P3, `P1, `P2)

// 规则 R6: 角度相等 => FH ∥ EC
Degree(`P1, `P2, `P3) == Angle(`P4, `P5, `P3, `P2) => Para(`P2, `P1, `P4, `P5)

// 查询：FH 是否平行于 EC？
Para(F, H, E, C) => Query()
