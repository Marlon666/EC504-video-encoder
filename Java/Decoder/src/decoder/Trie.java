/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
  */
package decoder;
import java.util.HashMap;
import java.util.Map;

/**
 *
 * @author awtry
 */
public class Trie 
{
    private TrieNode root;
 
    public Trie() {
        root = new TrieNode();
    }
    
    // Inserts a word into the trie.
    public void insert(boolean[] word, int len, Pair vals) {
        HashMap<Boolean, TrieNode> children = root.children;
        //System.out.println(len);
        for(int i=0; i<len; i++){
            boolean c = word[i];
            TrieNode t;
            if(children.containsKey(c)){
                    t = children.get(c);
            }else{
                t = new TrieNode(c);
                children.put(c, t);
            }
 
            children = t.children;
 
            //set leaf node
            if(i==len-1)
            {
                t.isLeaf = true;
                t.pair = vals;
            }
        }
    }
 
    // Returns if the word is in the trie.
    public boolean search(boolean[] word, int len, Pair pair) {
        TrieNode t = searchNode(word, len);
 
        if(t != null && t.isLeaf) 
        {
            
            pair.level = t.pair.level;
            pair.run = t.pair.run;
            return true;
        }
        else
            return false;
    }
 
    // Returns if there is any word in the trie
    // that starts with the given prefix.
   // public boolean startsWith(String prefix) {
      //  if(searchNode(prefix) == null) 
       //     return false;
       // else
        //    return true;
   // }
 
