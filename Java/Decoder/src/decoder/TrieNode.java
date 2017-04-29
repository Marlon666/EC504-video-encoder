/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package decoder;
import java.util.HashMap;
/**
 *
 * @author awtry
 */
public class TrieNode
{
    boolean c;
    Pair pair;
    HashMap<Boolean, TrieNode> children = new HashMap<Boolean, TrieNode>();
    boolean isLeaf;
    
    public TrieNode() {}
 
    public TrieNode(boolean c){
        this.c = c;
    }
}
