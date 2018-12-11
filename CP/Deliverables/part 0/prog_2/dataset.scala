val x = Seq(5, 7, 1, 3, 2, 1).toDS()
x.select(reduceAggregator((a:Int, b:Int) => if (a > b) a else b)).first