def unhex(hex: String) = {
  val sb = new StringBuilder
  for (i <- 0 until hex.size by 2) {
    val str = hex.substring(i, i + 2)
    sb.append(Integer.parseInt(str, 16).toChar)
  }
  sb.toString
}