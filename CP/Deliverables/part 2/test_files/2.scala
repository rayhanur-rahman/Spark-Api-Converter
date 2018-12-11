sc.range(15,30)
  .map(x => { val r = x % 5; ( x, if((5 * r) > 10) r - r else if (r == 0) r + r else r * r ) } )
  .collect()