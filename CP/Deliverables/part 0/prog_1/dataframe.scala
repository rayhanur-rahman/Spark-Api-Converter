val x = Seq(1,2,3,4,5).toDF()
val y = Seq(6,7,8,9,10).toDF()
x.crossJoin(y).collect