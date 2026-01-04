// 初始事实
Collinear(B, E, C)
Collinear(A, D, E)
Collinear(A, F, C)
Collinear(B, D, F)
Collinear(B, I, C)
Collinear(A, G, B)
Collinear(G, D, C)
Collinear(A, H, C)
Collinear(D, I, C)
Collinear(B, J, F)
Para(B, H, E, F)
Para(E, I, A, B)
Para(J, E, A, C)
Intro(A)
Intro(B)
Intro(C)
Intro(D)
Intro(E)
Intro(F)
Intro(G)
Intro(H)
Intro(I)
Intro(J)

// R1: A,B,G 共线 & EI ∥ AB => BG ∥ EI
Collinear(`P1, `P3, `P2), Para(`P4, `P5, `P1, `P2) => Para(`P2, `P3, `P4, `P5)

// R2: D,I,C 共线 & G,D,C 共线 => C,G,I 共线
Collinear(`P1, `P2, `P3), Collinear(`P4, `P1, `P3) => Collinear(`P3, `P4, `P2)

// R3: D,I,C 共线 & G,D,C 共线 => D,G,I 共线
Collinear(`P1, `P2, `P3), Collinear(`P4, `P1, `P3) => Collinear(`P1, `P4, `P2)

// R4: BG ∥ EI & B,E,C 共线 & C,G,I 共线 => BC:EC = BG:IE
Para(`P1, `P2, `P3, `P4), Collinear(`P1, `P3, `P5), Collinear(`P5, `P2, `P4) => Ratio(`P1, `P5, `P3, `P5) == Ratio(`P1, `P2, `P4, `P3)

// R5: A,H,C 共线 & A,F,C 共线 => C,H,F 共线
Collinear(`P1, `P2, `P3), Collinear(`P1, `P4, `P3) => Collinear(`P3, `P2, `P4)

// R6: BH ∥ EF & B,E,C 共线 & C,H,F 共线 => BC:EC = BH:EF
Para(`P1, `P2, `P3, `P4), Collinear(`P1, `P3, `P5), Collinear(`P5, `P2, `P4) => Ratio(`P1, `P5, `P3, `P5) == Ratio(`P1, `P2, `P3, `P4)

// R7: A,H,C 共线 & A,F,C 共线 & BH ∥ EF & AC ∥ EJ => ∠BHF = ∠FEJ
Collinear(`P1, `P2, `P3), Collinear(`P1, `P4, `P3), Para(`P5, `P2, `P6, `P4), Para(`P7, `P6, `P1, `P3) => Degree(`P5, `P2, `P4) == Degree(`P4, `P6, `P7)

// R8: B,D,F 共线 & A,H,C 共线 & A,F,C 共线 & B,J,F 共线 & AC ∥ EJ => ∠BFH = ∠FJE
Collinear(`P1, `P2, `P3), Collinear(`P4, `P5, `P6), Collinear(`P4, `P3, `P6), Collinear(`P1, `P7, `P3), Para(`P7, `P8, `P4, `P6) => Degree(`P1, `P3, `P5) == Degree(`P3, `P7, `P8)

// R9: ∠BHF = ∠FEJ & ∠BFH = ∠FJE => BH:EF = HF:JE
Degree(`P1, `P2, `P3) == Degree(`P3, `P4, `P5), Degree(`P1, `P3, `P2) == Degree(`P3, `P5, `P4) => Ratio(`P1, `P2, `P4, `P3) == Ratio(`P2, `P3, `P5, `P4)

// R10: 传递性推导
Ratio(`P1, `P2, `P3, `P2) == Ratio(`P1, `P4, `P5, `P3), Ratio(`P1, `P2, `P3, `P2) == Ratio(`P1, `P6, `P3, `P7), Ratio(`P1, `P6, `P3, `P7) == Ratio(`P6, `P7, `P8, `P3) => Ratio(`P6, `P7, `P8, `P3) == Ratio(`P1, `P4, `P5, `P3)

// R11: A,G,B 共线 & EI ∥ AB => AG ∥ EI
Collinear(`P1, `P2, `P3), Para(`P4, `P5, `P1, `P3) => Para(`P1, `P2, `P4, `P5)

// R12: AG ∥ EI & A,D,E 共线 & G,D,I 共线 => DE:AD = IE:AG
Para(`P1, `P2, `P3, `P4), Collinear(`P1, `P5, `P3), Collinear(`P2, `P5, `P4) => Ratio(`P5, `P3, `P1, `P5) == Ratio(`P4, `P3, `P1, `P2)

// R13: A,C,F 共线 & EJ ∥ AC => JE ∥ FA
Collinear(`P1, `P3, `P2), Para(`P4, `P5, `P1, `P2) => Para(`P4, `P5, `P3, `P1)

// R14: B,J,F 共线 & B,D,F 共线 => D,J,F 共线
Collinear(`P1, `P2, `P3), Collinear(`P1, `P4, `P3) => Collinear(`P4, `P2, `P3)

// R15: JE ∥ FA & A,D,E 共线 & D,J,F 共线 => DE:AD = JE:AF
Para(`P1, `P2, `P3, `P4), Collinear(`P4, `P5, `P2), Collinear(`P5, `P1, `P3) => Ratio(`P5, `P2, `P4, `P5) == Ratio(`P1, `P2, `P4, `P3)

// R16: 传递性推导
Ratio(`P1, `P2, `P3, `P1) == Ratio(`P4, `P2, `P3, `P5), Ratio(`P1, `P2, `P3, `P1) == Ratio(`P6, `P2, `P3, `P7) => Ratio(`P6, `P2, `P3, `P7) == Ratio(`P4, `P2, `P3, `P5)

// R17: 传递性推导
Ratio(`P1, `P2, `P3, `P4) == Ratio(`P5, `P6, `P7, `P4), Ratio(`P3, `P4, `P8, `P2) == Ratio(`P7, `P4, `P8, `P6) => Ratio(`P1, `P2, `P8, `P2) == Ratio(`P5, `P6, `P8, `P6)

// 查询：HF/AF = BG/AG ?
Ratio(H, F, A, F) == Ratio(B, G, A, G) => Query()
