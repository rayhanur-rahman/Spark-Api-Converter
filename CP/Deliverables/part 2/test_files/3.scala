sc.range(1,10)
  .map(x => { val z = x % 2; val y = z + 5; val m = x + y * z; ( x + 2 - y, if (z + 3 > 0) x else m - z, x * y + z) } )
  .map(r => r._1 * r._2 - r._3)
  .collect()