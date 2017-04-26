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
        int Imgheight = 0; //will later add these from header
        int Imgwidth = 0;
        int ImgArray[][][] = new int[Imgwidth][Imgheight][3]; //3D array for one image to hold RGB
        byte[] finalImg; //byte array to transfer image to
        finalImg = new byte[Imgheight*Imgwidth];
        Trie trie = new Trie(); // Initialize trie
        trie.init_trie();
        Pair pair = new Pair(0,0);
        File file;
        file = new File("myfile.txt");
	BinaryIn fin;	
        int len = (int)file.length();
        fin = new BinaryIn ("myfile.txt");
        boolean input;
        boolean array[] = new boolean[len * 8]; //boolean array used for image data
        int index = 0;
       // int block[] = new int[64];
        while (index <len*8) //inputs image bits as boooleans
        {
            input = fin.readBoolean();
            
            array[index] = input;
            index++;
        }
        index = 0;
        int[][] fullBlock = new int[6][64]; //4R 1G 1B block
        int length = 1;
        int start = 0;
        int j;
        int k;
        int coeff;
        int val = 0,loop = 0;
        int idx = 1;
        boolean foundCoeff = false;
        int blocksAcross = Imgwidth/16;
        int blocksDown = Imgheight/16;
        int blockCol = 0;
        int blockRow = 0;
        while(index < len*8) //goes for full length of image
        {
            loop = 0;
            while(loop <6)//one full block
            {
                if (foundCoeff == false)
                {
                    coeff = 0;
                    k = 0;
                    for (j = index;j < index+8;j++)
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
                    foundCoeff = true;
                    fullBlock[loop][0] = coeff; //set DC
                }
                boolean word[] = new boolean[length]; //word is a set of bits
                k = 0;
                for(j = start; j <index;j++) //read in the bits of certain length
                {
                    word[k] = array[j];
                    k++;
                }
                if (trie.search(word,length,pair)) //checks to see if a match is found in the trie
                {
                    if (pair.level == 0 ) //special cases
                    {
                        if (pair.run == 0) //eof
                        {
                            break;
                        }
                        if (pair.run == 1) //eob
                        {
                            Dequantize(fullBlock[loop]);
                            IDCT(fullBlock[loop]); //Still need to add this////////
                            //fullBlock[loop] = block;
                        }
                        if (pair.run == 2) //esc
                        { //still have to account for signed, it is currently unsigned
                            k = 0;
                            int run,newval = 0,level;
                            for (j=0;j < index+6;j++)
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
                            for (j=0;j<newval;j++)
                            {
                                fullBlock[loop][zigzag[idx]] = 0;
                                idx++;
                            }  
                            newval = 0;
                            k = 0;
                            for (j=0;j < index+16;j++)
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
                            fullBlock[loop][zigzag[idx]] = newval;
                            idx++;
                        }
                    }
                    else //normal match, just do run and level
                    {
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
                        for (j = 0; j < pair.run; j++)
                        {
                            fullBlock[loop][zigzag[idx]] = 0;
                            idx++;
                        }
                        
                        fullBlock[loop][zigzag[idx]] = pair.level * sign;
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
                loop++;
            }
            //all 6 blocks found, start reconstruction
            //red blocks first, can make more efficient later
            int i = 0;
            for (j = 0;j<8;j++)
            {
                for (k = 0; k<8;k++)
                {
                    ImgArray[blockCol*8+k][blockRow*8+j][0] = fullBlock[0][i];
                    i++;
                }
            }
            i=0;
            for (j = 0;j<8;j++)
            {
                for (k = 0; k<8;k++)
                {
                    ImgArray[(1+blockCol)*8+k][blockRow*8+j][0] = fullBlock[1][i];
                    i++;
                }
            }
            i=0;
            for (j = 0;j<8;j++)
            {
                for (k = 0; k<8;k++)
                {
                    ImgArray[blockCol*8+k][(1+blockRow)*8+j][0] = fullBlock[2][i];
                    i++;
                }
            }
            i=0;
            for (j = 0;j<8;j++)
            {
                for (k = 0; k<8;k++)
                {
                    ImgArray[(1+blockCol)*8+k][(1+blockRow)*8+j][0] = fullBlock[3][i];
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
                    ImgArray[blockCol*8+2*k][blockRow*8+j2][1] = value;
                    ImgArray[blockCol*8+(2*k)+1][blockRow*8+j2][1] = value;
                    ImgArray[blockCol*8+2*k+1][blockRow*8+j2+1][1] = value;
                    ImgArray[blockCol*8+2*k+1][blockRow*8+j2+1][1] = value;
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
                    value = fullBlock[4][i];
                    ImgArray[blockCol*8+2*k][blockRow*8+j2][2] = value;
                    ImgArray[blockCol*8+(2*k)+1][blockRow*8+j2][2] = value;
                    ImgArray[blockCol*8+2*k+1][blockRow*8+j2+1][2] = value;
                    ImgArray[blockCol*8+2*k+1][blockRow*8+j2+1][2] = value;
                    i++;
                }
            }
            //all colors have now been put into respective spots
            if (blockCol == blocksAcross) //move across in destination array
            {
                blockCol = 0;
                blockRow++;
            }
            else
            {
                blockCol++; 
            }
        } //end of while
        k = 0;
        for (int i = 0;i<Imgheight;i++) // convert the 3D array to a 1D byte array in BGR format
        {
            for (j = 0;j <Imgwidth;j++)
            {
                finalImg[k] = (byte) ImgArray[j][i][2];
                finalImg[k+1] = (byte) ImgArray[j][i][1];
                finalImg[k+2] = (byte) ImgArray[j][i][0];
                k += 3;
            }
        } 
        //the following should display the image, not sure if this is correct yet
         BufferedImage bufferedImage=null;
        try{
            InputStream inputStream = new ByteArrayInputStream(finalImg);
            bufferedImage = ImageIO.read(inputStream);
        }
         catch (IOException ex) {
            System.out.println(ex.getMessage());
        }
        JFrame frame = new JFrame();
        frame.getContentPane().setLayout(new FlowLayout());
        frame.getContentPane().add(new JLabel(new ImageIcon(bufferedImage)));
        frame.pack();
        frame.setVisible(true);
    }
    public static void Dequantize(int array[])
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
    }
    public static void IDCT(int array[])
    {
        
    }
    
}
