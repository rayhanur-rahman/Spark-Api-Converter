val a = spark.range(1, 9)
val b = spark.range(1, 3)
a.except(b).collect()