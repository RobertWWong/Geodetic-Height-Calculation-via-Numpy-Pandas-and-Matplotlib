using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;

namespace M7Gdop.FileParsers
{
    /// <summary>
    /// This class is designed to read a Moses7 Ascii Header Record. 
    /// </summary>
    public class Moses7AsciiHeaderRecord
    {
        //Line 1
        public char Sync; // Dollar Sign ($)
        public char FileForm; // File Form ('A' for Ascii or 'B' for binary)
        public char NumHeaderRecords; // Number of header records including this record (1-9)
        public char UnderLine; // (_)
        public char Blank; // left blank (space)
        public char[] DataType; // possible types: 'GEOD ', 'ECEF ', 'MGRP ' (5 chars)
        public char[] FileCreationDate; // in the form 20yymmdd ' (10 chars)
        public char[] FileCreationTime; // in the form 'hh:mm:ss ' (10 chars)
        public char[] Stitle; //from FILRUN namelist in moses7 run control (35 chars)
        public char Blank2; // left blank (space)
        public char[] FileType;// possible values: (14 Chars)
                               //'XSTATES/SIGMAS'
                               //'YSTATES/SIGMAS'
                               //'ZSTATES/SIGMAS'
                               //'MSMT RESIDUALS'
        //Line 2
        public char[] NumberOfDataDescriptors; // Number of data type descriptors following in this record (max 15) (4 chars)
        public List<DataTypeDescriptorRecord> DataTypeDescriptors;
        public char Blank3; // left blank (space)

        //Line 3
        public List<string> ExtraLines; //no clue how to deblock this info, but doesn't look needed

        /// <summary>
        /// Initializing the class sets the size of the known
        /// character arrays, and initializes the list object
        /// </summary>
        public Moses7AsciiHeaderRecord()
        {
            DataType = new char[5];
            FileCreationDate = new char[10];
            FileCreationTime = new char[10];
            Stitle = new char[35];
            FileType = new char[14];

            NumberOfDataDescriptors = new char[4];
            DataTypeDescriptors = new List<DataTypeDescriptorRecord>();
            ExtraLines = new List<string>();
        }

        /// <summary>
        /// This function will read through the entire header record given a valid 
        /// streamreader object. It will return true if the header record read is valid,
        /// and false if the record is not valid.
        /// </summary>
        /// <param name="reader"></param>
        /// <returns></returns>
        public bool ReadHeaderRecord(StreamReader reader)
        {
            bool val = false;
            if (reader != null)
            {
                
                string tempLine = "";
                if (reader.Peek() >= 0)
                {
                    tempLine = reader.ReadLine();
                    if (tempLine.Length >= 80)
                    {
                        Sync = tempLine[0];
                        FileForm = tempLine[1];
                        NumHeaderRecords = tempLine[2];
                        UnderLine = tempLine[3];
                        Blank = tempLine[4];

                        FileType = tempLine.ToCharArray(5, 5);
                        FileCreationDate = tempLine.ToCharArray(10, 10);
                        FileCreationTime = tempLine.ToCharArray(20, 10);
                        Stitle = tempLine.ToCharArray(30, 35);
                        Blank2 = tempLine[65];
                        FileType = tempLine.ToCharArray(66, 14);
                    }
                }

                if (Sync == '$' && FileForm == 'A')
                {
                    if (reader.Peek() >= 0)
                    {
                        tempLine = reader.ReadLine();
                        if (tempLine.Length > 4)
                        {
                            NumberOfDataDescriptors = tempLine.ToCharArray(0, 4);
                            int curByte = 4;
                            int num = Convert.ToInt32(new string(NumberOfDataDescriptors));

                            if (tempLine.Length >= curByte + 1 + num * 5)
                            {
                                if (num >= 1 && num <= 15)
                                {
                                    int i = 0;
                                    for (i = 0; i < num; i++)
                                    {
                                        DataTypeDescriptors.Add(
                                            new DataTypeDescriptorRecord(
                                                tempLine.ToCharArray(curByte, 3),
                                                tempLine.ToCharArray(curByte + 3, 2)
                                                )
                                            );

                                        curByte += 3 + 2;
                                    }
                                }

                                int recs = 2;
                                int numheadRecs = Convert.ToInt32(NumHeaderRecords.ToString());

                                for (recs = 2; recs < numheadRecs; recs++)
                                {
                                    if (reader.Peek() >= 0)
                                    {
                                        ExtraLines.Add(reader.ReadLine());
                                    }
                                }

                                val = true;
                            }
                        }
                    }

                   
                }
                
            }
            return val;
        }

        /// <summary>
        /// Class to store info about a data type descriptor record (essentially two char
        /// arrays, but this block can repeat and number of times wtihin the file)
        /// </summary>
        public class DataTypeDescriptorRecord
        {
            public char[] NumberOfValues; //from '1' to '999' (3 chars)
            public char[] TypeOfValues; // 'T8' Time real*8, 'R8' data real*8, 'R4' data real*4, 'I4' data integer*4 (2 chars)

            public DataTypeDescriptorRecord()
            {
                NumberOfValues = new char[3] { ' ', ' ', ' ' };
                TypeOfValues = new char[2] { ' ', ' ' };
            }

            public DataTypeDescriptorRecord(char[] _numVals, char[] _typeVals)
            {
                if (_numVals.Length == 3 && _typeVals.Length == 2)
                {
                    NumberOfValues = _numVals;
                    TypeOfValues = _typeVals;
                }
                else
                {
                    NumberOfValues = new char[3] { ' ', ' ', ' ' };
                    TypeOfValues = new char[2] { ' ', ' ' };
                }
            }

        }
    }
}
