using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;

namespace M7Gdop.FileParsers
{
    /// <summary>
    /// Class to read a Gmes Version 4 binary file. Each file contains a single Moses 7 Header Record, followed by
    /// any number of Data Blocks. Each Data Block begins with a leader record, followed by any number of Data Records
    /// (leader record determins number of data records in data block).
    /// </summary>
    public class GmesV4Class
    {

        private FileStream gmesFileStream; //File stream that is pointing at gmes file
        
        public Moses7HeaderRecord M7HeaderRecord; //Each gmes file has 1 m7 header record
        public GmesV4LeaderRecordClass LeaderRecord; //Each data block has 1 leader record (this will be reset for each data block)
        public List<GmesV4DataRecordClass> DataRecords; //Each datablock has a variable number of data records (number is defined in leader record)

        //delegate and event to handle percentage change (listeners will recieve update on percentage)
        public delegate void PercentageChange(PercentScannedEventArgs args);
        public event PercentageChange GmesPercentChanged = null;

        public double StartTime;
        public double StopTime;

        private double? updatePercentTime;

        /// <summary>
        /// Initialize method for GmesV4Class, initializes all needed variables
        /// </summary>
        public GmesV4Class()
        {
            gmesFileStream = null;
            M7HeaderRecord = new Moses7HeaderRecord();
            LeaderRecord = new GmesV4LeaderRecordClass();
            DataRecords = new List<GmesV4DataRecordClass>();
            StartTime = CustomNull.Double;
            StopTime = CustomNull.Double;

            updatePercentTime = null;
        }

        /// <summary>
        /// This method clears all of the values contained within the DataRecords List
        /// </summary>
        /// <returns></returns>
        public bool ClearDataRecords()
        {
            bool val = false;
            DataRecords.Clear();
            val = true;
            return val;
        }

        /// <summary>
        /// This method initializes the filestream object for the gmes file and
        /// reads past the header records. Returns true if everything read ok, 
        /// false if there are problems
        /// </summary>
        /// <param name="inputPath">String file path to gmes file</param>
        /// <returns></returns>
        public bool InitializeFile(string inputPath)
        {
            bool val = false;
            if (File.Exists(inputPath))
            {
                gmesFileStream = new FileStream(inputPath, FileMode.Open, FileAccess.Read);
                if (gmesFileStream.CanRead)
                {
                    if (M7HeaderRecord.ReadM7HeaderRecord(gmesFileStream)) //if we can read the M7 Header Record
                    {
                        if (M7HeaderRecord.IsThisValidRecord())
                        {
                            string tempString = new string(M7HeaderRecord.inputDataFileType);
                            if (tempString.ToUpper() == "GMES")
                            {
                                val = true;

                                //determine percentage scanned and call event (if not null)
                                if (GmesPercentChanged != null)
                                {
                                    PercentScannedEventArgs args = new PercentScannedEventArgs((Convert.ToDouble(gmesFileStream.Position) / Convert.ToDouble(gmesFileStream.Length)) * 100.0);
                                    GmesPercentChanged(args);
                                }
                            }
                        }
                    }
                }
            }
            return val;
        }

        /// <summary>
        /// This method will close the gmes file stream object
        /// </summary>
        /// <returns></returns>
        public bool CloseInputFileStream()
        {
            bool val = false;
            gmesFileStream.Close();
            val = true;

            //determine percentage scanned and call event (if not null)
            if (GmesPercentChanged != null)
            {
                PercentScannedEventArgs args = new PercentScannedEventArgs(100.0);
                GmesPercentChanged(args);
            }

            return val;

            
        }

