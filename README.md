# automate_WPA2_audit
Intent of create and automate process for WPA2/PSK Wifi Audit

The process have 2 steps:

- STEP 1: Generate Handshake with 3 strategies to capture (Deauthentication, Fake authentication & WPA Migration Mode). 
This step is exampled in case of use in archive WPA2-PSK_Operate.txt; this must to be automate with FSM scheme to involve this step in a group of possible situations in order to reduce the time of generate Handshake to make the attack more undetectable because the time is reduced to minimal time.

- STEP 2: Matching Handshake with dictionary in some crypto strategy (in the worst case SHA256) with aircrack-ng command.
This step generates a block of threads massive in with the dictionary more extensive for Latin (weakpass_4a.latin.txt) take one week or more. For this reason I proceed to understand how aircrack-ng process match handshake with worlist registry. The idea is reduce the time of process document all aircrack-ng package in C++ and modify this to matching with a Database in postgre SQL locally stored.
To make this possible create 3 python scripts to analyze in 3 levels all package (running with ollama interface and qwen2.5-coder:7b model):

-- LEVEL FUNCTIONAL: 
analizar_proyecto_cpp.py
This process analize each module to describe this components, dependencies and identified problems.
-- LEVEL INTERDEPENDECIES:
documentar_interdependencias.py
This process analyze based in the document previous functional and create graphical indications that give us graphical references for each command or process to focus in one of the process in C++ to identify how process works.
-- LEVEL PROCESS LOW LEVEL:
describir_procesos.py
This process analyze each block of package in particular to describe how it works low level to understand possible upgrades.

The probes of this process are in folder proyecto_cpp_doc to references the advances of this analysis. 

In parallel I create a database of 1 table indexed with the Word-list weakpass_4a.latin.txt with a process in C++. 

This process have referenced with:

- scripts_WL_DB.sh (in process)
- WL-V1.7 project (partially created).


