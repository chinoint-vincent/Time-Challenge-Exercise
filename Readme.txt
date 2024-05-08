Requirements:
1. C++17  
2. audio capture from laptop microphone
3. stream over websocket
4. JSON response log

IP address: 3.25.140.218
Port: 8765

Choose of language: Python 3.x
Advantage: Python is intrinsically a combination of C and C++, and is C++11 by default
dependency: 
1. python-logstash-async (pip install python-logstash-async)
2. jupyterlab (pip install jupyterlab)

Solution Overview:
A Python-based system for real-time audio streaming from a microphone on one machine to another over WebSockets, enabling applications like remote monitoring and broadcasting. 
This app supports multiple clients. 
The system will get the microphone enumerated as #0 in the system.
Log is in JSON format, simple with text and timestamp. ( more attributes can be added by using .info() )
Error handling is not sophisticated yet, still need more try / catch to make it production code.


