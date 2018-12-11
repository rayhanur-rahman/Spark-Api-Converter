val a = spark.range(1, 9).toDF("number")
val b = spark.range(1, 3).toDF("number")
a.except(b).collect()