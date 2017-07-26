using System;
using System.ComponentModel;
using System.Drawing;
using System.Security.Cryptography;
using System.Text;
using System.Windows.Forms;

namespace Doors
{
    public class Form1 : Form
    {
        private static void Main ()
        {
            Application.EnableVisualStyles ();
            Application.SetCompatibleTextRenderingDefault (false);
            Application.Run (new Form1 ());
        }
        //
        // Static Fields
        //
        public static int iNum;

        public static byte[] trollNum = new byte[] {
            50,
            5,
            56,
            4,
            73,
            31,
            58,
            50,
            16,
            52,
            36,
            59,
            57,
            19,
            10,
            62,
            19,
            86,
            39,
            74,
            63,
            78,
            41,
            11,
            8,
            22,
            51,
            11,
            47,
            75,
            68,
            7,
            15,
            12,
            69,
            28,
            69,
            47,
            73,
            86,
            63,
            37,
            18,
            9,
            12,
            37,
            9,
            75,
            60,
            69,
            12,
            4,
            22,
            19,
            14,
            76,
            56,
            52,
            18,
            75,
            16,
            73,
            14,
            14,
            25,
            69,
            54,
            25,
            36,
            74,
            55,
            8,
            37,
            56,
            42,
            41,
            28,
            37,
            39,
            25,
            55,
            53,
            57,
            24,
            40,
            10,
            64,
            64
        };

        public static byte[] trollMum = new byte[] {
            77,
            13,
            41,
            73,
            82,
            75,
            36,
            51,
            53,
            45,
            42,
            12,
            44,
            46,
            37,
            55,
            27,
            76,
            12,
            72,
            41,
            59,
            53,
            13,
            59,
            59,
            62,
            12,
            73,
            21,
            78,
            79,
            47,
            63,
            44,
            59,
            62,
            11,
            37,
            41,
            54,
            37,
            4,
            24,
            10,
            48,
            27,
            82,
            39,
            10,
            72,
            25,
            68,
            28,
            25,
            14,
            18,
            37,
            5,
            45,
            57,
            76,
            17,
            12,
            45,
            41,
            49,
            27,
            82,
            12,
            52,
            30,
            17,
            53,
            25,
            78,
            50,
            4,
            27,
            74,
            82,
            45,
            57,
            62,
            43,
            60,
            64,
            64
        };

        public static byte[] MagicNum = new byte[] {
            9,
            62,
            27,
            18,
            14,
            45,
            45,
            31,
            17,
            15,
            36,
            41,
            69,
            26,
            86,
            23,
            28,
            20,
            22,
            39,
            26,
            9,
            5,
            48,
            44,
            75,
            59,
            69,
            43,
            82,
            47,
            57,
            37,
            18,
            31,
            76,
            52,
            12,
            4,
            42,
            26,
            48,
            8,
            31,
            30,
            82,
            7,
            37,
            51,
            63,
            12,
            22,
            82,
            24,
            72,
            12,
            60,
            48,
            5,
            54,
            30,
            63,
            16,
            52,
            56,
            14,
            9,
            44,
            49,
            12,
            8,
            24,
            73,
            16,
            37,
            60,
            8,
            39,
            73,
            14,
            20,
            11,
            40,
            79,
            56,
            44,
            64,
            64
        };

        public static byte[] MagicMum = new byte[] {
            36,
            57,
            24,
            27,
            12,
            18,
            28,
            24,
            5,
            77,
            16,
            77,
            31,
            7,
            46,
            12,
            23,
            68,
            11,
            20,
            56,
            46,
            44,
            12,
            4,
            75,
            41,
            40,
            62,
            57,
            79,
            37,
            51,
            40,
            49,
            4,
            60,
            10,
            53,
            52,
            30,
            79,
            12,
            12,
            46,
            23,
            68,
            78,
            39,
            54,
            14,
            7,
            57,
            13,
            44,
            40,
            42,
            22,
            52,
            59,
            56,
            7,
            48,
            41,
            56,
            17,
            41,
            37,
            48,
            37,
            30,
            51,
            76,
            21,
            7,
            48,
            57,
            75,
            47,
            52,
            74,
            74,
            82,
            5,
            49,
            60,
            64,
            64
        };

        public static string szKeyValue = "4c61627972656e746843544632303137";

        public static string szmidkey = "F^>Y!\"t|fQlcM-z>o@E#^ {y\\Q%`pS{YdvcSTd~'Ftf(";

        public static string szlowkey = "RE,G pZ_QQt \u007f:S'^BMRXoe xs\"oO|Y#\u007f^\"SXTQ&'!P(";

        public static string szhighkey = "LvP\"L!@eo:]YPx-Avg~Sm_\u007fx>Fef|#`]fq@]T&L>Vcb(";

