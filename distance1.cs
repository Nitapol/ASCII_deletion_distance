// Copyright (c) 2019 Alexander Lopatin. All rights reserved.
using System;
using System.Collections.Generic;
using System.Diagnostics;

namespace deletionDistanceCSharp
{
    class MainClass
    {
        static int Penalty(char c) { return c; }

        static string Remove(string s, int i)
        {
            string r = i > 0 ? s.Substring(0, i) : "";
            if (i < s.Length)
                r += s.Substring(i + 1);
            return r;
        }

        static int Distance1(string a, string b)
        {
            if (a == b)
                return 0;
            int score = int.MaxValue;
            for (int i = 0; i < a.Length; i++)
                score = Math.Min(score, Penalty(a[i])+Distance1(Remove(a,i),b));
            for (int i = 0; i < b.Length; i++)
                score = Math.Min(score, Penalty(b[i])+Distance1(a,Remove(b,i)));
            return score;
        }

        static void assert(bool ok)
        {
            if (!ok)
                Console.WriteLine("*************** ERROR ***************");
        }

        public static void Main(string[] args)
        {
            assert(Distance1("at", "cat") == Penalty('c'));
            assert(Distance1("bat", "cat") == Penalty('b') + Penalty('c'));
            assert(Distance1("!~!", "~!!") == 2 * Penalty('!'));
            assert(Distance1("!!~", "!~!") == 2 * Penalty('!'));
            Stopwatch stopWatch = new Stopwatch();
            stopWatch.Start();
            int n = 0, N = 0, total_score = 0;
            while (n <= 99999) {
                string s = n.ToString("D5");
                for (int i = 0; i <= s.Length; i++) {
                    string a = s.Substring(0, i);
                    string b = s.Substring(i);
                    int score1 = Distance1(a, b);
                    int score2 = Distance1(a, b);
                    N += 2;
                    total_score += score1;
                    assert(score1 == score2);
                }
                n += 1;
            }
            stopWatch.Stop();
            //            TimeSpan ts = stopWatch.Elapsed;
            Double t = stopWatch.Elapsed.TotalSeconds;
            Console.Write(t+"," +total_score+"," + N+"," + t/N);
            Console.WriteLine();
        }
    }
}
