using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;

namespace M7Gdop.FileParsers
{

    /// <summary>
    /// Moses7 Header Record as defined within Suite_RevD.pdf section A-3.2 "Header Record Format"
    /// </summary>
    public class Moses7HeaderRecord
    {

        public char[] inputDataFileType; //input data file type, Possible Values:
                                         //INAV: Inertial Navigation Solution, typically an on-board real-time solution
                                         // DVT: Inertial measurements in the form of platform delta-velocities and delta-tehats
                                         //GMES: GPS pseudorange, carrier-phase, Doppler, and/or delta-range measurements
                                         //GEPH: GPS satellite ephemeris from the GPS telemetry message
                                         //EMES: Earth-centered earth-fixed (ECEF) "measurements", e.g., a GPS-based trajectory
                                         //GSEN: Ground Sensor range, azimuth, elevation, and/or range-rate measurements
        public char[] FileFormAndVersion; // file form and version number e.g "B004" (binary form version 4) or 'A004' (ascii form v4)
        public char[] MissionDate; //in the form of 'yyyymmdd' e.g. '20060921'
        public char[] OpsNum; //Operations number in the form, 'Axxxx'
        public char[] DataID1; //Data source identifier, e.g., 'GAINR','MAGR','GNP','GrafNav'
        public char[] DataID2; //Additional data identifier for GAINR data '<disk#>-<pass#>', or '<pod#>' for GNP
        public char[] Cdate; //File creation date in the form 'yyyymmdd'
        public char[] Ctime; //File creation time in the form, 'hhmmss'
        public char[] spare; //currently unused
        public char[] Dscript; //Data descriptor word specific to each file type, as outlined in file type format sections

        private int recordSize;

        /// <summary>
        /// Initialize header record class
        /// </summary>
        public Moses7HeaderRecord()
        {
            inputDataFileType = new char[4];
            FileFormAndVersion = new char[4];
            MissionDate = new char[8];
            OpsNum = new char[8];
            DataID1 = new char[8];
            DataID2 = new char[8];
            Cdate = new char[8];
            Ctime = new char[8];
            spare = new char[16];
            Dscript = new char[8]; //only last element is used, 1= length in meters, 2= length in feet

            recordSize = 80;
        }

        //return true if this m7header record is valid
        public bool IsThisValidRecord()
        {
            bool val = false;

            if (FileFormAndVersion != null)
            {
                string s = new string(inputDataFileType);
                if (s.ToUpper() == "INAV" || s.ToUpper() == "DVT" || s.ToUpper() == "GMES" || s.ToUpper() == "GEPH" || s.ToUpper() == "EMES" || s.ToUpper() == "GSEN") //only valid results given Suite_RevD.pdf
                {
                    val = true;
                }
            }

            return val;
        }

        /// <summary>
        /// This method will read from a file and set all member attributes for header record information
        /// </summary>
        /// <param name="inputFileStream">Filestream that contains header record</param>
        /// <returns></returns>
        public bool ReadM7HeaderRecord(FileStream inputFileStream)
        {
            bool val = false;
            if (inputFileStream != null)
            {
                if (inputFileStream.CanRead)
                {
                    if (inputFileStream.Position + recordSize < inputFileStream.Length)
                    {

                        byte[] buffer = new byte[recordSize];
                        inputFileStream.Read(buffer, 0, buffer.Length);

                        MemoryStream memStream = new MemoryStream(buffer);
                        BinaryReader reader = new BinaryReader(memStream);

                        inputDataFileType = reader.ReadChars(4);
                        FileFormAndVersion = reader.ReadChars(4);
                        MissionDate = reader.ReadChars(8);
                        OpsNum = reader.ReadChars(8);
                        DataID1 = reader.ReadChars(8);
                        DataID2 = reader.ReadChars(8);
                        Cdate = reader.ReadChars(8);
                        Ctime = reader.ReadChars(8);
                        spare = reader.ReadChars(16);
                        Dscript = reader.ReadChars(8);

                        val = true;
                    }
                    else
                    {
                        val = false;
                    }
                }
            }

            return val;
        }

        /// <summary>
        /// This method will write the header record (in binary) to file stream
        /// provided.
        /// </summary>
        /// <param name="inputFileStream"></param>
        /// <returns></returns>
        public bool WriteM7HeaderRecord(FileStream inputFileStream)
        {
            bool val = false;
            if (inputFileStream != null)
            {
                if (inputFileStream.CanWrite)
                {
                    byte[] buffer = new byte[recordSize];
                    MemoryStream memStream = new MemoryStream(buffer);
                    BinaryWriter bWriter = new BinaryWriter(memStream);

                    bWriter.Write(inputDataFileType, 0, 4);
                    bWriter.Write(FileFormAndVersion, 0, 4);
                    bWriter.Write(MissionDate, 0, 8);
                    bWriter.Write(OpsNum, 0, 8);
                    bWriter.Write(DataID1, 0, 8);
                    bWriter.Write(DataID2, 0, 8);
                    bWriter.Write(Cdate, 0, 8);
                    bWriter.Write(Ctime, 0, 8);
                    bWriter.Write(spare, 0, 16);
                    bWriter.Write(Dscript, 0, 8);
                    bWriter.Flush();

                    BinaryWriter writer = new BinaryWriter(inputFileStream);
                    writer.Write(buffer);
                    writer.Flush();
                    val = true;
                }
            }

            return val;
        }
    }
}
