// 初始事实
Collinear(B, C, A)
Collinear(B, D, F)
Collinear(E, A, G)
Collinear(C, G, F)
Collinear(B, E, H)
Collinear(C, H, F)
Collinear(C, I, F)
Collinear(D, I, A)
Para(A, E, B, D)
Para(B, E, A, D)
Length(C, A) == Length(C, B)

// R1: B,D,F 共线 & E,A,G 共线 & AE ∥ BD => DF ∥ AG
Collinear(`P1, `P2, `P3), Collinear(`P4, `P5, `P6), Para(`P5, `P4, `P1, `P2) => Para(`P2, `P3, `P5, `P6)

// R2: C,I,F 共线 & C,G,F 共线 => I,F,G 共线
Collinear(`P1, `P2, `P3), Collinear(`P1, `P4, `P3) => Collinear(`P2, `P3, `P4)

// R3: DF ∥ AG & I,F,G 共线 & D,I,A 共线 => IF/IG = FD/GA
Para(`P1, `P2, `P3, `P4), Collinear(`P5, `P2, `P4), Collinear(`P1, `P5, `P3) => Ratio(`P5, `P2, `P5, `P4) == Ratio(`P2, `P1, `P4, `P3)

// R4: B,D,F 共线 & E,A,G 共线 & AE ∥ BD => BF ∥ AG
Collinear(`P1, `P2, `P3), Collinear(`P4, `P5, `P6), Para(`P5, `P4, `P1, `P2) => Para(`P1, `P3, `P5, `P6)

// R5: BF ∥ AG & B,C,A 共线 & C,G,F 共线 => CB/CA = BF/AG
Para(`P1, `P2, `P3, `P4), Collinear(`P1, `P5, `P3), Collinear(`P5, `P4, `P2) => Ratio(`P5, `P1, `P5, `P3) == Ratio(`P1, `P2, `P3, `P4)

// R6: B,E,H 共线 & D,I,A 共线 & BE ∥ AD => BH ∥ DI
Collinear(`P1, `P2, `P3), Collinear(`P4, `P5, `P6), Para(`P1, `P2, `P6, `P4) => Para(`P1, `P3, `P4, `P5)

// R7: C,I,F 共线 & C,H,F 共线 => F,H,I 共线
Collinear(`P1, `P2, `P3), Collinear(`P1, `P4, `P3) => Collinear(`P3, `P4, `P2)

// R8: BH ∥ DI & B,D,F 共线 & F,H,I 共线 => BF/DF = HF/IF
Para(`P1, `P2, `P3, `P4), Collinear(`P1, `P3, `P5), Collinear(`P5, `P2, `P4) => Ratio(`P1, `P5, `P3, `P5) == Ratio(`P2, `P5, `P4, `P5)

// R9: IF:IG=FD:GA & CB:CA=BF:AG & CA=CB & BF:DF=HF:IF => HF:IF=IG:IF
Ratio(`P1, `P2, `P1, `P3) == Ratio(`P2, `P4, `P3, `P5), Ratio(`P6, `P7, `P6, `P5) == Ratio(`P7, `P2, `P5, `P3), Length(`P6, `P5) == Length(`P6, `P7), Ratio(`P7, `P2, `P4, `P2) == Ratio(`P8, `P2, `P1, `P2) => Ratio(`P8, `P2, `P1, `P2) == Ratio(`P1, `P3, `P1, `P2)

// R10: HF:IF = IG:IF => HF = IG
Ratio(`P1, `P2, `P3, `P2) == Ratio(`P3, `P4, `P3, `P2) => Length(`P1, `P2) == Length(`P3, `P4)

// 查询：HF 是否等于 IG？
Length(H, F) == Length(I, G) => Query()
