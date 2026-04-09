// 初始事实
Collinear(B, A, C)
Collinear(G, I, E)
Length(B, A) == Length(B, C)
Length(D, A) == Length(D, B)
Length(D, E) == Length(D, B)
Length(F, B) == Length(F, C)
Length(F, E) == Length(F, B)
Length(F, G) == Length(F, B)
Length(D, I) == Length(D, B)
Perp(A, G, A, D)

// R1: FB = FC & FG = FB & FE = FB ⇒ F 是 △CGE 的外心
Length(`P1, `P5) == Length(`P1, `P2), Length(`P1, `P3) == Length(`P1, `P5), Length(`P1, `P4) == Length(`P1, `P5) => Circumcenter(`P1, `P2, `P3, `P4)

// R2: FB = FC & FG = FB & FE = FB ⇒ G,B,E,C 共圆
Length(`P1, `P3) == Length(`P1, `P5), Length(`P1, `P2) == Length(`P1, `P3), Length(`P1, `P4) == Length(`P1, `P3) => Cyclic(`P2, `P3, `P4, `P5)

// R3: G,B,E,C 共圆 ⇒ ∠ECB = ∠EGB
Cyclic(`P1, `P2, `P3, `P4) => Degree(`P3, `P4, `P2) == Degree(`P3, `P1, `P2)

// R4: G,B,E,C 共圆 ⇒ ∠EBC = ∠EGC
Cyclic(`P1, `P2, `P3, `P4) => Degree(`P3, `P2, `P4) == Degree(`P3, `P1, `P4)

// R5: DA = DB & DI = DB & DE = DB ⇒ I,B,E,A 共圆
Length(`P1, `P5) == Length(`P1, `P3), Length(`P1, `P2) == Length(`P1, `P3), Length(`P1, `P4) == Length(`P1, `P3) => Cyclic(`P2, `P3, `P4, `P5)

// R6: I,B,E,A 共圆 ⇒ ∠IEB = ∠IAB
Cyclic(`P1, `P2, `P3, `P4) => Degree(`P1, `P3, `P2) == Degree(`P1, `P4, `P2)

// R7: B,A,C共线 & ∠EBC = ∠EGC & ∠IEB = ∠IAB & G,I,E共线 ⇒ ∠BAI = ∠ACG
Collinear(`P1, `P2, `P3), Degree(`P4, `P1, `P3) == Degree(`P4, `P5, `P3), Degree(`P6, `P4, `P1) == Degree(`P6, `P2, `P1), Collinear(`P5, `P6, `P4) => Degree(`P1, `P2, `P6) == Degree(`P2, `P3, `P5)

// R8: DA = DB & DI = DB ⇒ D 是 △ABI 的外心
Length(`P1, `P2) == Length(`P1, `P3), Length(`P1, `P4) == Length(`P1, `P3) => Circumcenter(`P1, `P2, `P3, `P4)

// R9: D是△ABI的外心 & AG ⟂ AD ⇒ ∠BAG = ∠BIA
Circumcenter(`P1, `P2, `P3, `P4), Perp(`P2, `P5, `P2, `P1) => Degree(`P3, `P2, `P5) == Degree(`P3, `P4, `P2)

// R10: B,A,C 共线 & ∠BIA = ∠BAG  ⇒  ∠BIA = ∠CAG
Collinear(`P1, `P2, `P3), Degree(`P1, `P4, `P2) == Degree(`P1, `P2, `P5) => Degree(`P1, `P4, `P2) == Degree(`P3, `P2, `P5)

// R11: ∠BAI = ∠ACG & ∠BIA = ∠CAG  =>  AB:CG = AI:CA
Degree(`P1, `P2, `P4) == Degree(`P2, `P3, `P5), Degree(`P1, `P4, `P2) == Degree(`P3, `P2, `P5) => Ratio(`P2, `P1, `P3, `P5) == Ratio(`P2, `P4, `P3, `P2)

// R12: AB:CG = AI:CA & BA = BC  =>  BC:GC = IA:CA
Ratio(`P2, `P1, `P3, `P5) == Ratio(`P2, `P4, `P3, `P2), Length(`P1, `P2) == Length(`P1, `P3) => Ratio(`P1, `P3, `P5, `P3) == Ratio(`P4, `P2, `P3, `P2)

// R13: B,A,C 共线 & ∠EBC = ∠EGC & ∠IEB = ∠IAB & G,I,E 共线  =>  ∠BCG = ∠CAI
Collinear(`P1, `P2, `P3), Degree(`P6, `P1, `P3) == Degree(`P6, `P5, `P3), Degree(`P4, `P6, `P1) == Degree(`P4, `P2, `P1), Collinear(`P5, `P4, `P6) => Degree(`P1, `P3, `P5) == Degree(`P3, `P2, `P4)

// R14: BC:GC = IA:CA & ∠BCG = ∠CAI  =>  ∠CBG = ∠CIA
Ratio(`P1, `P3, `P5, `P3) == Ratio(`P4, `P2, `P3, `P2), Degree(`P1, `P3, `P5) == Degree(`P3, `P2, `P4) => Degree(`P3, `P1, `P5) == Degree(`P3, `P4, `P2)

// R15: B,A,C 共线 & ∠EBC = ∠EGC & ∠IEB = ∠IAB & G,I,E 共线  =>  ∠(IA-BC) = ∠GCB
Collinear(`P1, `P2, `P3), Degree(`P6, `P1, `P3) == Degree(`P6, `P5, `P3), Degree(`P4, `P6, `P1) == Degree(`P4, `P2, `P1), Collinear(`P5, `P4, `P6) => Angle(`P4, `P2, `P1, `P3) == Degree(`P5, `P3, `P1)

// R16: ∠(IA-BC) = ∠GCB  =>  IA ∥ GC
Angle(`P4, `P2, `P1, `P3) == Degree(`P5, `P3, `P1) => Para(`P4, `P2, `P5, `P3)

// R17: ∠ECB = ∠EGB & B,A,C 共线 & ∠CBG = ∠CIA & IA ∥ CG  =>  ∠ICG = ∠CEG
Degree(`P6, `P3, `P1) == Degree(`P6, `P5, `P1), Collinear(`P1, `P2, `P3), Degree(`P3, `P1, `P5) == Degree(`P3, `P4, `P2), Para(`P4, `P2, `P5, `P3) => Degree(`P4, `P3, `P5) == Degree(`P3, `P6, `P5)

// R18: F is the circumcenter of CGE & ∠ICG = ∠CEG ⇒  CF ⟂ CI
Circumcenter(`P1, `P2, `P3, `P4), Degree(`P5, `P2, `P3) == Degree(`P2, `P4, `P3) => Perp(`P2, `P1, `P2, `P5)

// 查询：CF ⟂ CI？
Perp(C, F, C, I) => Query()
