package Others;

import java.awt.*;

public class App {
    public static boolean checkIfCharacterIsAlpha(char ch){
        if(ch == 95 || (ch>=65 && ch <= 90) || ((ch>=97 && ch <= 122)))
            return true;
        else
            return false;
    }

    public static boolean checkIfCharacterIsAlphanumeric(char ch){
        if(ch == 95 || (ch>=65 && ch <= 90) || (ch>=97 && ch <= 122)
        || ((ch>=48 && ch <= 57)))
            return true;
        else
            return false;
    }


    public static boolean isIdentifier(String str) {
        // TODO: Implement the recognition of identifiers
        if(str.isEmpty())
            return false;
        boolean isIdentifier = false;
        char firstLetter = str.charAt(0);
        isIdentifier = checkIfCharacterIsAlpha(firstLetter);
        if(isIdentifier == false)
            return false;
        int index = 1;
        for(index = 1; index < str.length(); index = index+1){
            if (checkIfCharacterIsAlphanumeric(str.charAt(index)))
                continue;
            else
                return false;
        }
        return true;
    }

    public static void main(String[] args){
        boolean x = isIdentifier("_kk9rgfvrgA8*&");
        System.out.print(x);
    }
}
