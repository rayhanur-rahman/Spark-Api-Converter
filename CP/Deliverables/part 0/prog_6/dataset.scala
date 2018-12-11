spark.range(1,100).as[Long]
  .filter(i => (i%5 == 0))
  .select(reduceAggregator((a:Long, b:Long) => a+b)).collect()