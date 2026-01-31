// 初始事实
Collinear(C, F, A)
Collinear(G, B, C)
Collinear(H, D, G)
Collinear(E, H, C)
Collinear(D, F, I)
Collinear(E, C, I)
Collinear(E, C, J)
Collinear(E, K, C)
Perp(F, J, C, E)
Perp(C, E, K, G)
Length(D, B) == Length(D, C)
Length(D, A) == Length(D, B)
Length(D, E) == Length(D, A)
Length(E, A) == Length(E, B)
Length(F, C) == Length(F, A)
Length(G, C) == Length(G, B)

// R1: DB = DC & GC = GB ⇒ BC ⟂ DG
Length(`P1, `P2) == Length(`P1, `P3), Length(`P4, `P3) == Length(`P4, `P2) => Perp(`P2, `P3, `P1, `P4)

// R2: DB = DC & DA = DB ⇒ DA = DC
Length(`P1, `P2) == Length(`P1, `P3), Length(`P1, `P4) == Length(`P1, `P2) => Length(`P1, `P4) == Length(`P1, `P3)

// R3: DA = DC & FC = FA ⇒ AC ⟂ DF
Length(`P1, `P2) == Length(`P1, `P3), Length(`P4, `P3) == Length(`P4, `P2) => Perp(`P2, `P3, `P1, `P4)

// R4: C,F,A共线 & D,F,I共线 & H,D,G共线 & G,B,C共线 & BC⟂DG & AC⟂DF ⇒ ∠CFI = ∠HGC
Collinear(`P1, `P2, `P3), Collinear(`P4, `P2, `P5), Collinear(`P6, `P4, `P7), Collinear(`P7, `P8, `P1), Perp(`P8, `P1, `P4, `P7), Perp(`P3, `P1, `P4, `P2) => Degree(`P1, `P2, `P5) == Degree(`P6, `P7, `P1)

// R5: DA=DB & DE=DA & DB=DC ⇒ D 是 △EBC 的外心
Length(`P1, `P2) == Length(`P1, `P3), Length(`P1, `P4) == Length(`P1, `P2), Length(`P1, `P3) == Length(`P1, `P5) => Circumcenter(`P1, `P4, `P3, `P5)

// R6: DA=DB & DE=DA & DB=DC ⇒ D 是 △EAC 的外心
Length(`P1, `P2) == Length(`P1, `P3), Length(`P1, `P4) == Length(`P1, `P2), Length(`P1, `P3) == Length(`P1, `P5) => Circumcenter(`P1, `P4, `P2, `P5)

// R7: DA=DB & DE=DA & DB=DC ⇒ DC = DE
Length(`P1, `P2) == Length(`P1, `P3), Length(`P1, `P4) == Length(`P1, `P2), Length(`P1, `P3) == Length(`P1, `P5) => Length(`P1, `P5) == Length(`P1, `P4)

// R8: G,B,C共线 & GC=GB ⇒ G是CB的中点
Collinear(`P1, `P2, `P3), Length(`P1, `P3) == Length(`P1, `P2) => Midpoint(`P1, `P3, `P2)

// R9: D是△EBC的外心 & G是CB的中点 ⇒ ∠DBE = ∠(DG-CE)
Circumcenter(`P1, `P2, `P3, `P4), Midpoint(`P5, `P4, `P3) => Degree(`P1, `P3, `P2) == Angle(`P1, `P5, `P4, `P2)

// R10: DA = DB & EA = EB ⇒ ∠DBE = ∠EAD
Length(`P1, `P2) == Length(`P1, `P3), Length(`P4, `P2) == Length(`P4, `P3) => Degree(`P1, `P3, `P4) == Degree(`P4, `P2, `P1)

// R11: C,F,A共线 & FC=FA ⇒ F是CA的中点
Collinear(`P1, `P2, `P3), Length(`P2, `P1) == Length(`P2, `P3) => Midpoint(`P2, `P1, `P3)