        /// <summary>
        /// This method will read the next data block (i.e. leader record and all subsequent data records
        /// for this data block)
        /// </summary>
        /// <returns>Returns true if record read, false if end of file reached</returns>
        public bool ReadNextFrame()
        {
            bool val = false;

            if (gmesFileStream.CanRead)
            {
                if (gmesFileStream.Position < gmesFileStream.Length)
                {
                    if (LeaderRecord.ReadGmesV4LeaderRecord(gmesFileStream)) //was the leader record successfully read for this data block?
                    {
                        //clear all current data records in list (we're reading a new set)
                        DataRecords.Clear();

                        //set the start time if it hasn't been set yet
                        if (StartTime == CustomNull.Double)
                        {
                            StartTime = LeaderRecord.Tgmes;
                        }

                        //set the stop time as every record, that way at the end we get last record time
                        StopTime = LeaderRecord.Tgmes;

                        int i = 0;
                        for (i = 0; i < LeaderRecord.Nsat; i++)
                        {
                            //add new item to data records (initializing datarecordclass with filestream and leader record will read and set all vaules)
                            DataRecords.Add(new GmesV4DataRecordClass(gmesFileStream, LeaderRecord));

                        }

                        //this should always be true as long as leaderRecord.Nsat is greater than 0
                        if (DataRecords.Count > 0)
                        {
                            val = true;
                        }

                        

                        if (updatePercentTime == null)
                        {
                            if (GmesPercentChanged != null)
                            {
                                PercentScannedEventArgs args = new PercentScannedEventArgs((Convert.ToDouble(gmesFileStream.Position) / Convert.ToDouble(gmesFileStream.Length)) * 100.0);
                                GmesPercentChanged(args);
                            }

                            updatePercentTime = LeaderRecord.Tgmes;
                        }
                        else
                        {
                            if (LeaderRecord.Tgmes - updatePercentTime >= 10.0)
                            {
                                if (GmesPercentChanged != null)
                                {
                                    PercentScannedEventArgs args = new PercentScannedEventArgs((Convert.ToDouble(gmesFileStream.Position) / Convert.ToDouble(gmesFileStream.Length)) * 100.0);
                                    GmesPercentChanged(args);
                                }

                                updatePercentTime = LeaderRecord.Tgmes;
                            }
                        }
                    }
                }
                else
                {
                    val = false;
                }
            }
            return val;
        }
    }


    /// <summary>
    /// This class contains all attributes and methods specific to the gmesV4 leader record. 
    /// </summary>
    public class GmesV4LeaderRecordClass
    {
        public char[] Sync; //sync word identifying start of data frame. Sync = $$$A for ascii file, $$$B for binary file
        public double Tgmes; // Gps time (seconds of week)
        public double Dtclk; //Receiver clock offset (seconds)
        public int Nsat; //Number of satellite data records in frame
        public int Nmes; //Number of measurements per data record
        public int[] Imes; //IDs of measurements m=1..mxim (mxim = 8)
        public int Uiode; //Usable IODE indicator 1=usable 0=unusable

        private int sizeOfRecord;

        /// <summary>
        /// Primary Class Initializer Method (just calls to re-init all variables)
        /// </summary>
        public GmesV4LeaderRecordClass()
        {
            InitializeVariables();
        }

        /// <summary>
        /// Overloaded Class Initializer Method, initializes class, re-inits all variables
        /// and then reads the file stream provided to set variables
        /// </summary>
        /// <param name="_inputFileStream"></param>
        public GmesV4LeaderRecordClass(FileStream _inputFileStream)
        {
            InitializeVariables();
            ReadGmesV4LeaderRecord(_inputFileStream);
        }

        /// <summary>
        /// This method sets all the class variables to their default values
        /// </summary>
        private void InitializeVariables()
        {
            Sync = new char[4] { CustomNull.Char, CustomNull.Char, CustomNull.Char, CustomNull.Char };
            Tgmes = CustomNull.Double;
            Dtclk = CustomNull.Double;
            Nsat = CustomNull.Int;
            Nmes = CustomNull.Int;
            Imes = new int[8] { CustomNull.Int, CustomNull.Int, CustomNull.Int, CustomNull.Int, CustomNull.Int, CustomNull.Int, CustomNull.Int, CustomNull.Int };
            Uiode = CustomNull.Int;

            sizeOfRecord = 33; 
        }


