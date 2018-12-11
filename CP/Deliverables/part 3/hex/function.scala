def hex(str: String) = {
  var ret = ""
  var s = 0
  while (s < str.size) {
    ret += str(s).toHexString
    s += 1
  }
  ret
}