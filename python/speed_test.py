#!/usr/bin/env python

# ==============================================================================
# Imports.
# ==============================================================================

import os;
import errno;
import json;

import mysql.connector;
from mysql.connector import errorcode;

from datetime import datetime;


# ==============================================================================
# Global declarations.
# ==============================================================================

# Path to store speed test results.
LOGS_PATH = "log_files";

# Path to store speed test result that have been saved to the cloud database.
TRASH_PATH = "pushed_logs";

# The command to perform the speed test.
SPEED_TEST_COMMAND = "speedtest --output-header -f json-pretty > " + LOGS_PATH + "/$(date +'%Y-%m-%d_%H:%M:%S').json";

# Database hostname.
DB_HOSTNAME = "my-own-domain.com";

# Database's name.
DB_NAME = "my-database-name";

# Database user.
DB_USERNAME = "my-database-user";

# Database user's pass.
DB_USER_PASSWORD = "password-of-my-user";


# ==============================================================================
# Main class definition.
# ==============================================================================

class SpeedTest():

    # This class initializer.. -------------------------------------------------
    def __init__( self ):

        os.system( "mkdir -p " + LOGS_PATH  );
        os.system( "mkdir -p " + TRASH_PATH );

    # --------------------------------------------------------------------------


    # Runs the test and saves the result as a log file. ------------------------
    def run( self ):

        os.system( SPEED_TEST_COMMAND );

    # --------------------------------------------------------------------------


    # Reads the logs path, reads them and pushes their info to the database. ---
    def push( self ):

        dataInserted = 0;

        print( "Reading logs directory (\"" + LOGS_PATH  + "\") ..." );

        for root, dirs, files in os.walk( LOGS_PATH ):
            for file in files:
                print( "Processing file: \"" + file + "\"...");
                with open( LOGS_PATH + "/"  + file ) as json_file:
                    dataInserted = self.insertIntoDatabase( json.load( json_file  ) );

                if( dataInserted == 1 ):
                    os.system( "mv " + LOGS_PATH + "/" + file + " " + TRASH_PATH + "/" + file );
                    dataInserted = 0;

    # --------------------------------------------------------------------------


    # Inserts a record into the Database. --------------------------------------
    def insertIntoDatabase( self, data ):

        print( "Saving to database ..." );

        try:
            connection = mysql.connector.connect( user     = DB_USERNAME,
                                                  password = DB_USER_PASSWORD,
                                                  host     = DB_HOSTNAME,
                                                  database = DB_NAME );
        except mysql.connector.Error as err:
            if( err.errno == errocode.ER_ACCESS_DENIED_ERROR ):
                print( "    Error: Invalid username or password!" );
                return 0;
            elif( err.errno == errorcode.ER_BAD_DB_ERROR ):
                print( "    Error: Database does not exist!" );
                return 0;
            else:
                print( err );
                return 0;

        cursor = connection.cursor();

        # Inserting new record.

        STR_INSERT = "INSERT INTO ST_RESULT( type, timestamp, ping_jitter, "      + \
            "ping_latency, download_bandwith, download_bytes, download_elapsed, " + \
            "upload_bandwith, upload_bytes, upload_elapsed, packetLoss, isp, "    + \
            "interface_internalIp, interface_name, interface_macAddr, "           + \
            "interface_isVpn, interface_externalIp, server_id, server_name, "     + \
            "server_location, server_country, server_host, server_port, "         + \
            "server_ip, result_id, result_url ) "                                 + \
            \
            "VALUES ( %(type)s, %(timestamp)s, %(ping_jitter)s, %(ping_latency)s, " + \
            "%(download_bandwith)s, %(download_bytes)s, %(download_elapsed)s, "     + \
            "%(upload_bandwith)s, %(upload_bytes)s, %(upload_elapsed)s, "           + \
            "%(packetLoss)s, %(isp)s, %(interface_internalIp)s, "                   + \
            "%(interface_name)s, %(interface_macAddr)s, %(interface_isVpn)s, "      + \
            "%(interface_externalIp)s, %(server_id)s, %(server_name)s, "            + \
            "%(server_location)s, %(server_country)s, %(server_host)s, "            + \
            "%(server_port)s, %(server_ip)s, %(result_id)s, %(result_url)s )";

        STR_VALUES = { 'type'                 : data['type'],
                       'timestamp'            : datetime.strptime( data['timestamp'], '%Y-%m-%dT%H:%M:%SZ' ),
                       'ping_jitter'          : data['ping']['jitter'],
                       'ping_latency'         : data['ping']['latency'],
                       'download_bandwith'    : data['download']['bandwidth'],
                       'download_bytes'       : data['download']['bytes'],
                       'download_elapsed'     : data['download']['elapsed'],
                       'upload_bandwith'      : data['upload']['bandwidth'],
                       'upload_bytes'         : data['upload']['bytes'],
                       'upload_elapsed'       : data['upload']['elapsed'],
                       'packetLoss'           : data['packetLoss'],
                       'isp'                  : data['isp'],
                       'interface_internalIp' : data['interface']['internalIp'],
                       'interface_name'       : data['interface']['name'],
                       'interface_macAddr'    : data['interface']['macAddr'],
                       'interface_isVpn'      : data['interface']['isVpn'],
                       'interface_externalIp' : data['interface']['externalIp'],
                       'server_id'            : data['server']['id'],
                       'server_name'          : data['server']['name'],
                       'server_location'      : data['server']['location'],
                       'server_country'       : data['server']['country'],
                       'server_host'          : data['server']['host'],
                       'server_port'          : data['server']['port'],
                       'server_ip'            : data['server']['ip'],
                       'result_id'            : data['result']['id'],
                       'result_url'           : data['result']['url']
        };

        cursor.execute( STR_INSERT, STR_VALUES );
        connection.commit();

        print( "    New record inserted!" );
        cursor.close();
        connection.close();

        return 1;

    # --------------------------------------------------------------------------


# ==============================================================================
# Main program.
# ==============================================================================

# Create new instance to perform the speed test.
speedTest = SpeedTest();

# Run teh speed test.
speedTest.run();

# Push this and any pending to push speed test results.
speedTest.push();
