import java.util.*;
import java.lang.*;
import java.time.*;

public class distance1
{
    static int Penalty(char c)
    {
        return c;
    }

    static String Remove(String s, int i)
    {
        String r = i > 0 ? s.substring(0, i) : "";
        if (i < s.length()) r += s.substring(i + 1);
        return r;
    }

    static int Distance1(String a, String b)
    {
        int la = a.length(), lb = b.length();
        if (la == lb && a.compareTo(b) == 0) return 0;
        int d = Integer.MAX_VALUE; // TotalPenalty(a + b);
        for (int i = 0; i < la; i++)
            d = Math.min(d, Penalty(a.charAt(i)) + Distance1(Remove(a, i), b));
        for (int i = 0; i < lb; i++)
            d = Math.min(d, Penalty(b.charAt(i)) + Distance1(a, Remove(b, i)));
        return d;
    }

    static void assert1(boolean ok)
    {
        if (!ok)
        {
            System.out.println("*************** ERROR ***************\n");
        }
    }

    public static void main(String[] args) {
        assert1(Distance1("at", "cat") == Penalty('c'));
        assert1(Distance1("bat", "cat") == Penalty('b') + Penalty('c'));
        assert1(Distance1("!~!", "~!!") == 2 * Penalty('!'));
        assert1(Distance1("!!~", "!~!") == 2 * Penalty('!'));
        long t1 = System.nanoTime();
        int n = 0, N = 0, total_score = 0;
        while (n <= 99999) {
            String s = String.format("%05d", n);
            for (int i = 0; i <= 5; i++) {
                String a = s.substring(0, i);
                String b = s.substring(i);
                int score1 = Distance1(a, b);
                int score2 = Distance1(b, a);
                N += 2;
                total_score += score1;
                assert1(score1 == score2);
            }
            n += 1;
        }
        long t2 = System.nanoTime();
        double t = (t2 - t1) / 1000000000.0;
        System.out.println(t + "," + total_score + "," + N + "," + t/N);
    }
}