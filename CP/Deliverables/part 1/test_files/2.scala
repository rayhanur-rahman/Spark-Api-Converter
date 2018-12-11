sc.textFile("sample.txt")
  .map(line => line.split(" ").size)
  .reduce((a:Int, b:Int) => if (a > b) a else b)