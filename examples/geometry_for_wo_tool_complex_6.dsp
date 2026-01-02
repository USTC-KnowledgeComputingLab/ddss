// 初始事实
Collinear(F, A, C)
Collinear(F, B, E)
Collinear(A, G, B)
Collinear(G, H, E)
Perp(E, F, A, C)
Perp(E, G, A, B)
Length(D, A) == Length(D, B)
Length(D, B) == Length(D, C)
Length(D, E) == Length(D, A)
Length(D, H) == Length(D, E)

// R1: A,G,B共线 & F,A,C共线 & EF⟂AC & EG⟂AB ⇒ ∠EGA = ∠EFA
Collinear(`P1, `P2, `P3), Collinear(`P4, `P1, `P5), Perp(`P6, `P4, `P1, `P5), Perp(`P6, `P2, `P1, `P3) => Degree(`P6, `P2, `P1) == Degree(`P6, `P4, `P1)

// R2: ∠EGA = ∠EFA ⇒ F,A,G,E 共圆
Degree(`P1, `P2, `P3) == Degree(`P1, `P4, `P3) => Cyclic(`P4, `P3, `P2, `P1)

// R3: F,A,G,E 共圆 ⇒ ∠FAE = ∠FGE
Cyclic(`P1, `P2, `P3, `P4) => Degree(`P1, `P2, `P4) == Degree(`P1, `P3, `P4)

// R4: DA=DB & DE=DA & DH=DE & DB=DC ⇒ A,C,H,E 共圆
Length(`P1, `P2) == Length(`P1, `P3), Length(`P1, `P4) == Length(`P1, `P2), Length(`P1, `P5) == Length(`P1, `P4), Length(`P1, `P3) == Length(`P1, `P6) => Cyclic(`P2, `P6, `P5, `P4)

// R5: A,C,H,E 共圆 ⇒ ∠ACH = ∠AEH
Cyclic(`P1, `P2, `P3, `P4) => Degree(`P1, `P2, `P3) == Degree(`P1, `P4, `P3)

// R6: G,H,E共线 & ∠FAE=∠FGE & F,A,C共线 & ∠ACH=∠AEH ⇒ ∠CHG=∠FGH
Collinear(`P1, `P2, `P3), Degree(`P4, `P5, `P3) == Degree(`P4, `P1, `P3), Collinear(`P4, `P5, `P6), Degree(`P5, `P6, `P2) == Degree(`P5, `P3, `P2) => Degree(`P6, `P2, `P1) == Degree(`P4, `P1, `P2)

// R7: ∠CHG = ∠FGH ⇒ HC ∥ FG
Degree(`P1, `P2, `P3) == Degree(`P4, `P3, `P2) => Para(`P2, `P1, `P4, `P3)

// 查询：HC 是否平行于 FG？
Para(H, C, F, G) => Query()
