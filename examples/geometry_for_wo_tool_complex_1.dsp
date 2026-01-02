// 初始事实
Collinear(F, A, C)
Collinear(F, E, B)
Collinear(D, B, G)
Collinear(A, G, C)
Collinear(D, B, H)
Collinear(I, A, D)
Collinear(E, I, C)
Collinear(E, J, B)
Length(K, A) == Length(K, F)
Length(K, F) == Length(K, J)
Length(L, F) == Length(L, G)
Length(L, B) == Length(L, F)
Length(M, G) == Length(M, H)
Length(M, C) == Length(M, G)
Length(N, D) == Length(N, H)
Length(N, H) == Length(N, I)
Length(O, E) == Length(O, I)
Length(O, I) == Length(O, J)
Length(K, P) == Length(K, F)
Length(L, P) == Length(L, F)
Length(M, Q) == Length(M, G)
Length(L, Q) == Length(L, G)
Length(N, R) == Length(N, H)
Length(M, R) == Length(M, H)
Length(K, T) == Length(K, J)
Length(O, T) == Length(O, J)
Length(O, S) == Length(O, I)

// R1: KA=KF & KF=KJ & KT=KJ => F,A,J,T 共圆
Length(`P1, `P2) == Length(`P1, `P3), Length(`P1, `P3) == Length(`P1, `P4), Length(`P1, `P5) == Length(`P1, `P4) => Cyclic(`P3, `P2, `P4, `P5)

// R2: F,A,J,T 共圆 & KA=KF & KP=KF & KF=KJ => A,F,P,T 共圆
Cyclic(`P1, `P2, `P3, `P4), Length(`P5, `P2) == Length(`P5, `P1), Length(`P5, `P6) == Length(`P5, `P1), Length(`P5, `P1) == Length(`P5, `P3) => Cyclic(`P2, `P1, `P6, `P4)

// R3: ND=NH & NR=NH & NH=NI => D,I,R,H 共圆
Length(`P1, `P2) == Length(`P1, `P3), Length(`P1, `P4) == Length(`P1, `P3), Length(`P1, `P3) == Length(`P1, `P5) => Cyclic(`P2, `P5, `P4, `P3)

// R4: D,I,R,H 共圆 => ∠DHR=∠DIR
Cyclic(`P1, `P2, `P3, `P4) => Degree(`P1, `P4, `P3) == Degree(`P1, `P2, `P3)

// R5: MG=MH & MR=MH & MC=MG => H,C,R,G 共圆
Length(`P1, `P2) == Length(`P1, `P3), Length(`P1, `P4) == Length(`P1, `P3), Length(`P1, `P5) == Length(`P1, `P2) => Cyclic(`P3, `P5, `P4, `P2)

// R6: H,C,R,G 共圆 => ∠HGC=∠HRC
Cyclic(`P1, `P2, `P3, `P4) => Degree(`P1, `P4, `P2) == Degree(`P1, `P3, `P2)

// R7: I,A,D共线 & ∠DHR=∠DIR & D,B,H共线 & ∠HGC=∠HRC & D,B,G共线 & A,G,C共线 => ∠ACR=∠AIR
Collinear(`P1, `P2, `P3), Degree(`P3, `P4, `P5) == Degree(`P3, `P1, `P5), Collinear(`P3, `P6, `P4), Degree(`P4, `P7, `P8) == Degree(`P4, `P5, `P8), Collinear(`P3, `P6, `P7), Collinear(`P2, `P7, `P8) => Degree(`P2, `P8, `P5) == Degree(`P2, `P1, `P5)

// R8: ∠ACR=∠AIR => A,I,R,C 共圆
Degree(`P1, `P2, `P3) == Degree(`P1, `P4, `P3) => Cyclic(`P1, `P4, `P3, `P2)

// R9: OE=OI & OI=OJ & OT=OJ & OS=OI => E,I,J,T 共圆
Length(`P1, `P2) == Length(`P1, `P3), Length(`P1, `P3) == Length(`P1, `P4), Length(`P1, `P5) == Length(`P1, `P4), Length(`P1, `P6) == Length(`P1, `P3) => Cyclic(`P2, `P3, `P5, `P5)

// R11: E,I,J,T 共圆 => ∠JTI=∠JEI
Cyclic(`P1, `P2, `P3, `P4) => Degree(`P3, `P2, `P4) == Degree(`P3, `P1, `P2)

