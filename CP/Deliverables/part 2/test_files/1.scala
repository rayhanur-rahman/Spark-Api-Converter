sc.range(1,10)
  .map(x => (x + 2, if(x + 3 > 6) x else 1 ) )
  .collect()