using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;

namespace M7Gdop.FileParsers
{

    class MRFILMEASBLOCK
    {
        public long BlockSyncLocation;

        public double CurrentMeasurementTime; //time tag for all records this measurement
        public int CurrentNumberOfRecords; //number of records within this measurement
        public int NumberOfParameters; //number of parameters for each record this measurement
        public MRFILRECORD[] Records; //current records this measurement

        public void SetRecordandMeasurementSize()
        {
            int i = 0;
            Records = new MRFILRECORD[CurrentNumberOfRecords];

            for (i = 0; i < CurrentNumberOfRecords; i++)
            {
                Records[i] = new MRFILRECORD();
                Records[i].SetMeasurementSize(NumberOfParameters);
            }
        }
    }

    class MRFILRECORD
    {
        public double GPStime; //seconds of week
        public int MeasurementID; // 10000 * sensor type number + 100 * sensor id number + measurement type number
        public int SensorType; // GPS = 1
        public int SVID; //GPS 1-32
        public int MeasurementNumber; // Description:
                                      // 11 = L1 C/A-code pseudorange
                                      // 12 = L1 P-code pseudorange
                                      // 13 = L1 Carrier Phase
                                      // 14 = L1 Doppler
                                      // 15 = L1 Delta Range
                                      // 21 = L2 C/A-code pseudorange
                                      // 22 = L2 P-code pseudorange
                                      // 23 = L2 Carrier Phase
                                      // 24 = L2 Doppler
                                      // 25 = L2 Delta Range
        public double[] Measurements;

        public void SetMeasurementSize(int numberOfParameters)
        {
            int i = 0;
            Measurements = new double[numberOfParameters];
            for (i = 0; i < numberOfParameters; i++)
            {
                Measurements[i] = new double();
            }

        }

    }



    //class used to store specific functions
    class MRFILCLASS
    {
        public delegate void PercentageChange(PercentScannedEventArgs args);
        public event PercentageChange MrfilPercentChanged = null;
        private double? updatePercentageTime;
        private long fileLength;

        private FileStream file;
        private StreamReader reader;

        public Moses7AsciiHeaderRecord HeaderRecord;
        public MRFILMEASBLOCK CurrentMrfilBlock;
        public MRFILMEASBLOCK PreviousMrfilBlock;

        public double StartTime;
        public double StopTime;

        public bool FileHasBeenInitialized;

        public MRFILCLASS()
        {
            file = null;
            reader = null;

            HeaderRecord = new Moses7AsciiHeaderRecord();
            CurrentMrfilBlock = new MRFILMEASBLOCK();
            PreviousMrfilBlock = new MRFILMEASBLOCK();

            StartTime = CustomNull.Double;
            StopTime = CustomNull.Double;

            FileHasBeenInitialized = false;

            updatePercentageTime = null;

            fileLength = 0;
        }


        public bool InitializeFile(string path)
        {
            bool val = false;
            if (File.Exists(path))
            {
                file = new FileStream(path, FileMode.Open, FileAccess.Read);
                fileLength = file.Length;

                if (file.CanRead)
                {
                    reader = new StreamReader(file);

                    if (HeaderRecord.ReadHeaderRecord(reader))
                    {
                        val = true;

                        string tempString = new string(HeaderRecord.FileType);
                        if (tempString != "MSMT RESIDUALS")
                        {
                            val = false;
                        }
                    }
                }

                FileHasBeenInitialized = true;
            }
            return val;
        }


        public int CloseFile()
        {
            int val = 0;
            reader.Close();
            file.Close();

            if (MrfilPercentChanged != null)
            {
                PercentScannedEventArgs args = new PercentScannedEventArgs(100.0);
                MrfilPercentChanged(args);
            }

            val = 1;
            return val;
        }

