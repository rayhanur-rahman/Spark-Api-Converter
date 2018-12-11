val x = Seq(5, 7, 1, 3, 2, 1).toDF()
x.agg(max($"value")).as[Int].first