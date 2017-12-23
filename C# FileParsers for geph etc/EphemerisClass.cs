using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Windows.Forms;

namespace M7Gdop.FileParsers
{


    /// <summary>
    /// Container for a single ephemeris record
    /// </summary>
    public class GephVersion4
    {
        public double Tgeph; //GPS Time (Seconds of Week)
        public Int16 SV_ID; // Space Vehicle PRN number
        public Int16 Week; // GPS week number
        public Int32 AODC; //
        public Int32 Toc;
        public Int32 Toe; //reference time ephemeris
        public Single Af1;
        public Single Af2;
        public Single DeltaN; // Mean motion difference from computed value (rad/s)
        public Single IDOT; //rate of inclination angle (rad/s)
        public Single Crs; // Sine harmonic correction to orbit radius (meters)
        public Single Cuc; // sine harmonic correction to argument of latitude (rad)
        public Single Cus; //sine harmonic correction to argument of latitude (rad)
        public Single Cic; //cosine harmonic correction to angle of inclination (rad)
        public Single Cis; //harmonic correction to angle of inclination (rad)
        public Single Crc; //cosine harmonic correction to orbit radius (m)
        public double Af0;
        public double M0; // mean anomaly at reference time (rad)
        public double e; //Orbit eccentricity
        public double RootA; //square root of semi-major axis (m^1/2)
        public double Omega0; //longitude of ascending node of orbit plane at reference time
        public double I0; //inclination angle at reference time (rad)
        public double omega; //argument of perigee (rad)
        public double OmegaDot; //rate of rightascension (rad/s)

        public static int SizeOfMessage = 128;



    }

    /// <summary>
    /// This class can parse and store all ephemeris records within an ephemeris file (geph.eph)
    /// </summary>
    public class EphemerisClass
    {
        
        private FileStream file;

        private Moses7HeaderRecord header;
        private List<GephVersion4> ephemRecords;

        //delegate and event to handle percentage change
        public delegate void PercentageChanged(PercentScannedEventArgs args);
        public event PercentageChanged EphemerisPercentChanged = null;

        public bool ReadOk;

        /// <summary>
        /// Class constructor, set everything to null
        /// </summary>
        public EphemerisClass()
        {
            file = null;
            ephemRecords = null;
            header = null;
            
        }

        /// <summary>
        /// InitializeClass function will verify file exists at given path and open it for reading
        /// </summary>
        /// <param name="filePath"></param>
        /// <returns></returns>
        public bool InitializeClass(string filePath)
        {
            bool val = false;

            if (File.Exists(filePath))
            {
               
                file = new FileStream(filePath, FileMode.Open, FileAccess.Read);

                ephemRecords = new List<GephVersion4>(); //initialzie new list to store all records
                header = new Moses7HeaderRecord();

                if (file != null)
                {
                    if (file.CanRead)
                    {
                        if (header.ReadM7HeaderRecord(file))
                        {
                            if (header.IsThisValidRecord())
                            {
                                string tempString = new string(header.inputDataFileType);
                                if (tempString.ToUpper() == "GEPH")
                                {
                                    if (ReadEphemerisFile())
                                    {
                                        CloseFile();
                                        val = true;
                                    }
                                }
                            }
                        }
                    }
                }
                
                
            }


            return val;
        }

        /// <summary>
        /// Close ephemeris file
        /// </summary>
        /// <returns></returns>
        public bool CloseFile()
        {
            bool val = false;

            if (file != null)
            {
                file.Close();
                file = null;
                val = true;

                if (EphemerisPercentChanged != null)
                {
                    PercentScannedEventArgs args = new PercentScannedEventArgs(100.0);
                    EphemerisPercentChanged(args);
                }
            }

            return val;
        }