// R12: D是△EAC的外心 & F是CA的中点 ⇒ ∠EAD = ∠(CE-DF)
Circumcenter(`P1, `P2, `P3, `P4), Midpoint(`P5, `P4, `P3) => Degree(`P2, `P3, `P1) == Angle(`P4, `P2, `P1, `P5)

// R13: ∠CFI=∠HGC & ∠CIF=∠GHC ⇒ IC:HC = IF:HG
Degree(`P2, `P4, `P1) == Degree(`P3, `P5, `P2), Degree(`P2, `P1, `P4) == Degree(`P5, `P3, `P2) => Ratio(`P1, `P2, `P3, `P2) == Ratio(`P1, `P4, `P3, `P5)

// R15: D,F,I共线 & DF⟂AC ⇒ IF⟂CA
Collinear(`P1, `P2, `P3), Perp(`P4, `P5, `P1, `P2) => Perp(`P3, `P2, `P5, `P4)

// R16: F是CA的中点 & IF⟂CA ⇒ IC = IA
Midpoint(`P1, `P2, `P3), Perp(`P4, `P1, `P2, `P3) => Length(`P4, `P2) == Length(`P4, `P3)

// R19: ∠GKH=∠IJF & ∠GHK=∠JIF ⇒ GK:FJ = GH:FI
Degree(`P1, `P2, `P3) == Degree(`P4, `P5, `P6), Degree(`P1, `P3, `P2) == Degree(`P5, `P4, `P6) => Ratio(`P1, `P2, `P6, `P5) == Ratio(`P1, `P3, `P6, `P4)

// R21: DC = DE ⇒ ∠DCE = ∠CED
Length(`P1, `P2) == Length(`P1, `P3) => Degree(`P1, `P2, `P3) == Degree(`P2, `P3, `P1)

// R22: E,H,C共线 & E,C,I共线 & ∠DCE=∠CED ⇒ ∠DCH = ∠IED
Collinear(`P1, `P2, `P3), Collinear(`P1, `P3, `P4), Degree(`P5, `P3, `P1) == Degree(`P3, `P1, `P5) => Degree(`P5, `P3, `P2) == Degree(`P4, `P1, `P5)

// R23: ∠DHC=∠EID & ∠DCH=∠IED ⇒ CD:ED = CH:EI
Degree(`P1, `P2, `P3) == Degree(`P4, `P5, `P1), Degree(`P1, `P3, `P2) == Degree(`P5, `P4, `P1) => Ratio(`P3, `P1, `P4, `P1) == Ratio(`P3, `P2, `P4, `P5)

// R25: E,H,C共线 & E,C,I共线 & ∠DEC=∠ECD ⇒ ∠DEH = ∠ICD
Collinear(`P2, `P4, `P3), Collinear(`P2, `P3, `P5), Degree(`P1, `P3, `P2) == Degree(`P3, `P2, `P1) => Degree(`P1, `P2, `P4) == Degree(`P5, `P3, `P1)

// R26: ∠DHE=∠CID & ∠DEH=∠ICD ⇒ ED:CD = EH:CI
Degree(`P1, `P2, `P3) == Degree(`P4, `P5, `P1), Degree(`P1, `P3, `P2) == Degree(`P5, `P4, `P1) => Ratio(`P3, `P1, `P4, `P1) == Ratio(`P3, `P2, `P4, `P5)

// R27: GK:FJ = EI:EH
Ratio(`P1, `P2, `P3, `P2) == Ratio(`P1, `P4, `P3, `P5), Length(`P1, `P2) == Length(`P1, `P6), Ratio(`P5, `P7, `P4, `P8) == Ratio(`P5, `P3, `P4, `P1), Ratio(`P2, `P9, `P10, `P9) == Ratio(`P2, `P3, `P10, `P1), Length(`P9, `P2) == Length(`P9, `P10), Ratio(`P10, `P9, `P2, `P9) == Ratio(`P10, `P3, `P2, `P1) => Ratio(`P5, `P7, `P4, `P8) == Ratio(`P10, `P1, `P10, `P3)

// 查询：GK:FJ 是否等于 EI:EH
Ratio(G, K, F, J) == Ratio(E, I, E, H) => Query()
