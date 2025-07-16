#!/usr/bin/env python

# ==============================================================================
# Imports.
# ==============================================================================

import subprocess;
import errno;
import json;

import sqlite3;


# ==============================================================================
# Global declarations.
# ==============================================================================

# The command to perform the speed test.
SPEED_TEST_COMMAND = "/app/speedtest -f json-pretty";

# Database's name.
DB_NAME = "/app/database/speedtest.sqlite3";


# ==============================================================================
# Classes definition.
# ==============================================================================

class SpeedTest():

    # This class initializer. --------------------------------------------------
    def __init__( self, connector ):
        self.conn = connector;
        self.result = {};
        self.lastSpeedtestWithError = False;
    
    # --------------------------------------------------------------------------

    
    # Runs the test and holds the result. --------------------------------------
    def run( self ):
        try:
            self.result = json.loads( subprocess.check_output( SPEED_TEST_COMMAND, shell=True, text=True ) );
            #print( self.result );
        except subprocess.CalledProcessError as e:
            self.lastSpeedtestWithError = True;
            print( f"Error executing command: {e}" );
    
    # --------------------------------------------------------------------------


    # Insert the result into the database. -------------------------------------
    def push( self ):
        if( self.lastSpeedtestWithError == False ):
            STR_INSERT = "INSERT INTO rawResults( type, timestamp, ping_jitter, ping_latency, ping_low, ping_high, download_bandwith, download_bytes, download_elapsed, download_latency_iqm, download_latency_low, download_latency_high, download_latency_jitter, upload_bandwith, upload_bytes, upload_elapsed, upload_latency_iqm, upload_latency_low, upload_latency_high, upload_latency_jitter, isp, interface_internalIp, interface_name, interface_macAddr, interface_isVpn, interface_externalIp, server_id, server_host, server_port, server_name, server_location, server_country, server_ip, result_id, result_url, result_persisted ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
            STR_VALUES = ( self.result["type"], self.result["timestamp"], self.result["ping"]["jitter"], self.result["ping"]["latency"], self.result["ping"]["low"], self.result["ping"]["high"], self.result["download"]["bandwidth"], self.result["download"]["bytes"], self.result["download"]["elapsed"], self.result["download"]["latency"]["iqm"], self.result["download"]["latency"]["low"], self.result["download"]["latency"]["high"], self.result["download"]["latency"]["jitter"], self.result["upload"]["bandwidth"], self.result["upload"]["bytes"],self.result["upload"]["elapsed"], self.result["upload"]["latency"]["iqm"], self.result["upload"]["latency"]["low"], self.result["upload"]["latency"]["high"], self.result["upload"]["latency"]["jitter"], self.result["isp"], self.result["interface"]["internalIp"], self.result["interface"]["name"], self.result["interface"]["macAddr"], self.result["interface"]["isVpn"], self.result["interface"]["externalIp"], self.result["server"]["id"], self.result["server"]["host"], self.result["server"]["port"], self.result["server"]["name"], self.result["server"]["location"], self.result["server"]["country"], self.result["server"]["ip"],self.result["result"]["id"], self.result["result"]["url"], self.result["result"]["persisted"] );

            try:
                cur = self.conn.cursor();
                cur.execute( STR_INSERT, STR_VALUES );
                self.conn.commit();
            except sqlite3.Error as err:
                print( err );

    # --------------------------------------------------------------------------


# ==============================================================================
# Main program.
# ==============================================================================

# Establish connection with the database.
try:
    conn = sqlite3.connect( DB_NAME );
except sqlite3.Error as err:
    print( err );

# Create new instance to perform the speed test.
speedTest = SpeedTest( conn );

# Run the speed test.
speedTest.run();

# Push this and any pending to push speed test results.
speedTest.push();

# All done, close the database connection.
conn.close();