        //
        // Fields
        //
        private Button button8;

        private Button button7;

        private Button button12;

        private Button button0;

        private Button button11;

        private Button btnSubmit;

        private Button btnClear;

        private Button button9;

        private IContainer components;

        private Button button1;

        private TextBox txtInput;

        private Button button2;

        private Button button3;

        private Button button6;

        private Button button5;

        private Button button4;

        //
        // Constructors
        //
        public Form1 ()
        {
            this.InitializeComponent ();
            this.txtInput.Text = Form1.Decrypt(Form1.xorToString(Form1.szmidkey), Form1.szKeyValue);
            btnSubmit_Click(null, null);
            this.txtInput.Text = Form1.Decrypt(Form1.xorToString(Form1.szlowkey), Form1.szKeyValue);
            btnSubmit_Click(null, null);
            this.txtInput.Text = Form1.Decrypt(Form1.xorToString(Form1.szhighkey), Form1.szKeyValue);
            btnSubmit_Click(null, null);
        }

        //
        // Static Methods
        //
        public static string ByteToStr (byte[] buf)
        {
            return Encoding.UTF8.GetString (buf);
        }

        public static string ByteTostring (byte[] bt)
        {
            string text = "";
            for (int i = 0; i < bt.Length; i++) {
                text += Encoding.Default.GetString (bt, i, 1);
            }
            return text;
        }

        public static string Decrypt (string textToDecrypt, string key)
        {
            RijndaelManaged expr_05 = new RijndaelManaged ();
            expr_05.Mode = CipherMode.CBC;
            expr_05.Padding = PaddingMode.PKCS7;
            expr_05.KeySize = 256;
            expr_05.BlockSize = 256;
            byte[] array = Convert.FromBase64String (textToDecrypt);
            byte[] arg_43_0 = Encoding.UTF8.GetBytes (key);
            byte[] array2 = new byte[32];
            int length = arg_43_0.Length;
            Array.Copy (arg_43_0, array2, length);
            expr_05.Key = array2;
            expr_05.IV = array2;
            byte[] bytes = expr_05.CreateDecryptor ().TransformFinalBlock (array, 0, array.Length);
            return Encoding.UTF8.GetString (bytes);
        }

        public static string Encrypt (string textToEncrypt, string key)
        {
            RijndaelManaged expr_05 = new RijndaelManaged ();
            expr_05.Mode = CipherMode.CBC;
            expr_05.Padding = PaddingMode.PKCS7;
            expr_05.KeySize = 256;
            expr_05.BlockSize = 256;
            byte[] arg_3C_0 = Encoding.UTF8.GetBytes (key);
            byte[] array = new byte[32];
            int length = arg_3C_0.Length;
            Array.Copy (arg_3C_0, array, length);
            expr_05.Key = array;
            expr_05.IV = array;
            ICryptoTransform arg_6B_0 = expr_05.CreateEncryptor ();
            byte[] bytes = Encoding.UTF8.GetBytes (textToEncrypt);
            return Convert.ToBase64String (arg_6B_0.TransformFinalBlock (bytes, 0, bytes.Length));
        }

        public static byte[] stringTobyte (string str)
        {
            return Encoding.UTF8.GetBytes (str.ToCharArray ());
        }

        public static string StringToXOR (string data)
        {
            string arg_05_0 = string.Empty;
            byte[] array = new byte[data.Length];
            array = Form1.stringTobyte (data);
            for (int i = 0; i < array.Length; i++) {
                byte[] expr_24_cp_0 = array;
                int expr_24_cp_1 = i;
                expr_24_cp_0 [expr_24_cp_1] ^= 37;
                byte[] expr_32_cp_0 = array;
                int expr_32_cp_1 = i;
                expr_32_cp_0 [expr_32_cp_1] ^= 88;
            }
            return Form1.ByteTostring (array);
        }

        public static string xorToString (string data)
        {
            string arg_05_0 = string.Empty;
            byte[] array = new byte[data.Length];
            array = Form1.stringTobyte (data);
            for (int i = 0; i < array.Length; i++) {
                byte[] expr_24_cp_0 = array;
                int expr_24_cp_1 = i;
                expr_24_cp_0 [expr_24_cp_1] ^= 21;
            }
            return Form1.ByteTostring (array);
        }

        //
        // Methods
        //
        private void btnClear_Click (object sender, EventArgs e)
        {
            this.txtInput.Text = "";
        }

