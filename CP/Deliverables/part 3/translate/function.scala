def translate(input: String, from: String, to: String) = {
  var fromLen = from.length()
  var j = 0
  var result = ""
  var tempInput = input
  var index = tempInput.indexOf(from, j)
  var temp = ""
  while(j < tempInput.length && index >= 0) {
    temp = tempInput.substring(0, index)
    result = temp + to
    result += tempInput.substring(index + fromLen, tempInput.length())
    j = index + fromLen
    tempInput = result
    index = tempInput.indexOf(from, j)
  }
  result
}