        /// <summary>
        /// This method will read all ephemeris records in the file and add them to the 
        /// ephemeris record list. It will return true if ephemeris records were found, false
        /// other wise.
        /// </summary>
        /// <returns></returns>
        public bool ReadEphemerisFile()
        {
            bool val = false;

            if (file != null)
            {
                if (file.CanRead)
                {
                    while (file.Position < file.Length)
                    {
                        if (file.Length - file.Position >= GephVersion4.SizeOfMessage)
                        {
                            
                            byte[] buffer = new byte[GephVersion4.SizeOfMessage];
                            file.Read(buffer, 0, buffer.Length);

                            MemoryStream memStream = new MemoryStream(buffer);
                            BinaryReader reader = new BinaryReader(memStream);


                            ephemRecords.Add(new GephVersion4());
                            ephemRecords[ephemRecords.Count - 1].Tgeph = reader.ReadDouble();
                            ephemRecords[ephemRecords.Count - 1].SV_ID = reader.ReadInt16();
                            ephemRecords[ephemRecords.Count - 1].Week = reader.ReadInt16();
                            ephemRecords[ephemRecords.Count - 1].AODC = reader.ReadInt32();
                            ephemRecords[ephemRecords.Count - 1].Toc = reader.ReadInt32();
                            ephemRecords[ephemRecords.Count - 1].Toe = reader.ReadInt32();
                            ephemRecords[ephemRecords.Count - 1].Af1 = reader.ReadSingle();
                            ephemRecords[ephemRecords.Count - 1].Af2 = reader.ReadSingle();
                            ephemRecords[ephemRecords.Count - 1].DeltaN = reader.ReadSingle();
                            ephemRecords[ephemRecords.Count - 1].IDOT = reader.ReadSingle();
                            ephemRecords[ephemRecords.Count - 1].Crs = reader.ReadSingle();
                            ephemRecords[ephemRecords.Count - 1].Cuc = reader.ReadSingle();
                            ephemRecords[ephemRecords.Count - 1].Cus = reader.ReadSingle();
                            ephemRecords[ephemRecords.Count - 1].Cic = reader.ReadSingle();
                            ephemRecords[ephemRecords.Count - 1].Cis = reader.ReadSingle();
                            ephemRecords[ephemRecords.Count - 1].Crc = reader.ReadSingle();
                            ephemRecords[ephemRecords.Count - 1].Af0 = reader.ReadDouble();
                            ephemRecords[ephemRecords.Count - 1].M0 = reader.ReadDouble();
                            ephemRecords[ephemRecords.Count - 1].e = reader.ReadDouble();
                            ephemRecords[ephemRecords.Count - 1].RootA = reader.ReadDouble();
                            ephemRecords[ephemRecords.Count - 1].Omega0 = reader.ReadDouble();
                            ephemRecords[ephemRecords.Count - 1].I0 = reader.ReadDouble();
                            ephemRecords[ephemRecords.Count - 1].omega = reader.ReadDouble();
                            ephemRecords[ephemRecords.Count - 1].OmegaDot = reader.ReadDouble();
                            val = true;
                        }
                        else
                        {
                            break;
                        }
                    }
                }

                ephemRecords = FindValidRecords(ephemRecords);

                if (ephemRecords != null)
                {
                    if (ephemRecords.Count == 0)
                    {
                        val = false;
                    }
                    else
                    {
                        ephemRecords.Sort((x, y) => x.Toe.CompareTo(y.Toe));
                    }
                }

                
            }

            return val;
        }

        private List<GephVersion4> FindValidRecords(List<GephVersion4> _recs)
        {
            List<GephVersion4> outRecs = new List<GephVersion4>();
            foreach (GephVersion4 rec in _recs)
            {
                if (rec.Tgeph >= 0.0 && rec.Tgeph <= 604800.0)
                {
                    if (rec.SV_ID < 50 && rec.SV_ID >= 0)
                    {
                        outRecs.Add(rec);
                    }
                }
            }
            
            return outRecs;
        }

        /// <summary>
        /// This method will return an ephemeris record that best corresponds to the PRN ID and the time provided, if none
        /// are found it returns a null.
        /// </summary>
        /// <param name="SV_PRN"></param>
        /// <param name="Gps_Time"></param>
        /// <returns></returns>
        private GephVersion4 ChooseEphemRecord(int SV_PRN, double Gps_Time)
        {
            GephVersion4 rec = new GephVersion4();
            int i;
            int selectedEphemRecordIndex = -1;

            if (ephemRecords != null)
            {

                //first find ephem record to use for this SV and time
                List<int> possibleRecordIndex = new List<int>();
                for (i = 0; i < ephemRecords.Count; i++)
                {
                    if (ephemRecords[i].SV_ID == SV_PRN)
                    {
                        if (Math.Abs(Gps_Time - ephemRecords[i].Toe) <= 2 * 60 * 60)
                        {
                            possibleRecordIndex.Add(i);
                        }
                    }
                }

                if (possibleRecordIndex.Count > 1)
                {
                    selectedEphemRecordIndex = 0;

                    for (i = 0; i < possibleRecordIndex.Count; i++)
                    {
                        if (Math.Abs(Gps_Time - ephemRecords[possibleRecordIndex[i]].Toe) < Math.Abs(Gps_Time - ephemRecords[possibleRecordIndex[selectedEphemRecordIndex]].Toe))
                        {
                            selectedEphemRecordIndex = i;
                        }
                    }

                }
                else if (possibleRecordIndex.Count == 1)
                {
                    selectedEphemRecordIndex = 0;
                }
                else
                {
                    selectedEphemRecordIndex = -1;
                }

                if (selectedEphemRecordIndex != -1)
                {
                    rec = ephemRecords[possibleRecordIndex[selectedEphemRecordIndex]];
                }
                else
                {
                    rec = null;
                }
            }
            else
            {
                rec = null;
            }

            return rec;
        }

