// 初始事实：定义数字 1 和 2 存在
Exist(Literal(1) :: Int)
Exist(Literal(2) :: Int)

// 规则：如果 X 存在，Y 存在，且 X + Y = W，则 W 也存在
Exist(Literal(`X) :: Int), Exist(Literal(`Y) :: Int), Literal(`X) :: Int + Literal(`Y) :: Int == Literal(`W) :: Int => Exist(Literal(`W) :: Int)

// 查询：数字 5 是否存在？
Exist(Literal(5) :: Int) => Query()
