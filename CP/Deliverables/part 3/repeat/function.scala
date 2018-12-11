def repeat(str: String, count: Int) = {
  var ret = ""
  var i = 0
  while (i < count) {
    ret += str
    i += 1
  }
  ret
}