        public bool StepForward()
        {
            bool val = false;

            string line;
            string[] lineSplit;
            char[] DelimChars = { ' ' };
            int i;
            int j;

            long ReadPosition = 0;

            if (reader.Peek() >= 0)
            {
                ReadPosition = file.Position;

                //read line and determine number of items in line
                line = reader.ReadLine();
                lineSplit = line.Split(DelimChars, StringSplitOptions.RemoveEmptyEntries);

                //find start of measurement block
                if (lineSplit.Length == 3)
                {
                    //copy data to hold variable to use for data verification
                    PreviousMrfilBlock = CurrentMrfilBlock;

                    //create new class to hold info
                    CurrentMrfilBlock = new MRFILMEASBLOCK();
                    CurrentMrfilBlock.CurrentMeasurementTime = Convert.ToDouble(lineSplit[0]);// double.Parse(lineSplit[0]);
                    CurrentMrfilBlock.CurrentNumberOfRecords = Convert.ToInt32(lineSplit[1]);// int.Parse(lineSplit[1]);
                    CurrentMrfilBlock.NumberOfParameters = Convert.ToInt32(lineSplit[2]);// int.Parse(lineSplit[2]);
                    CurrentMrfilBlock.SetRecordandMeasurementSize();
                    CurrentMrfilBlock.BlockSyncLocation = ReadPosition;

                    if (StartTime == CustomNull.Double) StartTime = CurrentMrfilBlock.CurrentMeasurementTime;
                    StopTime = CurrentMrfilBlock.CurrentMeasurementTime;

                    //now read rest of measurement block and assign values
                    for (i = 0; i < CurrentMrfilBlock.CurrentNumberOfRecords; i++)
                    {
                        if (reader.Peek() >= 0)
                        {
                            //read next line
                            line = reader.ReadLine();
                            lineSplit = line.Split(DelimChars, StringSplitOptions.RemoveEmptyEntries);

                            CurrentMrfilBlock.Records[i].GPStime = Convert.ToDouble(lineSplit[0]);// double.Parse(lineSplit[0]);
                            CurrentMrfilBlock.Records[i].MeasurementID = Convert.ToInt32(lineSplit[1]);// int.Parse(lineSplit[1]);
                            CurrentMrfilBlock.Records[i].SensorType = Convert.ToInt32(lineSplit[2]);// int.Parse(lineSplit[2]);
                            CurrentMrfilBlock.Records[i].SVID = Convert.ToInt32(lineSplit[3]);// int.Parse(lineSplit[3]);
                            CurrentMrfilBlock.Records[i].MeasurementNumber = Convert.ToInt32(lineSplit[4]);// int.Parse(lineSplit[4]);

                            for (j = 0; j < CurrentMrfilBlock.NumberOfParameters; j++)
                            {
                                CurrentMrfilBlock.Records[i].Measurements[j] = Convert.ToDouble(lineSplit[5 + j]);// double.Parse(lineSplit[5 + j]);
                            }
                        }
                        else
                        {
                            val = false;
                        }
                    }

                    if (MrfilPercentChanged != null)
                    {
                        if (updatePercentageTime == null)
                        {
                            PercentScannedEventArgs args = new PercentScannedEventArgs((Convert.ToDouble(file.Position) / Convert.ToDouble(fileLength)) * 100.0);
                            MrfilPercentChanged(args);
                            updatePercentageTime = CurrentMrfilBlock.CurrentMeasurementTime;
                        }
                        else
                        {
                            if ((CurrentMrfilBlock.CurrentMeasurementTime - updatePercentageTime) >= 10.0)
                            {
                                PercentScannedEventArgs args = new PercentScannedEventArgs((Convert.ToDouble(file.Position) / Convert.ToDouble(fileLength)) * 100.0);
                                MrfilPercentChanged(args);
                                updatePercentageTime = CurrentMrfilBlock.CurrentMeasurementTime;
                            }
                        }


                    }

                    val = true;
                }
            }
            else
            {
                val = false;
            }

            return val;
        }

        public HashSet<int> FindAllNonRejectedSVIDs()
        {
            HashSet<int> finalList = new HashSet<int>();

            if (PreviousMrfilBlock.Records != null)
            {
                foreach (MRFILRECORD rec in CurrentMrfilBlock.Records)
                {
                    if (CheckForDuplicateMeasurement(rec) != 1 && CheckForRejectedMeasurement(rec) != 1)
                    {
                        if (rec.MeasurementNumber == 11 || rec.MeasurementNumber == 12 || rec.MeasurementNumber == 13 ||
                            rec.MeasurementNumber == 21 || rec.MeasurementNumber == 22 || rec.MeasurementNumber == 23)
                        {
                            finalList.Add(rec.SVID);
                        }
                    }
                    else
                    {
                        int testbreak = 0;
                    }

                }
            }
            else
            {
                foreach (MRFILRECORD rec in CurrentMrfilBlock.Records)
                {
                    finalList.Add(rec.SVID);
                }
            }

            return finalList;
        }

        //returns 1 if measurement is duplicate
        public int CheckForDuplicateMeasurement(MRFILRECORD current)
        {
            int val = 1;
            int i;
            int k;

            if (PreviousMrfilBlock.Records != null)
            {
                //first determine which record within previous block is matching this one
                for (i = 0; i < PreviousMrfilBlock.Records.Length; i++)
                {
                    if (PreviousMrfilBlock.Records[i].SVID == current.SVID && PreviousMrfilBlock.Records[i].MeasurementNumber == current.MeasurementNumber)
                    {
                        for (k = 0; k < PreviousMrfilBlock.Records[i].Measurements.Length; k++)
                        {
                            if (current.Measurements[k] != PreviousMrfilBlock.Records[i].Measurements[k])
                            {
                                val = 0;
                            }
                        }
                        break;
                    }
                }
            }
            else
            {
                val = 0;
            }
            return val;
        }

        //returns 1 if measurement is being rejected, expects 5th measurement to represent rejection window
        public int CheckForRejectedMeasurement(MRFILRECORD current)
        {
            int val = 0;
            int i;
            int k;

            if (PreviousMrfilBlock.Records != null)
            {
                //first determine which record in previous block is matching this one
                for (i = 0; i < PreviousMrfilBlock.Records.Length; i++)
                {
                    if (PreviousMrfilBlock.Records[i].SVID == current.SVID && PreviousMrfilBlock.Records[i].MeasurementNumber == current.MeasurementNumber)
                    {
                        if (current.Measurements[4] > PreviousMrfilBlock.Records[i].Measurements[4])
                        {
                            val = 1;
                        }
                        break;
                    }
                }
            }
            return val;
        }

        //returns 1 if measurement is currently outside of sigma lines
        public int CheckForMeasurementOutsideSigmas(MRFILRECORD current)
        {
            int val = 0;

            if (current.Measurements[0] > (current.Measurements[1]))
            {
                val = 1;
            }
            return val;
        }
    }
}
