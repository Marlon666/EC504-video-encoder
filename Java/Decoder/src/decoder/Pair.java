/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package decoder;

/**
 *
 * @author awtry
 */
public class Pair 
{
    int run;
    int level;
    public Pair() {}
    public Pair(int i, int j)
    {
        run = i;
        level = j;
    }
    public void change(int i, int j)
    {
        run = i;
        level = j;
    }
}
