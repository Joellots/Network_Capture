@echo off

REM Add Wireshark directory to PATH (if not already added)
set WIRESHARK_DIR=C:\Program Files\Wireshark
set PATH=%PATH%;%WIRESHARK_DIR%

REM Set the interface number. List interfaces with `tshark -D` if unknown
set INTERFACE_NUM=5
REM Set the duration of the capture in seconds
set CAPTURE_DURATION=60
REM Set the output file names
set PCAP_FILE=C:\Users\okore\OneDrive\Desktop\tshark_capture\capture.pcap
set CSV_FILE=C:\Users\okore\OneDrive\Desktop\tshark_capture\capture.csv

REM Capture network traffic for the specified duration
echo Capturing network traffic on interface %INTERFACE_NUM% for %CAPTURE_DURATION% seconds...
tshark -i %INTERFACE_NUM% -a duration:%CAPTURE_DURATION% -w %PCAP_FILE%

REM Check if tshark command was successful
if %ERRORLEVEL% neq 0 (
    echo Tshark failed to capture packets.
    exit /b %ERRORLEVEL%
)

REM Convert the pcap file to csv format
echo Converting %PCAP_FILE% to CSV format...
tshark -r %PCAP_FILE% -T fields -e frame.time_relative -e ip.proto -e tcp.flags -e ip.len -e tcp.srcport -e tcp.dstport -e tcp.flags.reset -e tcp.flags.syn -e ip.frag_offset -e tcp.urgent_pointer -E header=y -E separator=, -E quote=d -E occurrence=f > %CSV_FILE%

REM Check if tshark command was successful
if %ERRORLEVEL% neq 0 (
    echo Tshark failed to convert pcap to csv.
    exit /b %ERRORLEVEL%
)

echo Capture and conversion completed successfully.
echo PCAP file: %PCAP_FILE%
echo CSV file: %CSV_FILE%
pause
