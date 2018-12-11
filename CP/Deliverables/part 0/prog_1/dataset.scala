val x = Seq(1,2,3,4,5).toDS()
val y = Seq(6,7,8,9,10).toDS()
x.crossJoin(y).collect