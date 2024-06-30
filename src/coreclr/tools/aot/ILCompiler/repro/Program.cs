// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System;
using System.Runtime.CompilerServices;

class Program
{
    [ThreadStatic]
    static int x = 5;

    static void Main()
    {
        Test();
    }

    [MethodImpl(MethodImplOptions.NoInlining)]
    static void Test()
    {
        Console.WriteLine(x);
    }
}
