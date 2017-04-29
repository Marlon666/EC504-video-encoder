/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package decoder;

import java.awt.FlowLayout;
import javax.swing.JPanel;
import javax.swing.SwingUtilities;
import java.awt.Graphics;
import java.awt.image.BufferedImage;

import java.io.IOException;

import java.io.ByteArrayInputStream;
import java.io.File;

import java.io.InputStream;

import javax.imageio.ImageIO;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;
/**
 *
 * @author awtry
 */
public class Decoder 
{

   
    public static void main(String[] args) 
    {
        //array of indices for zig zag
        int zigzag[] = {0,  1,  8, 16,  9,  2,  3, 10,
               17, 24, 32, 25, 18, 11, 4,  5,
               12, 19, 26, 33, 40, 48, 41, 34,
               27, 20, 13,  6,  7, 14, 21, 28,
               35, 42, 49, 56, 57, 50, 43, 36,
               29, 22, 15, 23, 30, 37, 44, 51,
               58, 59, 52, 45, 38, 31, 39, 46,
               53, 60, 61, 54, 47, 55, 62, 63};
        int Imgheight = 32; //will later add these from header
        int Imgwidth = 32;
        int totalMblocks = 4;
        int ImgArray[][][] = new int[Imgheight][Imgwidth][3]; //3D array for one image to hold RGB
        byte[] finalImg; //byte array to transfer image to
        finalImg = new byte[3*Imgheight*Imgwidth];
        
        Trie trie = new Trie(); // Initialize trie
        trie.init_trie();
        
        Pair pair = new Pair(0,0);
        File file;
        file = new File("mountain_32_32.bin");
        System.out.print(file.exists());
	BinaryIn fin;	
        int len = (int)file.length();
        System.out.print(file.length());
        fin = new BinaryIn ("mountain_32_32.bin");
        boolean input;
        boolean array[] = new boolean[len * 8]; //boolean array used for image data
        int index = 0;
        while (index <len*8) //inputs image bits as boooleans to array
        {
            input = fin.readBoolean();
            
            array[index] = input;
            index++;
        }
        index = 0; //current spot for end of word in the binary data to search trie
        int[][] fullBlock = new int[6][64]; //4R 1G 1B block
        int length = 1;
        int start = 0; //begining of word that we search for in trie
        int j;
        int k;
        int coeff;
        int val;
        int loop; //keeps track of how many blocks done in current macroblock
        int idx = 1;
        boolean foundCoeff = false;
        int blocksAcross = Imgwidth/8;
        int blocksDown = Imgheight/8;
        int blockCol = 0;
        int blockRow = 0;
        int blockCount = 0;
        while(blockCount < totalMblocks) //goes for full length of image
        {
            
            loop = 0;
            while(loop <6)//one full block
            {
                
               
                if (foundCoeff == false) //get teh leading coefficient
                {
                    System.out.println("Coeff");
                    coeff = 0;
                    k = 0;
                    for (j = index;j < index+8;j++) //it is 8 bits long
                    {
                        if (array[j] == false)
                        {
                            val = 0;
                        }
                        else
                        {
                            val = (int) Math.pow(2,k); //converting binary to int

                        }
                        k++;
                        coeff += val;
                    }
                    index +=8; //move index tonew spot
                    start = index;
                    foundCoeff = true;
                    fullBlock[loop][0] = coeff; //set DC
                }
                boolean word[] = new boolean[length]; //word is a set of bits
                k = 0;
                for(j = start; j <=index;j++) //read in the bits of certain length
                {
                    word[k] = array[j];
                    k++;
                }
                if (trie.search(word,length,pair)) //checks to see if a match is found in the trie
                {
                    length = 1;
                    
                    if (pair.level == 0 ) //special cases
                    {
                        
                        if (pair.run == 0) //eof
                        {
                            break;
                        }
                        else if (pair.run == 1) //eob
                        {
                            
                            idx = 0;
                            fullBlock[loop] = Dequantize(fullBlock[loop]);
                            fullBlock[loop] = IDCT(fullBlock[loop]); //Still need to add this////////
                            loop++;
                            foundCoeff = false;
                        
                        }
                        else if (pair.run == 2) //esc
                        { //still have to account for signed, it is currently unsigned
                            k = 0;
                            index++;
                            start = index;
                            int run,newval = 0,level;
                            for (j=start;j <= index+6;j++)
                            {
                                if (array[j] == false)
                                {
                                    run = 0;
                                }
                                else
                                {
                                    run = (int) Math.pow(2,k); //convert from binary to int
                                }
                                newval += run;
                                k++;
                            }
                            index += 6;
                            start = index;
                            for (j=0;j<newval;j++)
                            {
                                fullBlock[loop][zigzag[idx]] = 0;
                                idx++;
                            }  
                            newval = 0;
                            k = 0;
                            for (j=start;j <= index+16;j++)
                            {
                                if (array[j] == false)
                                {
                                    level = 0;
                                }
                                else
                                {
                                    level = (int) Math.pow(2,k);
                                }
                                newval += level;
                                k++;
                            }
                            index += 15;
                            fullBlock[loop][zigzag[idx]] = newval;
                            idx++;
                        }
                    }
                    else //normal match, just do run and level
                    {
                        
                        //System.out.format("run %d level %d idx %d%n", pair.run,pair.level,idx);
                        int sign;
                        index++;
                        if (array[index] == true)
                        {
                            sign = -1;
                        }
                        else
                        {
                            sign = 1;
                        }
                        //System.out.println("a");
                        for (j = 0; j < pair.run; j++)
                        {
                            fullBlock[loop][zigzag[idx]] = 0;
                            idx++;
                        }
                        System.out.format("loop %d idx %d blocks %d%n",loop,idx,blockCount);
                        fullBlock[loop][zigzag[idx]] = pair.level * sign;
                        //System.out.println(fullBlock[loop][zigzag[idx]]);
                        idx++;
                        
                    }
                    
                    index++;
                    start = index;
                }
                else //if no match, add one more bit and try again
                {
                    length++;
                    index++;
                }
            }
            //all 6 blocks found, start reconstruction
            //red blocks first, can make more efficient later
            int i = 0;
            for (j = 0;j<8;j++)
            {
                for (k = 0; k<8;k++)
                {
                    //System.out.print(fullBlock[0][i]);
                    //System.out.format("blockCol %d blockRow %d j%d i %d index %d%n",blockCol,blockRow,j,i,index);
                    ImgArray[blockRow*8+j][blockCol*8+k][0] = fullBlock[0][i];
                    i++;
                }
            }
            i=0;
            for (j = 0;j<8;j++)
            {
                for (k = 0; k<8;k++)
                {
                    //System.out.format("blockCol %d blockRow %d j%d i%d%n",blockCol,blockRow,j,i);
                    ImgArray[(blockRow)*8+j][(1+blockCol)*8+k][0] = fullBlock[1][i];
                    i++;
                }
            }
            i=0;
            for (j = 0;j<8;j++)
            {
                for (k = 0; k<8;k++)
                {
                    //System.out.format("blockCol %d blockRow %d j%d i%d%n",blockCol,blockRow,j,i);
                    ImgArray[(1+blockRow)*8+j][(blockCol)*8+k][0] = fullBlock[2][i];
                    i++;
                }
            }
            i=0;
            for (j = 0;j<8;j++)
            {
                for (k = 0; k<8;k++)
                {
                    ImgArray[(1+blockRow)*8+j][(1+blockCol)*8+k][0] = fullBlock[3][i];
                    i++;
                }
            }
            //green and blue next
            //green
            int value;
            i = 0;
            int j2;
            for (j = 0;j<8;j++)
            {
                j2 = 2*j;
                for (k = 0; k<8;k++)
                {
                    value = fullBlock[4][i];
                    ImgArray[blockRow*8+j2][blockCol*8+2*k][1] = value;
                    ImgArray[blockRow*8+j2][blockCol*8+2*k+1][1] = value;
                    ImgArray[blockRow*8+j2+1][blockCol*8+2*k][1] = value;
                    ImgArray[blockRow*8+j2+1][blockCol*8+2*k+1][1] = value;
                    i++;
                }
            }
            //blue
            i = 0;
            for (j = 0;j<8;j++)
            {
                j2 = 2*j;
                for (k = 0; k<8;k++)
                {
                    value = fullBlock[5][i];
                    ImgArray[blockRow*8+j2][blockCol*8+2*k][1] = value;
                    ImgArray[blockRow*8+j2][blockCol*8+2*k+1][1] = value;
                    ImgArray[blockRow*8+j2+1][blockCol*8+2*k][1] = value;
                    ImgArray[blockRow*8+j2+1][blockCol*8+2*k+1][1] = value;
                    i++;
                }
            }
            //all colors have now been put into respective spots
            if (blockCol == blocksAcross-2) //move across in destination array
            {
                blockCol = 0;
                blockRow +=2;
            }
            else
            {
                blockCol += 2; 
            }
            //checwhile++;
                                //System.out.println(checwhile);
            blockCount++;
        } //end of while
        k = 0;
        for (int i = 0;i<Imgheight;i++) // convert the 3D array to a 1D byte array in BGR format
        {
            for (j = 0;j <Imgwidth;j++)
            {
                //System.out.println(finalImg.length);
                //System.out.format("j is %d i is %d k is %d%n",j,i,k);
                
                finalImg[k] = (byte) ImgArray[j][i][2];
                finalImg[k+1] = (byte) ImgArray[j][i][1];
                finalImg[k+2] = (byte) ImgArray[j][i][0];
                k += 3;
                //System.out.print(ImgArray[j][i][0]);
            }
            //System.out.println();
        } 
        //the following should display the image, not sure if this is correct yet
        /* BufferedImage bufferedImage=null;
        try{
            InputStream inputStream = new ByteArrayInputStream(finalImg);
            bufferedImage = ImageIO.read(inputStream);
        }
         catch (IOException ex) {
            System.out.println(ex.getMessage());
        }
        JFrame frame = new JFrame();
        frame.getContentPane().setLayout(new FlowLayout());
        ImageIcon ii;
        ii = new ImageIcon(bufferedImage);
        frame.getContentPane().add(new JLabel(ii));
        frame.pack();
        frame.setVisible(true); */
    }
    public static int[] Dequantize(int array[])
    {
        int quant[] =
            { 8, 16, 19, 22, 26, 27, 29, 34,
             16, 16, 22, 24, 27, 29, 34, 37,
             19, 22, 26, 27, 29, 34, 34, 38,
             22, 22, 26, 27, 29, 34, 37, 40,
             22, 26, 27, 29, 32, 35, 40, 48,
             26, 27, 29, 32, 35, 40, 48, 58,
             26, 27, 29, 34, 38, 46, 56, 69,
             27, 29, 35, 38, 46, 56, 69, 83 };
        int i;
        for (i = 0;i < 64;i++)
        {
            array[i] = array[i] *quant[i];
        }
        return array;
    }
    
    public static int C(int u)
    {
        if (u == 0)
        {
            return (int) Math.pow(2, -.5);
        }
        else
        {
            return 1;
        }
    }
    public static int[] IDCT(int array[])
    {
        int sum;
        int[] newArray = new int[64];
        for (int i = 0;i <8;i++)
        {
            for (int j =0;j<8;j++)
            {
                sum = 0;
                for (int u = 0;u <8;u++)
                {
                    for(int v = 0;v<8;v++)
                    {
                        sum = (int)(sum + C(u)*C(v)/4*array[u*8+ v]*Math.cos((2*i + 1)*u*Math.PI/16)*Math.cos((2*j + 1)*v*Math.PI/16));
                    }
                }
                if (sum > 255)
                {
                    newArray[i*8+j] = 255;
                }
                else
                {
                    newArray[i*8+j] = sum;
                }
            }
        }
        return newArray;
        
    }
    
    
}