        /// <summary>
        /// This method will parse a file stream into the associated member variables. It will return
        /// true if successful, and false if not (false means end of file)
        /// </summary>
        /// <param name="_inputFileStream"></param>
        /// <returns></returns>
        public bool ReadGmesV4LeaderRecord(FileStream _inputFileStream)
        {
            bool val = false;
            if (_inputFileStream != null) {
                if (_inputFileStream.CanRead)
                {
                    if (_inputFileStream.Position + sizeOfRecord < _inputFileStream.Length)
                    {
                        long startByte = _inputFileStream.Position;

                        byte[] buffer = new byte[sizeOfRecord];
                        _inputFileStream.Read(buffer, 0, sizeOfRecord);

                        MemoryStream memStream = new MemoryStream(buffer);

                        BinaryReader reader = new BinaryReader(memStream);

                        int i = 0;
                        for (i = 0; i < Sync.Length; i++)
                        {
                            Sync[i] = Convert.ToChar(reader.ReadByte());
                        }

                        Tgmes = reader.ReadDouble();
                        Dtclk = reader.ReadDouble();
                        Nsat = Convert.ToInt32(reader.ReadInt16());
                        Nmes = Convert.ToInt32(reader.ReadInt16());

                        for (i = 0; i < Imes.Length; i++)
                        {
                            Imes[i] = Convert.ToInt32(reader.ReadByte());
                        }

                        Uiode = Convert.ToInt32(reader.ReadByte());

                        val = true;

                        //check for sync if sync is bad assume message block is bad (no checksums to verify)
                        //i'm hoping that this only happens near the end of the file with an incomplete message
                        //block. Included extra check that throws an exception to alert if there's something 
                        //fishy going on.
                        if (new string(Sync) != "$$$B")
                        {
                            //extra check
                            if (_inputFileStream.Length - _inputFileStream.Position > 100) 
                            {
                                throw new Exception("Error in GmesV4 Leader record, sync not correct but more data at end of file...");
                            }

                            _inputFileStream.Seek(startByte + 1, SeekOrigin.Begin);
                            val = false;
                        }
                    }
                }
            }
            return val;
        }
    }

    /// <summary>
    /// This class contains the Iwrn messages in the leader record. Its purpose
    /// is to provide an easy to understand way of looking at the bit fields.
    /// </summary>
    public class GmesV4IwrnClass
    {
        //enumerator to define flag status
        public enum IwrnGoodBad
        {
            Good,
            Bad
        }

        //array to hold flags
        public IwrnGoodBad[] WarnArray;

        /// <summary>
        /// Class constructor method, just initializes class variables
        /// </summary>
        public GmesV4IwrnClass()
        {
            WarnArray = new IwrnGoodBad[8]; //initialize array
            int i = 0;
            for (i = 0; i < WarnArray.Length; i++) WarnArray[i] = IwrnGoodBad.Good; //set all values to good at first

        }

        //per the Suite_RevD.pdf Table A-36 0 = good, 1 = bad
        // bit 1 = measurement 1, bit 8 = measurement 8
        public void SetFlags(byte inputByte)
        {

            if ((inputByte & 0x80) == 0x80)
            {
                WarnArray[7] = IwrnGoodBad.Bad;
            }
            if ((inputByte & 0x40) == 0x40)
            {
                WarnArray[6] = IwrnGoodBad.Bad;
            }
            if ((inputByte & 0x20) == 0x20)
            {
                WarnArray[5] = IwrnGoodBad.Bad;
            }
            if ((inputByte & 0x10) == 0x10)
            {
                WarnArray[4] = IwrnGoodBad.Bad;
            }
            if ((inputByte & 0x08) == 0x08)
            {
                WarnArray[3] = IwrnGoodBad.Bad;
            }
            if ((inputByte & 0x04) == 0x04)
            {
                WarnArray[2] = IwrnGoodBad.Bad;
            }
            if ((inputByte & 0x02) == 0x02)
            {
                WarnArray[1] = IwrnGoodBad.Bad;
            }
            if ((inputByte & 0x01) == 0x01)
            {
                WarnArray[0] = IwrnGoodBad.Bad;
            }
        }
    }

