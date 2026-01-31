// 初始事实
Collinear(D, B, H)
Length(C, A) == Length(C, B)
Length(C, D) == Length(C, A)
Length(C, F) == Length(C, A)
Length(F, C) == Length(F, D)
Length(C, G) == Length(C, A)
Length(G, C) == Length(G, D)

// 规则 R1: 如果 CF=CA, CG=CA, CA=CB, CE=CA, CD=CA，则 B, G, F, D 四点共圆
Length(`P1, `P2) == Length(`P1, `P3), Length(`P1, `P4) == Length(`P1, `P3), Length(`P1, `P3) == Length(`P1, `P5), Length(`P1, `P6) == Length(`P1, `P3), Length(`P1, `P7) == Length(`P1, `P3) => Cyclic(`P5, `P4, `P2, `P7)

// 规则 R2: 四点共圆引出的圆周角相等：∠DBG = ∠DFG
Cyclic(`P1, `P2, `P3, `P4) => Degree(`P2, `P3, `P1) == Degree(`P2, `P4, `P1)

// 规则 R3: 四点共圆引出的圆周角相等：∠FGD = ∠FBD
Cyclic(`P1, `P2, `P3, `P4) => Degree(`P4, `P1, `P2) == Degree(`P4, `P3, `P2)

// 规则 R4: 通过边长相等推导：GC=GD, CG=CA, CF=CA, FC=FD => DF=DG
Length(`P1, `P2) == Length(`P1, `P3), Length(`P2, `P1) == Length(`P2, `P4), Length(`P2, `P5) == Length(`P2, `P4), Length(`P5, `P2) == Length(`P5, `P3) => Length(`P3, `P5) == Length(`P3, `P1)

// 规则 R5: 等腰三角形推导底角相等：DF=DG => ∠DFG = ∠FGD
Length(`P1, `P2) == Length(`P1, `P3) => Degree(`P1, `P2, `P3) == Degree(`P2, `P3, `P1)

// 规则 R6: 综合共线与角度相等推导角平分关系：∠FBH = ∠HBG
Collinear(`P1, `P2, `P3), Degree(`P1, `P2, `P4) == Degree(`P1, `P5, `P4), Degree(`P1, `P5, `P4) == Degree(`P5, `P4, `P1), Degree(`P5, `P4, `P1) == Degree(`P5, `P2, `P1) => Degree(`P5, `P2, `P3) == Degree(`P3, `P2, `P4)

// 查询：∠FBH 是否等于 ∠HBG？
Degree(F, B, H) == Degree(H, B, G) => Query()
