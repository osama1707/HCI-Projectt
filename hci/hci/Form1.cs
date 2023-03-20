using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;
using System.Diagnostics;
using System.Threading;
namespace hci
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }
        public static string id, text;
        int n;
        string filePath = @"C:\Users\hp\Desktop\andrew.txt";
        private void button2_Click(object sender, EventArgs e)
        {
            id = textBox1.Text;
            bool isNumeric = int.TryParse(id, out n);
            if (isNumeric == true)
            {
                MessageBox.Show("fiducial ID " + id + " Note is Deleted");
                int lineToDelete;

                // Read all lines from the file into an array
                string[] lines = File.ReadAllLines(filePath);
                for (int i = 0; i < lines.Length; i++)
                {
                    for (int j = 0; j < id.Length; j++)
                    {
                        if (id[j] == lines[i][j])
                        {
                            if (id.Length - 1 == j)
                            {
                                lines = lines.Where((line, index) => index != i).ToArray();
                            }

                        }
                        else
                        {
                            break;
                        }
                    }
                }
                // Remove the desired line from the array


                // Write the modified array back to the file
                File.WriteAllLines(filePath, lines);
                textBox1.Clear();
                textBox2.Clear();

            }
            else
            {
                MessageBox.Show(" please check that fiducial ID is a number ");

            }
        }

        private void button3_Click(object sender, EventArgs e)
        {
            string[] lines = File.ReadAllLines(filePath);
            for (int i = 0; i < lines.Length; i++)
            {
                textBox2.Text += "fiducial ID ";
                for (int j = 0; j < lines[i].Length; j++)
                {
                    if (lines[i][j] == ',')
                    {
                        textBox2.Text += ' ';
                        textBox2.Text += ':';
                        textBox2.Text += ' ';
                        j++;
                    }
                    textBox2.Text += lines[i][j];
                }
                textBox2.Text += "\r\n";
            }
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void button4_Click(object sender, EventArgs e)
        {
            textBox1.Clear();
            textBox2.Clear();
        }

        private void button5_Click(object sender, EventArgs e)
        {
            

            // Set the path to the executable file of the other project

           
           string otherProjectExecutablePath = @"C:\Users\hp\Downloads\reacTIVision-1.5.1-win64\reacTIVision-1.5.1-win64\reacTIVision.exe";
            // Create a new process to start the other project
            Process otherProjectProcess = new Process();
            otherProjectProcess.StartInfo.FileName = otherProjectExecutablePath;

            // Start the other project
            otherProjectProcess.Start();
            Thread.Sleep(5000); // wait for 5 seconds (adjust as needed)

            // Get the other project's main form
            Form otherProjectMainForm = Application.OpenForms[0];

            // Set the size of the other project's main form
            otherProjectMainForm.Size = new System.Drawing.Size(800, 600);

            // Move the other project's main form to the desired location
            otherProjectMainForm.Location = new System.Drawing.Point(100, 100);
            otherProjectExecutablePath = @"C:\Users\hp\Downloads\TUIO11_NET-master\TUIO11_NET-master\bin\Debug\TuioDemo.exe";
            // Create a new process to start the other project
            Process otherProjectProcess2 = new Process();
            otherProjectProcess2.StartInfo.FileName = otherProjectExecutablePath;
          
            // Start the other project
            otherProjectProcess2.Start();

        }

        private void button1_Click(object sender, EventArgs e)
        {
            id = textBox1.Text;

            bool isNumeric = int.TryParse(id, out n);

            text = textBox2.Text;
            if (text == null)
            {
                MessageBox.Show(" please write a note ");
            }
            else
            {
                if (isNumeric == true)
                {
                  
                    int lineToDelete;

                    // Read all lines from the file into an array
                    string[] lines = File.ReadAllLines(filePath);
                    for (int i = 0; i < lines.Length; i++)
                    {
                        for (int j = 0; j < id.Length; j++)
                        {
                            if (lines[i][j] > 0)
                            {


                                if (id[j] == lines[i][j])
                                {
                                    if (id.Length - 1 == j)
                                    {
                                        lines = lines.Where((line, index) => index != i).ToArray();
                                        MessageBox.Show("old fiducial ID " + id + " Note is Deleted");
                                    }

                                }
                                else
                                {
                                    break;
                                }
                            }
                        }
                    }
                    // Remove the desired line from the array


                    // Write the modified array back to the file
                    File.WriteAllLines(filePath, lines);
                    textBox1.Clear();
                    textBox2.Clear();


                    if (isNumeric == true)
                    {
                        MessageBox.Show("fiducial ID " + id + ": " + text);


                        // Create a StreamWriter instance with the file path
                        using (StreamWriter writer = new StreamWriter(filePath, true))
                        {
                            string w = id + "," + text;
                            // Write a string to the file
                            writer.WriteLine(w);
                        }
                        textBox1.Clear();
                        textBox2.Clear();
                    }
                    else
                    {
                        MessageBox.Show(" please check that fiducial ID is a number ");

                    }
                }

            }
        }
    }
}