        /// <summary>
        /// This method wil return the ECEF position for a satellite at a given time. It will return
        /// null if no result was possible (i.e. time and satellite ephem record not found)
        /// </summary>
        /// <param name="SV_PRN"></param>
        /// <param name="TransmissionTime"></param>
        /// <returns></returns>
        public Coordinates.ECEF CalculateSVPositionAtTime(int SV_PRN, double TransmissionTime)
        {
            Coordinates.ECEF result = new Coordinates.ECEF();

            GephVersion4 selectedEphemRecord = ChooseEphemRecord(SV_PRN, TransmissionTime);

            if (selectedEphemRecord != null)
            {
                //Parameters from WGS84
                double GM = Constants.WGS84.GM; // m^3/s^2
                double omegaE = Constants.WGS84.omegaE; // rad/s

                //check for type of units via the M7HeaderMessage Data Descriptor
                if (header.Dscript[7] != '1')
                {
                    throw new Exception("Error Ephemeris record not in meters and radians, this isn't supposed to happen");
                }

                //Calculating the satellite clock offset and adjusting time
                double dt = TransmissionTime - selectedEphemRecord.Toc;

                if (dt > 304200.0)
                {
                    dt = dt - 604800.0;
                }
                else if (dt < -304200.0)
                {
                    dt = dt + 604800.0;
                }

                double svTimeOffset = selectedEphemRecord.Af0 + selectedEphemRecord.Af1 * (dt) + selectedEphemRecord.Af2 * Math.Pow(dt, 2.0);

                double svTransmissionTime = TransmissionTime - svTimeOffset;

                //Seconds elapsed from the reference epoch
                //double DeltaT = TransmissionTime - selectedEphemRecord.Toe;
                double DeltaT = svTransmissionTime - selectedEphemRecord.Toe;

                //check for week rollover and adjust if needed
                if (DeltaT > 304200.0)
                {
                    DeltaT = DeltaT - 604800.0;
                }
                else if (DeltaT < -304200.0)
                {
                    DeltaT = DeltaT + 604800.0;
                }

                //Mean motion (RootA is Square Root of a, to get a^3 we need RootA^6)
                double n0 = Math.Sqrt(GM / Math.Pow(selectedEphemRecord.RootA, 6.0));
                double n = n0 + selectedEphemRecord.DeltaN;

                //Mean anomaly
                double M = selectedEphemRecord.M0 + n * DeltaT;

                //Excentric anomaly by iteration
                double E0 = M;
                double E = M + selectedEphemRecord.e * Math.Sin(E0);
                double EMinusE0 = E - E0;
                E0 = E; //this is technically the first iteration

                //the 1e-11 signified the number of decimal places they need to be equal out to
                //Kepeler iteration
                while (Math.Abs(EMinusE0) > 1e-12)
                {
                    E = M + selectedEphemRecord.e * Math.Sin(E0);
                    EMinusE0 = E - E0;
                    E0 = E;
                }


                //True anomaly
                double CosV = (Math.Cos(E) - selectedEphemRecord.e) / (1 - selectedEphemRecord.e * Math.Cos(E));
                double SinV = (Math.Sqrt(1 - Math.Pow(selectedEphemRecord.e, 2.0)) * Math.Sin(E)) / (1 - selectedEphemRecord.e * Math.Cos(E));       

                double v = Math.Atan2(SinV,CosV);


                #region Method1
                //argument of perigee
                double omega = selectedEphemRecord.omega + selectedEphemRecord.Cuc * Math.Cos(2 * (selectedEphemRecord.omega + v)) + selectedEphemRecord.Cus * Math.Sin(2 * (selectedEphemRecord.omega + v));

                //radial distance
                double r = Math.Pow(selectedEphemRecord.RootA, 2.0) * (1 - selectedEphemRecord.e * Math.Cos(E)) + selectedEphemRecord.Crc * Math.Cos(2 * (selectedEphemRecord.omega + v)) + selectedEphemRecord.Crs * Math.Sin(2 * (selectedEphemRecord.omega + v));

                //inclination
                double i = selectedEphemRecord.I0 + selectedEphemRecord.IDOT * DeltaT + selectedEphemRecord.Cic * Math.Cos(2 * (selectedEphemRecord.omega + v)) + selectedEphemRecord.Cis * Math.Sin(2 * (selectedEphemRecord.omega + v));

                //compute right ascension
                double Omega = selectedEphemRecord.Omega0 + (selectedEphemRecord.OmegaDot - omegaE) * DeltaT - omegaE * selectedEphemRecord.Toe;

                //now do rotation into ECEF coordinates [E,F,G]=RMatrix*rMatrix
                double[] rMatrix = { r * Math.Cos(v), r * Math.Sin(v), 0 };
                double[,] RMatrix = new double[3, 3];
                RMatrix[0, 0] = Math.Cos(Omega) * Math.Cos(omega) - Math.Sin(Omega) * Math.Sin(omega) * Math.Cos(i);
                RMatrix[0, 1] = (-1.0) * Math.Cos(Omega) * Math.Sin(omega) - Math.Sin(Omega) * Math.Cos(omega) * Math.Cos(i);
                RMatrix[0, 2] = Math.Sin(Omega) * Math.Sin(i);
                RMatrix[1, 0] = Math.Sin(Omega) * Math.Cos(omega) + Math.Cos(Omega) * Math.Sin(omega) * Math.Cos(i);
                RMatrix[1, 1] = (-1.0) * Math.Sin(Omega) * Math.Sin(omega) + Math.Cos(Omega) * Math.Cos(omega) * Math.Cos(i);
                RMatrix[1, 2] = (-1.0) * Math.Cos(Omega) * Math.Sin(i);
                RMatrix[2, 0] = Math.Sin(omega) * Math.Sin(i);
                RMatrix[2, 1] = Math.Cos(omega) * Math.Sin(i);
                RMatrix[2, 2] = Math.Cos(i);

                double[,] Ecef = MatrixFunctions.Multiply(RMatrix, rMatrix);

                //double Ecef_E = RMatrix[0, 0] * rMatrix[0] + RMatrix[0, 1] * rMatrix[1] + RMatrix[0, 2] * rMatrix[2];
                //double Ecef_F = RMatrix[1, 0] * rMatrix[0] + RMatrix[1, 1] * rMatrix[1] + RMatrix[1, 2] * rMatrix[2];
                //double Ecef_G = RMatrix[2, 0] * rMatrix[0] + RMatrix[2, 1] * rMatrix[1] + RMatrix[2, 2] * rMatrix[2];

                result.E = Ecef[0,0];
                result.F = Ecef[1,0];
                result.G = Ecef[2, 0];
                #endregion

                #region Secondary Method (both methods return same result, so used method above
                ////Argument of longitude
                //double du = selectedEphemRecord.Cuc * Math.Cos(2 * (v + selectedEphemRecord.omega)) + selectedEphemRecord.Cus * Math.Sin(2 * (v + selectedEphemRecord.omega));
                //double u = v + selectedEphemRecord.omega + du;

                ////Radius
                //double dr = selectedEphemRecord.Crc * Math.Cos(2 * (v + selectedEphemRecord.omega)) + selectedEphemRecord.Crs * Math.Sin(2 * (v + selectedEphemRecord.omega));
                //double r2 = Math.Pow(selectedEphemRecord.RootA, 2.0) * (1 - selectedEphemRecord.e * Math.Cos(E)) + dr;

                ////Coordinates of GPS SV in orbital plane
                //double x = r2 * Math.Cos(u);
                //double y = r2 * Math.Sin(u);

                ////Orbit inclination
                //double di = selectedEphemRecord.Cic * Math.Cos(2 * (v + selectedEphemRecord.omega)) + selectedEphemRecord.Cis * Math.Sin(2 * (v + selectedEphemRecord.omega));
                //double i2 = selectedEphemRecord.I0 + selectedEphemRecord.IDOT * DeltaT + di;

                ////Longitude of ascending node (right ascension)
                //double Omega2 = selectedEphemRecord.Omega0 + (selectedEphemRecord.OmegaDot - omegaE) * DeltaT - omegaE * selectedEphemRecord.Toe;

                ////WGS84 Coordinates
                //double X = x * Math.Cos(Omega2) - y * Math.Sin(Omega2) * Math.Cos(i2);
                //double Y = x * Math.Sin(Omega2) + y * Math.Cos(Omega2) * Math.Cos(i2);
                //double Z = y * Math.Sin(i2);

                //result.E = X;
                //result.F = Y;
                //result.G = Z;
                #endregion
            }
            else
            {
                result = null;
            }

            return result;
        }

    }
}