// R12: F,A,J,T 共圆 => ∠AFJ=∠ATJ
Cyclic(`P1, `P2, `P3, `P4) => Degree(`P2, `P1, `P3) == Degree(`P2, `P4, `P3)

// R13: E,I,C共线 & ∠JTI=∠JEI & E,J,B共线 & ∠AFJ=∠ATJ & F,A,C共线 & F,E,B共线 => ∠CAT=∠CIT
Collinear(`P1, `P2, `P3), Degree(`P4, `P2, `P8) == Degree(`P4, `P1, `P2), Collinear(`P1, `P4, `P6), Degree(`P7, `P5, `P4) == Degree(`P7, `P8, `P4), Collinear(`P5, `P7, `P3), Collinear(`P5, `P1, `P6) => Degree(`P3, `P7, `P8) == Degree(`P3, `P2, `P8)

// R14: ∠CAT=∠CIT => A,I,T,C 共圆
Degree(`P1, `P2, `P3) == Degree(`P1, `P4, `P3) => Cyclic(`P2, `P4, `P3, `P1)

// R15: A,I,R,C 共圆 & A,I,T,C 共圆 => A,C,T,R 共圆
Cyclic(`P1, `P2, `P3, `P4), Cyclic(`P1, `P2, `P5, `P4) => Cyclic(`P1, `P4, `P5, `P3)

// R16: ∠AFP=∠ATP & F,A,C共线 & ∠CAT=∠CRT => ∠CRT=∠FPT
Degree(`P1, `P2, `P3) == Degree(`P1, `P4, `P3), Collinear(`P2, `P1, `P5), Degree(`P5, `P1, `P4) == Degree(`P5, `P6, `P4) => Degree(`P5, `P6, `P4) == Degree(`P2, `P3, `P4)

// R17: H,C,R,G 共圆 & MG=MH & MQ=MG & MC=MG => C,R,G,Q 共圆
Cyclic(`P1, `P2, `P3, `P4), Length(`P5, `P4) == Length(`P5, `P1), Length(`P5, `P6) == Length(`P5, `P4), Length(`P5, `P2) == Length(`P5, `P4) => Cyclic(`P2, `P3, `P4, `P6)

// R18: Q,G,C,R 共圆 => ∠QGC=∠QRC
Cyclic(`P1, `P2, `P3, `P4) => Degree(`P1, `P2, `P3) == Degree(`P1, `P4, `P3)

// R19: LP=LF & LF=LG & LQ=LG & LB=LF => F,Q,P,G 共圆
Length(`P1, `P2) == Length(`P1, `P3), Length(`P1, `P3) == Length(`P1, `P4), Length(`P1, `P5) == Length(`P1, `P4), Length(`P1, `P6) == Length(`P1, `P3) => Cyclic(`P3, `P5, `P2, `P4)

// R20: F,Q,P,G 共圆 => ∠FPQ=∠FGQ
Cyclic(`P1, `P2, `P3, `P4) => Degree(`P1, `P3, `P2) == Degree(`P1, `P4, `P2)

// R21: ∠QGC=∠QRC & A,G,C共线 & ∠FPQ=∠FGQ & F,A,C共线 => ∠FPQ=∠CRQ
Degree(`P1, `P2, `P3) == Degree(`P1, `P4, `P3), Collinear(`P6, `P2, `P3), Degree(`P5, `P7, `P1) == Degree(`P5, `P2, `P1), Collinear(`P5, `P6, `P3) => Degree(`P5, `P7, `P1) == Degree(`P3, `P4, `P1)

// R22: ∠CRT=∠FPT & ∠FPQ=∠CRQ => ∠TPQ=∠TRQ
Degree(`P1, `P2, `P3) == Degree(`P4, `P5, `P3), Degree(`P4, `P5, `P6) == Degree(`P1, `P2, `P6) => Degree(`P3, `P5, `P6) == Degree(`P3, `P2, `P6)

// R23: ∠TPQ=∠TRQ => Q,P,R,T 共圆
Degree(`P3, `P5, `P6) == Degree(`P3, `P2, `P6) => Cyclic(`P6, `P5, `P2, `P3)

// 查询：A,I,T,C 是否共圆？
Cyclic(A, I, T, C) => Query()
