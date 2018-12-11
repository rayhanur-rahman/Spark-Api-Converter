val x = Seq(5, 7, 1, 3, 2, 1).toDS()
x.sort($"value".asc).collect()