    public TrieNode searchNode(boolean[] str, int len){
        Map<Boolean, TrieNode> children = root.children; 
        TrieNode t = null;
        for(int i=0; i<len; i++){
            boolean c = str[i];
            if(children.containsKey(c)){
                t = children.get(c);
                children = t.children;
            }else{
                return null;
            }
        }

        return t;
    }
    public void init_trie()
    {
        boolean word01[] = {true,true};
        Pair pair01 = new Pair(0,1);
        this.insert(word01,2,pair01);
        Pair pair02 = new Pair(0,2);
        boolean word02[] = {false, true, false, false};
        this.insert(word02, 4, pair02);
        Pair pair03 = new Pair(0,3);
        boolean word03[] = {false,false,true,false,true};
        this.insert(word03, 5, pair03);
        Pair pair04 = new Pair(0,4);
        boolean word04[] = {false,false,false,false,true,true,false};
        this.insert(word04, 7, pair04);
        Pair pair05 = new Pair(0,5);
        boolean word05[] = {false,false,true,false,false,true,true,false};
        this.insert(word05, 8, pair05);
        Pair pair06 = new Pair(0,6);
        boolean word06[] = {false,false,true,false,false,false,false,true};
        this.insert(word06, 8, pair06);
        Pair pair07 = new Pair(0,7);
        boolean word07[] = {false,false,false,false,false,false,true,false,true,false};
        this.insert(word07, 10, pair07);
        Pair pair08 = new Pair(0,8);
        boolean word08[] = {false,false,false,false,false,false,false,true,true,true,false,true};
        this.insert(word08, 12, pair08);
        Pair pair09 = new Pair(0,9);
        boolean word09[] = {false,false,false,false,false,false,false,true,true,false,false,false};
        this.insert(word09, 12, pair09);
        Pair pair010 = new Pair(0,10);
        boolean word010[] = {false,false,false,false,false,false,false,true,false,false,true,true};
        this.insert(word010, 12, pair010);
        Pair pair011 = new Pair(0,11);
        boolean word011[] = {false,false,false,false,false,false,false,true,false,false,false,false};
        this.insert(word011, 12, pair011);
        Pair pair012 = new Pair(0,12);
        boolean word012[] = {false,false,false,false,false,false,false,false,true,true,false,true,false};
        this.insert(word012, 13, pair012);
        Pair pair013 = new Pair(0,13);
        boolean word013[] = {false,false,false,false,false,false,false,false,true,true,false,false,true};
        this.insert(word013,13,pair013);
        Pair pair014 = new Pair(0,14);
        boolean word014[] = {false,false,false,false,false,false,false,false,true,true,false,false,false};
        this.insert(word014,13,pair014);
        Pair pair015 = new Pair(0,15);
        boolean word015[] = {false,false,false,false,false,false,false,false,true,false,true,true,true};
        this.insert(word015, 13, pair015);
        Pair pair016 = new Pair(0,16);
        boolean word016[] = {false,false,false,false,false,false,false,false,false,true,true,true,true,true};
        this.insert(word016, 14, pair016);
        Pair pair017 = new Pair(0,17);
        boolean word017[] = {false,false,false,false,false,false,false,false,false,true,true,true,true,false};
        this.insert(word017, 14, pair017);
        Pair pair018 = new Pair(0,18);
        boolean word018[] = {false,false,false,false,false,false,false,false,false,true,true,true,false,true};
        this.insert(word018,14,pair018);
        Pair pair019 = new Pair(0,19);
        boolean word019[] = {false,false,false,false,false,false,false,false,false,true,true,true,false,false};
        this.insert(word019, 14, pair019);
        Pair pair020 = new Pair(0,20);
        boolean word020[] = {false,false,false,false,false,false,false,false,false,true,true,false,true,true};
        this.insert(word020, 14, pair020);
        Pair pair021 = new Pair(0,21);
        boolean word021[] = {false,false,false,false,false,false,false,false,false,true,true,false,true,false};
        this.insert(word021, 14, pair021);
        Pair pair022 = new Pair(0,22);
        boolean word022[] = {false,false,false,false,false,false,false,false,false,true,true,false,false,true};
        this.insert(word022,14,pair022);
        Pair pair023 = new Pair(0,23);
        boolean word023[] = {false,false,false,false,false,false,false,false,false,true,true,false,false,false};
        this.insert(word023, 14, pair023);
        Pair pair024 = new Pair(0,24);
        boolean word024[] = {false,false,false,false,false,false,false,false,false,true,false,true,true,true};
        this.insert(word024, 14, pair024);
        Pair pair025 = new Pair(0,25);
        boolean word025[] = {false,false,false,false,false,false,false,false,false,true,false,true,true,false};
        this.insert(word025, 14, pair025);
        Pair pair026 = new Pair(0,26);
        boolean word026[] = {false,false,false,false,false,false,false,false,false,true,false,true,false,true};
        this.insert(word026,14,pair026);
        Pair pair027 = new Pair(0,27);
        boolean word027[] = {false,false,false,false,false,false,false,false,false,true,false,true,false,false};
        this.insert(word027, 14, pair027);
        Pair pair028 = new Pair(0,28);
        boolean word028[] = {false,false,false,false,false,false,false,false,false,true,false,false,true,true};
        this.insert(word028, 14, pair028);
        Pair pair029 = new Pair(0,29);
        boolean word029[] = {false,false,false,false,false,false,false,false,false,true,false,false,true,false};
        this.insert(word029, 14, pair029);
        Pair pair030 = new Pair(0,30);
        boolean word030[] = {false,false,false,false,false,false,false,false,false,true,false,false,false,true};
        this.insert(word030, 14, pair030);
        Pair pair031 = new Pair(0,31);
        boolean word031[] = {false,false,false,false,false,false,false,false,false,true,false,false,false,false};
        this.insert(word031, 14, pair031);
        Pair pair032 = new Pair(0,32);
        boolean word032[] = {false,false,false,false,false,false,false,false,false,false,true,true,false,false,false};
        this.insert(word032, 15, pair032);
        Pair pair033 = new Pair(0,33);
        boolean word033[] = {false,false,false,false,false,false,false,false,false,false,true,false,true,true,true};
        this.insert(word033, 15, pair033);
        Pair pair034 = new Pair(0,34);
        boolean word034[] = {false,false,false,false,false,false,false,false,false,false,true,false,true,true,false};
        this.insert(word034, 15, pair034);
        Pair pair035 = new Pair(0,35);
        boolean word035[] = {false,false,false,false,false,false,false,false,false,false,true,false,true,false,true};
        this.insert(word035, 15, pair035);
        Pair pair036 = new Pair(0,36);
        boolean word036[] = {false,false,false,false,false,false,false,false,false,false,true,false,true,false,false};
        this.insert(word036, 15, pair036);
        Pair pair037 = new Pair(0,37);
        boolean word037[] = {false,false,false,false,false,false,false,false,false,false,true,false,false,true,true};
        this.insert(word037, 15, pair037);
        Pair pair038 = new Pair(0,38);
        boolean word038[] = {false,false,false,false,false,false,false,false,false,false,true,false,false,true,false};
        this.insert(word038, 15, pair038);
        Pair pair039 = new Pair(0,39);
        boolean word039[] = {false,false,false,false,false,false,false,false,false,false,true,false,false,false,true};
        this.insert(word039,15,pair039);
        Pair pair040 = new Pair(0,40);
        boolean word040[] = {false,false,false,false,false,false,false,false,false,false,true,false,false,false,false};
        this.insert(word040, 15, pair040);
        Pair pair11 = new Pair(1,1);
        boolean word11[] = {false,true,true};
        this.insert(word11, 3, pair11);
        Pair pair12 = new Pair(1,2);
        boolean word12[] = {false,false,false,true,true,false};
        this.insert(word12, 6, pair12);
        Pair pair13 = new Pair(1,3);
        boolean word13[] = {false,false,true,false,false,true,false,true};
        this.insert(word13, 8, pair13);
        Pair pair14 = new Pair(1,4);
        boolean word14[] = {false,false,false,false,false,false,true,true,false,false};
        this.insert(word14, 10, pair14);
        Pair pair15 = new Pair(1,5);
        boolean word15[] = {false,false,false,false,false,false,false,true,true,false,true,true};
        this.insert(word15, 12, pair15);
        Pair pair16 = new Pair(1,6);
        boolean word16[] = {false,false,false,false,false,false,false,false,true,false,true,true,false};
        this.insert(word16, 13, pair16);
        Pair pair17 = new Pair(1,7);
        boolean word17[] = {false,false,false,false,false,false,false,false,true,false,true,false,true};
        this.insert(word17, 13, pair17);
        Pair pair18 = new Pair(1,8);
        boolean word18[] = {false,false,false,false,false,false,false,false,false,false,true,true,true,true,true};
        this.insert(word18,15,pair18);
        Pair pair19 = new Pair(1,9);
        boolean word19[] = {false,false,false,false,false,false,false,false,false,false,true,true,true,true,false};
        this.insert(word19, 15, pair19);
        Pair pair110 = new Pair(1,10);
        boolean word110[] = {false,false,false,false,false,false,false,false,false,false,true,true,true,false,true};
        this.insert(word110, 15, pair110);
        Pair pair111 = new Pair(1,11);
        boolean word111[] = {false,false,false,false,false,false,false,false,false,false,true,true,true,false,false};
        this.insert(word111, 15, pair111);
        Pair pair112 = new Pair(1,12);
        boolean word112[] = {false,false,false,false,false,false,false,false,false,false,true,true,false,true,true};
        this.insert(word112, 15, pair112);
        Pair pair113 = new Pair(1,13);
        boolean word113[] = {false,false,false,false,false,false,false,false,false,false,true,true,false,true,false};
        this.insert(word113, 15, pair113);
        Pair pair114 = new Pair(1,14);
        boolean word114[] = {false,false,false,false,false,false,false,false,false,false,true,true,false,false,true};
        this.insert(word114, 15, pair114);
        Pair pair115 = new Pair(1,15);
        boolean word115[] = {false,false,false,false,false,false,false,false,false,false,false,true,false,false,true,true};
        this.insert(word115, 16, pair115);
        Pair pair116 = new Pair(1,16);
        boolean word116[] = {false,false,false,false,false,false,false,false,false,false,false,true,false,false,true,false};
        this.insert(word116, 16, pair116);
        Pair pair117 = new Pair(1,17);
        boolean word117[] = {false,false,false,false,false,false,false,false,false,false,false,true,false,false,false,true};
        this.insert(word117,16,pair117);
        Pair pair118 = new Pair (1,18);
        boolean word118[] = {false,false,false,false,false,false,false,false,false,false,false,true,false,false,false,false};
        this.insert(word118,16,pair118);
        Pair pair21 = new Pair(2,1);
        boolean word21[] = {false,true,false,true};
        this.insert(word21, 4, pair21);
        Pair pair22 = new Pair(2,2);
        boolean word22[] = {false,false,false,false,true,false,false};
        this.insert(word22, 7, pair22);
        Pair pair23 = new Pair(2,3);
        boolean word23[] = {false,false,false,false,false,false,true,false,true,true};
        this.insert(word23, 10, pair23);
        Pair pair24 = new Pair(2,4);
        boolean word24[] = {false,false,false,false,false,false,false,true,false,true,false,false};
        this.insert(word24,12,pair24);
        Pair pair25 = new Pair(2,5);
        boolean word25[] = {false,false,false,false,false,false,false,false,true,false,true,false,false};
        this.insert(word25, 13, pair25);
        Pair pair31 = new Pair(3,1);
        boolean word31[] = {false,false,true,true,true};
        this.insert(word31, 5, pair31);
        Pair pair32 = new Pair(3,2);
        boolean word32[] = {false,false,true,false,false,true,false,false};
        this.insert(word32, 8, pair32);
        Pair pair33 = new Pair(3,3);
        boolean word33[] = {false,false,false,false,false,false,false,true,true,true,false,false};
        this.insert(word33, 12, pair33);
        Pair pair34 = new Pair(3,4);
        boolean word34[] = {false,false,false,false,false,false,false,false,true,false,false,true,true};
        this.insert(word34, 13, pair34);
        Pair pair41 = new Pair(4,1);
        boolean word41[] = {false,false,true,true,false};
        this.insert(word41, 5, pair41);
        Pair pair42 = new Pair(4,2);
        boolean word42[] = {false,false,false,false,false,false,true,true,true,true};
        this.insert(word42, 10, pair42);
        Pair pair43 = new Pair(4,3);
        boolean word43[] = {false,false,false,false,false,false,false,true,false,false,true,false};
        this.insert(word43, 12, pair43);
        Pair pair51 = new Pair(5,1);
        boolean word51[] = {false,false,false,true,true,true};
        this.insert(word51, 6, pair51);
        Pair pair52 = new Pair(5,2);
        boolean word52[] = {false,false,false,false,false,false,true,false,false,true};
        this.insert(word52, 10, pair52);
        Pair pair53 = new Pair(5,3);
        boolean word53[] = {false,false,false,false,false,false,false,false,true,false,false,true,false};
        this.insert(word53, 13, pair53);
        Pair pair61 = new Pair(6,1);
        boolean word61[] = {false,false,false,true,false,true};
        this.insert(word61, 6, pair61);
        Pair pair62 = new Pair(6,2);
        boolean word62[] = {false,false,false,false,false,false,false,true,true,true,true,false};
        this.insert(word62, 12, pair62);
        Pair pair63 = new Pair(6,3);
        boolean word63[] = {false,false,false,false,false,false,false,false,false,false,false,true,false,true,false,false};
        this.insert(word63, 16, pair63);
        Pair pair71 = new Pair(7,1);
        boolean word71[] = {false,false,false,true,false,false};
        this.insert(word71, 6, pair71);
        Pair pair72 = new Pair(7,2);
        boolean word72[] = {false,false,false,false,false,false,false,true,false,true,false,true};
        this.insert(word72, 12, pair72);
        Pair pair81 = new Pair(8,1);
        boolean word81[] = {false,false,false,false,true,true,true};
        this.insert(word81, 7, pair81);
        Pair pair82 = new Pair(8,2);
        boolean word82[] = {false,false,false,false,false,false,false,true,false,false,false,true};
        this.insert(word82, 12, pair82);
        Pair pair91 = new Pair(9,1);
        boolean word91[] = {false,false,false,false,true,false,true};
        this.insert(word91, 7, pair91);
        Pair pair92 = new Pair(9,2);
        boolean word92[] = {false,false,false,false,false,false,false,false,true,false,false,false,true};
        this.insert(word92, 13, pair92);
        Pair pair101 = new Pair(10,1);
        boolean word101[] = {false,false,true,false,false,true,true,true};
        this.insert(word101,8,pair101);
        Pair pair102 = new Pair(10,2);
        boolean word102[] = {false,false,false,false,false,false,false,false,true,false,false,false,false};
        this.insert(word102, 13, pair102);
        Pair pair1101 = new Pair(11,1);
        boolean word1101[] = {false,false,true,false,false,false,true,true};
        this.insert(word1101,8,pair1101);
        Pair pair1102 = new Pair(11,2);
        boolean word1102[] = {false,false,false,false,false,false,false,false,false,false,false,true,true,false,true,false};
        this.insert(word1102, 16, pair1102);
        Pair pair121 = new Pair(12,1);
        boolean word121[] = {false,false,true,false,false,true,true,true};
        this.insert(word121, 8, pair121);
        Pair pair122 = new Pair(12,2);
        boolean word122[] = {false,false,false,false,false,false,false,false,false,false,false,true,true,false,false,true};
        this.insert(word122, 16, pair122);
        Pair pair131 = new Pair(13,1);
        boolean word131[] = {false,false,true,false,false,false,false,false};
        this.insert(word131, 8, pair131);
        Pair pair132 = new Pair(13,2);
        boolean word132[] = {false,false,false,false,false,false,false,false,false,false,false,true,true,false,false,false};
        this.insert(word132, 16, pair132);
        Pair pair141 = new Pair(14,1);
        boolean word141[] = {false,false,false,false,false,false,true,true,true,false};
        this.insert(word141,10,pair141);
        Pair pair142 = new Pair(14,2);
        boolean word142[] = {false,false,false,false,false,false,false,false,false,false,false,true,false,true,true,true};
        this.insert(word142, 16, pair142);
        Pair pair151 = new Pair(15,1);
        boolean word151[] = {false,false,false,false,false,false,true,true,false,true};
        this.insert(word151, 10, pair151);
        Pair pair152 = new Pair(15,2);
        boolean word152[] = {false,false,false,false,false,false,false,false,false,false,false,true,false,true,true,false};
        this.insert(word152, 16, pair152);
        Pair pair161 = new Pair(16,1);
        boolean word161[] = {false,false,false,false,false,false,true,false,false,false};
        this.insert(word161,10,pair161);
        Pair pair162 = new Pair(16,2);
        boolean word162[] = {false,false,false,false,false,false,false,false,false,false,false,true,false,true,false,true};
        this.insert(word162, 16, pair162);
        Pair pair171 = new Pair(17,1);
        boolean word171[] = {false,false,false,false,false,false,false,true,true,true,true,true};
        this.insert(word171, 12, pair171);
        Pair pair181 = new Pair(18,1);
        boolean word181[] = {false,false,false,false,false,false,false,true,true,false,true,false};
        this.insert(word181, 12, pair181);
        Pair pair191 = new Pair(19,1);
        boolean word191[] = {false,false,false,false,false,false,false,true,true,false,false,true};
        this.insert(word191, 12, pair191);
        Pair pair201 = new Pair(20,1);
        boolean word201[] = {false,false,false,false,false,false,false,true,false,true,true,true};
        this.insert(word201, 12, pair201);
        Pair pair211 = new Pair(21,1);
        boolean word211[] = {false,false,false,false,false,false,false,true,false,true,true,false};
        this.insert(word211, 12, pair211);
        Pair pair221 = new Pair(21,1);
        boolean word221[] = {false,false,false,false,false,false,false,false,true,true,true,true,true};
        this.insert(word221, 13, pair221);
        Pair pair231 = new Pair(23,1);
        boolean word231[] = {false,false,false,false,false,false,false,false,true,true,true,true,false};
        this.insert(word231,13,pair231);
        Pair pair241 = new Pair(24,1);
        boolean word241[] = {false,false,false,false,false,false,false,false,true,true,true,false,true};
        this.insert(word241, 13, pair241);
        Pair pair251 = new Pair(25,1);
        boolean word251[] = {false,false,false,false,false,false,false,false,true,true,true,false,false};
        this.insert(word251,13,pair251);
        Pair pair261 = new Pair(26,1);
        boolean word261[] = {false,false,false,false,false,false,false,false,true,true,false,true,true};
        this.insert(word261,13,pair261);
        Pair pair271 =new Pair(27,1);
        boolean word271[] = {false,false,false,false,false,false,false,false,false,false,false,true,true,true,true,true};
        this.insert(word271,16,pair271);
        Pair pair281 = new Pair(28,1);
        boolean word281[] = {false,false,false,false,false,false,false,false,false,false,false,true,true,true,true,false};
        this.insert(word281,16,pair281);
        Pair pair291 = new Pair(29,1);
        boolean word291[] = {false,false,false,false,false,false,false,false,false,false,false,true,true,true,false,true};
        this.insert(word291,16,pair291);
        Pair pair301 = new Pair(30,1);
        boolean word301[] = {false,false,false,false,false,false,false,false,false,false,false,true,true,true,false,false};
        this.insert(word301,16,pair301);
        Pair pair311 = new Pair(31,1);
        boolean word311[] = {false,false,false,false,false,false,false,false,false,false,false,true,true,false,true,true};
        this.insert(word311, 16, pair311);
        //special characters
        Pair pair10 = new Pair(1,0);//EOB
        boolean EOB[] = {true,false};
        this.insert(EOB,2,pair10);
        
        Pair pair391 = new Pair(0,0); //EOF
        boolean EOF[] = {false,false,false,false,false,false,false,false,
                         false,false,false,false,false,false,false,false,
                         false,false,false,false,false,false,false,false,
                         false,false,false,false,false,false,false,false,
                         false,false,false,false,false,false,false,true};
        this.insert(EOF, 40, pair391);
        
        Pair pairESC= new Pair(2,0); //ESC
        boolean ESC[] = {false,false,false,false,false,true};
        this.insert(ESC,6,pairESC);
    }
    
    
}
