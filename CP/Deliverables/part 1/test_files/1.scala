sc.range(1,100000)
  .filter(i => (i%5 == 0))
  .reduce((a:Long, b:Long) => a+b)