        private void btnSubmit_Click (object sender, EventArgs e)
        {
            if (!(this.txtInput.Text != "") || this.txtInput.TextLength != 16) {
                MessageBox.Show ("Either empty string or string length is wrong!");
                return;
            }
            if (Form1.xorToString (Form1.Encrypt (this.txtInput.Text, Form1.szKeyValue)) == Form1.szmidkey) {
                string str = Form1.Decrypt (Form1.StringToXOR (Form1.ByteToStr (Form1.trollMum)), Form1.szKeyValue);
                MessageBox.Show ("Do you know  " + str);
                return;
            }
            if (Form1.xorToString (Form1.Encrypt (this.txtInput.Text, Form1.szKeyValue)) == Form1.szlowkey) {
                string str2 = Form1.Decrypt (Form1.StringToXOR (Form1.ByteToStr (Form1.MagicNum)), Form1.szKeyValue);
                MessageBox.Show ("Do you know  " + str2);
                return;
            }
            if (Form1.xorToString (Form1.Encrypt (this.txtInput.Text, Form1.szKeyValue)) == Form1.szhighkey) {
                string str3 = Form1.Decrypt (Form1.StringToXOR (Form1.ByteToStr (Form1.MagicMum)), Form1.szKeyValue);
                MessageBox.Show ("Do you know  " + str3);
                return;
            }
            string str4 = Form1.Decrypt (Form1.StringToXOR (Form1.ByteToStr (Form1.trollNum)), Form1.szKeyValue);
            MessageBox.Show ("Do you know  " + str4);
        }

        private void button0_Click (object sender, EventArgs e)
        {
            Form1.iNum = 0;
            this.TextInput (Form1.iNum);
        }

        private void button1_Click (object sender, EventArgs e)
        {
            Form1.iNum = 1;
            this.TextInput (Form1.iNum);
        }

        private void button2_Click (object sender, EventArgs e)
        {
            Form1.iNum = 2;
            this.TextInput (Form1.iNum);
        }

        private void button3_Click (object sender, EventArgs e)
        {
            Form1.iNum = 3;
            this.TextInput (Form1.iNum);
        }

        private void button4_Click (object sender, EventArgs e)
        {
            Form1.iNum = 4;
            this.TextInput (Form1.iNum);
        }

        private void button5_Click (object sender, EventArgs e)
        {
            Form1.iNum = 5;
            this.TextInput (Form1.iNum);
        }

        private void button6_Click (object sender, EventArgs e)
        {
            Form1.iNum = 6;
            this.TextInput (Form1.iNum);
        }

        private void button7_Click (object sender, EventArgs e)
        {
            Form1.iNum = 7;
            this.TextInput (Form1.iNum);
        }

        private void button8_Click (object sender, EventArgs e)
        {
            Form1.iNum = 8;
            this.TextInput (Form1.iNum);
        }

        private void button9_Click (object sender, EventArgs e)
        {
            Form1.iNum = 9;
            this.TextInput (Form1.iNum);
        }

        protected override void Dispose (bool disposing)
        {
            if (disposing && this.components != null) {
                this.components.Dispose ();
            }
            base.Dispose (disposing);
        }

