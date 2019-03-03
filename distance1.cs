// Copyright (c) 2019 Alexander Lopatin. All rights reserved.
using System;
using System.Diagnostics;

namespace deletionDistanceCSharp {
    class MainClass {
        static int Fee(char c) { return c; }

        static string Remove(string s, int i) {
            string r = i > 0 ? s.Substring(0, i) : "";
            if (i < s.Length)
                r += s.Substring(i + 1);
            return r;
        }

        static int Distance1(string a, string b) {
            if (a == b)
                return 0;
            int d = int.MaxValue;
            for (int i = 0; i < a.Length; i++)
                d = Math.Min(d, Fee(a[i])+Distance1(Remove(a,i),b));
            for (int i = 0; i < b.Length; i++)
                d = Math.Min(d, Fee(b[i])+Distance1(a,Remove(b,i)));
            return d;
        }

        static void assert(bool ok) {
            if (!ok)
                Console.WriteLine("*************** ERROR ***************");
        }

        public static void Main(string[] args) {
            assert(Distance1("bat", "cat") == Fee('b') + Fee('c'));
            assert(Distance1("!~!", "~!!") == 2 * Fee('!'));
            Stopwatch stopWatch = new Stopwatch();
            stopWatch.Start();
            const int len = 5;
            int n = 0, d = 0;
            do
            {
                string s = n.ToString("D" + len.ToString());
                for (int i = 0; i <= len; i++)
                {
                    string a = s.Substring(0, i);
                    string b = s.Substring(i);
                    int da = Distance1(a, b);
                    int db = Distance1(a, b);
                    d += da;
                    assert(da == db);
                }
            } while (n++ < 99999);
            n *= 2 * (len + 1);
            stopWatch.Stop();
            Double t = stopWatch.Elapsed.TotalSeconds;
            Console.Write(t+"," +d+"," + n+"," + t/n);
            Console.WriteLine();
        }
    }
}
