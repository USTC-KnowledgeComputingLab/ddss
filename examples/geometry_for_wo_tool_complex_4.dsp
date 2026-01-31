// 初始事实
Collinear(A, B, E)
Collinear(G, C, E)
Collinear(G, A, D)
Collinear(H, C, E)
Perp(B, C, A, D)
Perp(C, E, A, B)
Length(F, A) == Length(F, C)
Length(F, A) == Length(F, B)
Length(F, H) == Length(F, C)

// R1: G,C,E 共线 & A,B,E 共线 & H,C,E 共线 & CE ⟂ AB ⇒ ∠GEA = ∠AEH
Collinear(`P1, `P2, `P3), Collinear(`P4, `P5, `P3), Collinear(`P6, `P2, `P3), Perp(`P2, `P3, `P4, `P5) => Degree(`P1, `P3, `P4) == Degree(`P4, `P3, `P6)

// R2: FA = FC & FH = FC & FA = FB ⇒ H,A,B,C 共圆
Length(`P1, `P2) == Length(`P1, `P3), Length(`P1, `P4) == Length(`P1, `P3), Length(`P1, `P2) == Length(`P1, `P5) => Cyclic(`P4, `P2, `P5, `P3)

// R3: H,A,B,C 共圆 ⇒ ∠HAB = ∠HCB
Cyclic(`P1, `P2, `P3, `P4) => Degree(`P1, `P2, `P3) == Degree(`P1, `P4, `P3)

// R4: G,A,D 共线 & BC ⟂ AD ⇒ CB ⟂ GA
Collinear(`P1, `P2, `P3), Perp(`P4, `P5, `P2, `P3) => Perp(`P5, `P4, `P1, `P2)

// R5: H,C,E 共线 & G,C,E 共线 & CE ⟂ AB ⇒ AB ⟂ GH
Collinear(`P1, `P2, `P3), Collinear(`P4, `P2, `P3), Perp(`P2, `P3, `P5, `P6) => Perp(`P5, `P6, `P4, `P1)

// R6: CB ⟂ GA & AB ⟂ GH ⇒ ∠(CB-GH) = ∠GAB
Perp(`P1, `P2, `P3, `P4), Perp(`P4, `P2, `P3, `P5) => Angle(`P1, `P2, `P3, `P5) == Degree(`P3, `P4, `P2)

// R7: G,A,D共线 & A,B,E共线 & ∠HAB=∠HCB & H,C,E共线 & ∠(CB-GH)=∠GAB & G,C,E共线 ⇒ ∠GAE=∠EAH
Collinear(`P1, `P2, `P3), Collinear(`P2, `P4, `P5), Degree(`P6, `P2, `P4) == Degree(`P6, `P7, `P4), Collinear(`P6, `P7, `P5), Angle(`P7, `P4, `P1, `P6) == Degree(`P1, `P2, `P4), Collinear(`P1, `P7, `P5) => Degree(`P1, `P2, `P5) == Degree(`P6, `P2, `P5)

// R8: ∠GEA = ∠AEH & ∠GAE = ∠EAH ⇒ EG = EH
Degree(`P1, `P2, `P3) == Degree(`P4, `P2, `P3), Degree(`P1, `P3, `P2) == Degree(`P4, `P3, `P2) => Length(`P2, `P1) == Length(`P2, `P4)

// 查询：EG 是否等于 EH？
Length(E, G) == Length(E, H) => Query()