    /// <summary>
    /// This Class contains all the variables and methods for a specific data record. It has two
    /// inititialization methods. Given a filestream it parses it and sets its values.
    /// </summary>
    public class GmesV4DataRecordClass
    {
        public int Isat; //Satellite vehicle ID
        public GmesV4IwrnClass Iwrn; //Warning flags for satellite measurements
        public int Icn01; // Carrier-to-noise ratio for sat L1 meas
        public int Icn02; // Carrier-to-noise ratio for sat L2 meas
        public int Lokc1; //Cumulative lock-count for sat L1 carrier tracking
        public int Lokc2; //Cumulative lock-count for sat L2 carrier tracking
        public List<double> Msmt; //Measurement data values
        public int Iode; //Issue of data ephemeris for sat (usable if Uiode = 1)

        private int sizeMinusMeasurements; 
        private int sizeOfSingleMeasurement;

        /// <summary>
        /// This method sets all member variables to default values
        /// </summary>
        private void InitializeVariables()
        {
            Isat = CustomNull.Int;
            Iwrn = new GmesV4IwrnClass();
            Icn01 = CustomNull.Int;
            Icn02 = CustomNull.Int;
            Lokc1 = CustomNull.Int;
            Lokc2 = CustomNull.Int;
            Msmt = new List<double>();
            Iode = CustomNull.Int;

            sizeMinusMeasurements = 14;
            sizeOfSingleMeasurement = 8;
        }

        /// <summary>
        /// Class constructor, calls function to set variables
        /// </summary>
        public GmesV4DataRecordClass()
        {
            InitializeVariables();
        }

        /// <summary>
        /// Overloaded Class constructor, calls function to set variable defaults, then reads file stream
        /// and sets the correct values
        /// </summary>
        /// <param name="_inputStream"></param>
        /// <param name="_leaderRecord"></param>
        public GmesV4DataRecordClass(FileStream _inputStream, GmesV4LeaderRecordClass _leaderRecord)
        {
            InitializeVariables();
            ReadDataRecord(_inputStream, _leaderRecord);
        }

        /// <summary>
        /// This function reads the file stream and sets the class variables. It uses the leader
        /// record to determine the number of measurements for this data record to read.
        /// </summary>
        /// <param name="_inputStream"></param>
        /// <param name="_leaderRecord"></param>
        /// <returns></returns>
        public bool ReadDataRecord(FileStream _inputStream, GmesV4LeaderRecordClass _leaderRecord)
        {
            bool val = false;
            if (_inputStream != null && _leaderRecord != null)
            {
                if (_inputStream.CanRead)
                {
                    int totalSize = (_leaderRecord.Nmes * sizeOfSingleMeasurement) + sizeMinusMeasurements;

                    if (_inputStream.Position + totalSize < _inputStream.Length)
                    {
                        byte[] buffer = new byte[totalSize];
                        _inputStream.Read(buffer, 0, totalSize);

                        MemoryStream memStream = new MemoryStream(buffer);
                        BinaryReader reader = new BinaryReader(memStream);

                        Isat = Convert.ToInt32(reader.ReadByte());
                        Iwrn.SetFlags(reader.ReadByte());
                        Icn01 = Convert.ToInt32(reader.ReadByte());
                        Icn02 = Convert.ToInt32(reader.ReadByte());
                        Lokc1 = Convert.ToInt32(reader.ReadInt32());
                        Lokc2 = Convert.ToInt32(reader.ReadInt32());

                        int i = 0;
                        Msmt.Clear();
                        for (i = 0; i < _leaderRecord.Nmes; i++)
                        {
                            Msmt.Add(Convert.ToDouble(reader.ReadDouble()));
                        }

                        Iode = Convert.ToInt32(reader.ReadInt16());

                        val = true;
                    }
                }
            }

            return val;   
        }
    }
}
