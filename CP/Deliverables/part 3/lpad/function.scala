def lpad(str: String, len: Int, pad: String) = {
  var strLength = str.length()
  var diff = len - strLength
  var ret = str
  if (diff < 0){
    ret = str.substring(0, len)
  }
  if(diff > 0 ){
    while(ret.length() < len) {
      ret = pad + ret
    }
    var ret_lenth = ret.length()
    if(ret_lenth > len){
      ret = ret.substring(ret_lenth - len, ret_lenth)
    }
  }
  ret
}