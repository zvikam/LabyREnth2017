using System;

public class Example
{
    public static int Main(string[] args)
    {
        System.Resources.ResourceReader res = new System.Resources.ResourceReader(args[0]);
        string type = "";
        Byte[] value = null;
        res.GetResourceData(args[1], out type, out value);
        using (System.IO.Stream stdout = Console.OpenStandardOutput())
        {
            stdout.Write(value, 4, value.Length-4);
        }
        res.Close();
        return 0;
    }
}
