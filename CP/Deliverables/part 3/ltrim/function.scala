def ltrim(str: String) = {
    var (s, e) = (0, str.size)
    for (i <- 0 until str.size) {
        if (s == i && str(i) == ' ') s += 1
    }
    str.substring(s, e)
}