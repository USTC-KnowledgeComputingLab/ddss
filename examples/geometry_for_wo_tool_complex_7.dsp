// 初始事实
Para(E, D, B, C)
Para(G, D, C, F)
Length(A, C) == Length(A, B)
Length(A, D) == Length(A, B)
Length(A, E) == Length(A, B)
Length(A, F) == Length(A, B)
Length(A, G) == Length(A, B)

// R1: AD = AB & AF = AB & AE = AB & AC = AB ⇒ F,D,E,C 共圆
Length(`P1, `P2) == Length(`P1, `P3), Length(`P1, `P4) == Length(`P1, `P3), Length(`P1, `P5) == Length(`P1, `P3), Length(`P1, `P6) == Length(`P1, `P3) => Cyclic(`P4, `P2, `P5, `P6)

// R2: AF=AB & AG=AB & AE=AB & AD=AB & AC=AB ⇒ G,E,B,C 共圆
Length(`P1, `P2) == Length(`P1, `P3), Length(`P1, `P4) == Length(`P1, `P3), Length(`P1, `P5) == Length(`P1, `P3), Length(`P1, `P6) == Length(`P1, `P3), Length(`P1, `P7) == Length(`P1, `P3) => Cyclic(`P4, `P5, `P3, `P7)

// R3: G,E,B,C 共圆 ⇒ ∠BGE = ∠BCE
Cyclic(`P1, `P2, `P3, `P4) => Degree(`P3, `P1, `P2) == Degree(`P3, `P4, `P2)

// R4: F,D,E,C 共圆 ⇒ ∠DFC = ∠DEC
Cyclic(`P1, `P2, `P3, `P4) => Degree(`P2, `P1, `P4) == Degree(`P2, `P3, `P4)

// R5: AF=AB & AG=AB & AE=AB & AD=AB & AC=AB ⇒ G,F,D,E 共圆
Length(`P1, `P2) == Length(`P1, `P3), Length(`P1, `P4) == Length(`P1, `P3), Length(`P1, `P5) == Length(`P1, `P3), Length(`P1, `P6) == Length(`P1, `P3), Length(`P1, `P7) == Length(`P1, `P3) => Cyclic(`P4, `P2, `P6, `P5)

// R6: G,F,D,E 共圆 ⇒ ∠GDF = ∠GEF
Cyclic(`P1, `P2, `P3, `P4) => Degree(`P1, `P3, `P2) == Degree(`P1, `P4, `P2)

// R7: ∠BGE=∠BCE & ∠DFC=∠DEC & DE∥BC & ∠GDF=∠GEF & DG∥CF ⇒ ∠FEG = ∠BGE
Degree(`P1, `P2, `P3) == Degree(`P1, `P4, `P3), Degree(`P5, `P6, `P4) == Degree(`P5, `P3, `P4), Para(`P5, `P3, `P1, `P4), Degree(`P2, `P5, `P6) == Degree(`P2, `P3, `P6), Para(`P5, `P2, `P4, `P6) => Degree(`P6, `P3, `P2) == Degree(`P1, `P2, `P3)

// R8: ∠FEG = ∠BGE ⇒ FE ∥ GB
Degree(`P1, `P2, `P3) == Degree(`P4, `P3, `P2) => Para(`P1, `P2, `P3, `P4)

// 查询：FE 是否平行于 GB？
Para(F, E, G, B) => Query()
