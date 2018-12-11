spark.range(1,100).selectExpr("id as _1")
     .selectExpr("if(_1%5==0, _1, _1*0) as _1")
     .selectExpr("sum(_1)")
     .as[Long].first
     

