val y = sc.parallelize(Array(5, 7, 1, 3, 2, 1))
y.reduce((a, b) => if (a > b) a else b)


