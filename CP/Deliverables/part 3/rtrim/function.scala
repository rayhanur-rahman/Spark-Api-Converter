def rtrim(str:String) = {
    var ret = ""
    var s = 0
    for (i <- s until str.size) {
        if (str(i) != ' ') {
            ret += str.substring(s, i+1)
            s = i+1
        }
    }
    ret
}