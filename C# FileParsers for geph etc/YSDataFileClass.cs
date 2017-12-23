using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;

namespace M7Gdop.FileParsers
{
    /// <summary>
    /// This class can deblock/parse a moses7 ys file. 
    /// </summary>
    public class YSDataFileClass
    {
        private FileStream file; //file stream used to process file
        private StreamReader reader;

        public Moses7AsciiHeaderRecord HeaderRecord;
        public YSDataMessageBlock message;

        private long fileLength; 

        public delegate void PercentageChange(PercentScannedEventArgs args);
        public event PercentageChange YsPercentChanged = null;


        public double StartTime;
        public double StopTime;

        private double? updatePercentageTime;
        
        /// <summary>
        /// Class constructor, initialize all values
        /// </summary>
        public YSDataFileClass()
        {
            message = new YSDataMessageBlock();
            fileLength = 0;
            file = null;
            reader = null;
            HeaderRecord = new Moses7AsciiHeaderRecord();

            StartTime = CustomNull.Double;
            StopTime = CustomNull.Double;

            updatePercentageTime = null;
        }

        /// <summary>
        /// This method will initialze a ysmthf file given a string path to the file. It will 
        /// return true if everything was ok, false if bad stuff happened. If false, file not 
        /// valid for use.
        /// </summary>
        /// <param name="filePath"></param>
        /// <returns></returns>
        public bool InitializeFile(string filePath)
        {
            bool val = false;
            if (File.Exists(filePath))
            {
                file = new FileStream(filePath, FileMode.Open, FileAccess.Read);
                reader = new StreamReader(file);
                fileLength = file.Length;
                
                if (HeaderRecord.ReadHeaderRecord(reader))
                {
                    val = true;

                    string tempString = new string(HeaderRecord.FileType);
                    if (tempString != "YSTATES/SIGMAS") ///this is a ys file, if this isn't true then there's a problem
                    {
                        val = false;
                    }
                }
            }

            return val;
        }

        /// <summary>
        /// This method will read through the file stream one record at a time (in this case one line at a time)
        /// each record will be parsed into the appropriate record formats
        /// </summary>
        /// <returns></returns>
        public bool ReadNextRecord()
        {
            bool val = false;
            string line = "";
            string[] lineSplit;
            char[] delimiters = { ' ' };
            if (file != null)
            {
                
                if (reader != null)
                {
                    if (reader.Peek() >= 0)
                    {
                        line = reader.ReadLine();
                        lineSplit = line.Split(delimiters, StringSplitOptions.RemoveEmptyEntries);
                        if (lineSplit.Length >= 19)
                        {
                            message.gpsTime = Convert.ToDouble(lineSplit[0]);

                            message.positionVector[0] = Convert.ToDouble(lineSplit[1]);
                            message.positionVector[1] = Convert.ToDouble(lineSplit[2]);
                            message.positionVector[2] = Convert.ToDouble(lineSplit[3]);

                            message.velocityVector[0] = Convert.ToDouble(lineSplit[4]);
                            message.velocityVector[1] = Convert.ToDouble(lineSplit[5]);
                            message.velocityVector[2] = Convert.ToDouble(lineSplit[6]);

                            message.attitudeVector[0] = Convert.ToDouble(lineSplit[7]);
                            message.attitudeVector[1] = Convert.ToDouble(lineSplit[8]);
                            message.attitudeVector[2] = Convert.ToDouble(lineSplit[9]);

                            message.accelerationVector[0] = Convert.ToDouble(lineSplit[10]);
                            message.accelerationVector[1] = Convert.ToDouble(lineSplit[11]);
                            message.accelerationVector[2] = Convert.ToDouble(lineSplit[12]);

                            message.specificForceVector[0] = Convert.ToDouble(lineSplit[13]);
                            message.specificForceVector[1] = Convert.ToDouble(lineSplit[14]);
                            message.specificForceVector[2] = Convert.ToDouble(lineSplit[15]);

                            message.attitudeRatesVector[0] = Convert.ToDouble(lineSplit[16]);
                            message.attitudeRatesVector[1] = Convert.ToDouble(lineSplit[17]);
                            message.attitudeRatesVector[2] = Convert.ToDouble(lineSplit[18]);

                            //set the start time of the file if haven't been set yet
                            if (StartTime == CustomNull.Double)
                            {
                                StartTime = message.gpsTime;
                            }

                            //set the stop time of file so on last record we're left with stop time
                            StopTime = message.gpsTime;

                            val = true;
                        }

                        if (updatePercentageTime == null)
                        {
                            if (YsPercentChanged != null)
                            {
                                PercentScannedEventArgs args = new PercentScannedEventArgs((Convert.ToDouble(file.Position) / Convert.ToDouble(fileLength)) * 100.0);
                                YsPercentChanged(args);
                            }

                            updatePercentageTime = message.gpsTime;
                        }
                        else
                        {
                            if (message.gpsTime - updatePercentageTime >= 10.0)
                            {
                                if (YsPercentChanged != null)
                                {
                                    PercentScannedEventArgs args = new PercentScannedEventArgs((Convert.ToDouble(file.Position) / Convert.ToDouble(fileLength)) * 100.0);
                                    YsPercentChanged(args);
                                }

                                updatePercentageTime = message.gpsTime;
                            }
                        }
                        
                    }
                    else
                    {
                        
                    }
                }
            }

            return val;
        }

        /// <summary>
        /// This method will close the open file stream and trigger an event
        /// to let listeners know we're done with the file
        /// </summary>
        public void CloseFile()
        {
            file.Dispose();
            file.Close();

            if (YsPercentChanged != null)
            {
                PercentScannedEventArgs args = new PercentScannedEventArgs(100.0);
                YsPercentChanged(args);
            }
        }

    }

    /// <summary>
    /// This class will store a single YS data block (a single line in ysmthf.asc)
    /// </summary>
    public class YSDataMessageBlock
    {
        public double gpsTime;
        public double[] positionVector;
        public double[] velocityVector;
        public double[] attitudeVector;
        public double[] accelerationVector;
        public double[] specificForceVector;
        public double[] attitudeRatesVector;

        public YSDataMessageBlock()
        {
            gpsTime = 0.0;
            positionVector = new double[3];
            velocityVector = new double[3];
            attitudeVector = new double[3];
            accelerationVector = new double[3];
            specificForceVector = new double[3];
            attitudeRatesVector = new double[3];

        }


    }
}