        private void InitializeComponent ()
        {
            this.button1 = new Button ();
            this.txtInput = new TextBox ();
            this.button2 = new Button ();
            this.button3 = new Button ();
            this.button6 = new Button ();
            this.button5 = new Button ();
            this.button4 = new Button ();
            this.button9 = new Button ();
            this.button8 = new Button ();
            this.button7 = new Button ();
            this.button12 = new Button ();
            this.button0 = new Button ();
            this.button11 = new Button ();
            this.btnSubmit = new Button ();
            this.btnClear = new Button ();
            base.SuspendLayout ();
            this.button1.Location = new Point (13, 48);
            this.button1.Name = "button1";
            this.button1.Size = new Size (50, 50);
            this.button1.TabIndex = 0;
            this.button1.Text = "1";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new EventHandler (this.button1_Click);
            this.txtInput.Location = new Point (13, 13);
            this.txtInput.MaxLength = 32;
            this.txtInput.Name = "txtInput";
            this.txtInput.ReadOnly = true;
            this.txtInput.Size = new Size (190, 20);
            this.txtInput.TabIndex = 1;
            this.button2.Location = new Point (83, 48);
            this.button2.Name = "button2";
            this.button2.Size = new Size (50, 50);
            this.button2.TabIndex = 2;
            this.button2.Text = "2";
            this.button2.UseVisualStyleBackColor = true;
            this.button2.Click += new EventHandler (this.button2_Click);
            this.button3.Location = new Point (153, 48);
            this.button3.Name = "button3";
            this.button3.Size = new Size (50, 50);
            this.button3.TabIndex = 3;
            this.button3.Text = "3";
            this.button3.UseVisualStyleBackColor = true;
            this.button3.Click += new EventHandler (this.button3_Click);
            this.button6.Location = new Point (153, 118);
            this.button6.Name = "button6";
            this.button6.Size = new Size (50, 50);
            this.button6.TabIndex = 6;
            this.button6.Text = "6";
            this.button6.UseVisualStyleBackColor = true;
            this.button6.Click += new EventHandler (this.button6_Click);
            this.button5.Location = new Point (83, 118);
            this.button5.Name = "button5";
            this.button5.Size = new Size (50, 50);
            this.button5.TabIndex = 5;
            this.button5.Text = "5";
            this.button5.UseVisualStyleBackColor = true;
            this.button5.Click += new EventHandler (this.button5_Click);
            this.button4.Location = new Point (13, 118);
            this.button4.Name = "button4";
            this.button4.Size = new Size (50, 50);
            this.button4.TabIndex = 4;
            this.button4.Text = "4";
            this.button4.UseVisualStyleBackColor = true;
            this.button4.Click += new EventHandler (this.button4_Click);
            this.button9.Location = new Point (153, 188);
            this.button9.Name = "button9";
            this.button9.Size = new Size (50, 50);
            this.button9.TabIndex = 9;
            this.button9.Text = "9";
            this.button9.UseVisualStyleBackColor = true;
            this.button9.Click += new EventHandler (this.button9_Click);
            this.button8.Location = new Point (83, 188);
            this.button8.Name = "button8";
            this.button8.Size = new Size (50, 50);
            this.button8.TabIndex = 8;
            this.button8.Text = "8";
            this.button8.UseVisualStyleBackColor = true;
            this.button8.Click += new EventHandler (this.button8_Click);
            this.button7.Location = new Point (13, 188);
            this.button7.Name = "button7";
            this.button7.Size = new Size (50, 50);
            this.button7.TabIndex = 7;
            this.button7.Text = "7";
            this.button7.UseVisualStyleBackColor = true;
            this.button7.Click += new EventHandler (this.button7_Click);
            this.button12.Location = new Point (153, 258);
            this.button12.Name = "button12";
            this.button12.Size = new Size (50, 50);
            this.button12.TabIndex = 12;
            this.button12.Text = "#";
            this.button12.UseVisualStyleBackColor = true;
            this.button0.Location = new Point (83, 258);
            this.button0.Name = "button0";
            this.button0.Size = new Size (50, 50);
            this.button0.TabIndex = 11;
            this.button0.Text = "0";
            this.button0.UseVisualStyleBackColor = true;
            this.button0.Click += new EventHandler (this.button0_Click);
            this.button11.Location = new Point (13, 258);
            this.button11.Name = "button11";
            this.button11.Size = new Size (50, 50);
            this.button11.TabIndex = 10;
            this.button11.Text = "*";
            this.button11.UseVisualStyleBackColor = true;
            this.btnSubmit.Location = new Point (128, 326);
            this.btnSubmit.Name = "btnSubmit";
            this.btnSubmit.Size = new Size (75, 23);
            this.btnSubmit.TabIndex = 13;
            this.btnSubmit.Text = "Validate";
            this.btnSubmit.UseVisualStyleBackColor = true;
            this.btnSubmit.Click += new EventHandler (this.btnSubmit_Click);
            this.btnClear.Location = new Point (13, 326);
            this.btnClear.Name = "btnClear";
            this.btnClear.Size = new Size (75, 23);
            this.btnClear.TabIndex = 14;
            this.btnClear.Text = "Clear";
            this.btnClear.UseVisualStyleBackColor = true;
            this.btnClear.Click += new EventHandler (this.btnClear_Click);
            base.AutoScaleDimensions = new SizeF (6f, 13f);
            base.AutoScaleMode = AutoScaleMode.Font;
            base.ClientSize = new Size (220, 361);
            base.Controls.Add (this.btnClear);
            base.Controls.Add (this.btnSubmit);
            base.Controls.Add (this.button12);
            base.Controls.Add (this.button0);
            base.Controls.Add (this.button11);
            base.Controls.Add (this.button9);
            base.Controls.Add (this.button8);
            base.Controls.Add (this.button7);
            base.Controls.Add (this.button6);
            base.Controls.Add (this.button5);
            base.Controls.Add (this.button4);
            base.Controls.Add (this.button3);
            base.Controls.Add (this.button2);
            base.Controls.Add (this.txtInput);
            base.Controls.Add (this.button1);
            base.Name = "Form1";
            base.StartPosition = FormStartPosition.CenterScreen;
            this.Text = "Doors";
            base.ResumeLayout (false);
            base.PerformLayout ();
        }

        public bool TextInput (int txt)
        {
            bool result;
            if (this.txtInput.MaxLength > this.txtInput.TextLength) {
                TextBox expr_1E = this.txtInput;
                expr_1E.Text += txt;
                result = true;
            }
            else {
                MessageBox.Show ("length error!!");
                result = false;
            }
            return result;
        }
    }
}

