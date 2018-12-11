def concat(strs: String*) :String = {
  var ret = ""
  for(i <- 0 until strs.size){
    ret += strs(i)
  }
  ret
}