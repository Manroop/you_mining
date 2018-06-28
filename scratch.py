

from __future__ import division, print_function, absolute_import
from pydub import AudioSegment
import numpy as np
import os
from webvtt import WebVTT
import glob
from pandas import DataFrame

Search = 'hello'

#    READING FILE CONTENT
path = "/home/mst/Documents/Youtube/March_03/Vtt/*"
files = glob.glob(path)       #Reading whole Directory
start_time = []
end_time = []
sub_file_name = []
for i in range(len(files)):
    #print (files[i])    # Display the File name being read
    sub_file = open(files[i], "r")
    lines = sub_file.readlines() # reading lines of sub file line by line
                                 #  Therefore, it is possible to iteretate
                                 #  and search strings of interest
#print (lines[5])
    #print (len(lines)) # number of lines in a file

#     Step 1: Loop through each line to search Keyword of choice
#     Step 2: Extract Time stamp of each matched Keyword
#     Step 3: Write the Time Stamp with Two Columns: Start Time and End Time,
#     Step 4: Also, write Keyword to a same excel file
    for l in range(len(lines)):
        if Search in lines[l]:
            print ("Keyword Found.......\n----->>Shifting marker to previous line<<------")
            #print (lines[l])

            if "-->" in lines[l-1]:
                print ("Time STamp Found")
                print (lines[l])
                start_time.append(lines[l-1][0:11])
                end_time.append(lines[l-1][16:28])
                sub_file_name.append(files[i])
            else:
                if "-->" in lines[l-2]:
                    print ("Time STamp Found")
                    print (lines[l-2])
                    start_time.append(lines[l-2][0:11])
                    end_time.append(lines[l-2][16:28])
                    sub_file_name.append(files[i])



df = DataFrame({'Start Time': start_time, 'End Time': end_time,  'Sub_File Name': sub_file_name, 'Caption': Search})
print (df)
df.to_excel('/home/mst/Documents/Youtube/March_03/Time_Stamp_Data.xlsx', sheet_name='sheet1', index=False)
#df = DataFrame({'Time Stamp': l1})
#print (df)




# Slice Stings and Add Audio FIle Name for processing
audio_path = "/home/mst/Documents/Youtube/March_03/Audio_Files/*"
audio_files = glob.glob(audio_path)
start_hr = []
start_min = []
start_sec = []
start_ms = []
end_hr = []
end_min = []
end_sec = []
end_ms = []
audio_vip = []
caption = []
st_t = []
ed_t = []

for i in range(len(audio_files)):
    for j,k,l in zip(range(len(start_time)), range(len(end_time)), range(len(sub_file_name))):
        sub_audio_match =  audio_files[i][50:59]
        if sub_audio_match in sub_file_name[l][42:52]:
            audio_vip.append(audio_files[i])
            start_hr.append(int(start_time[j][0:2]))
            start_min.append(int(start_time[j][3:5]))
            start_sec.append(int(start_time[j][6:8]))
            start_ms.append(int(start_time[j][9:11]))
            end_hr.append(int(end_time[k][1:3]))
            end_min.append(int(end_time[k][4:6]))
            end_sec.append(int(end_time[k][7:9]))
            end_ms.append(int(end_time[k][10:12]))
            caption.append(Search)
            st_t.append(start_time[j])
            ed_t.append(end_time[k])


print (len(audio_vip))
print (len(sub_file_name))
print (len(start_min))
print (len(end_min))
print (sub_file_name[0][41:60])
print (audio_vip[0])
#print (audio_vip[0][49:69])

final_frame = DataFrame({'Start Hour': start_hr, 'Start Min': start_min, 'Start Sec': start_sec,
                        'Start Mili Sec': start_ms, 'End Hour': end_hr, 'Start Time': st_t, 'End Min': end_min,
                        'End Sec': end_sec, 'End Mili Sec': end_ms, 'End Time': ed_t,
                        'Audio File': audio_vip, 'Caption': caption})
print (final_frame)
final_frame.to_excel('/home/mst/Documents/Youtube/March_03/DOI.xlsx', sheet_name='sheet1', index=False)




# Clipping Audio
begin_time = []
finish_time = []
for i,j,k,l,m  in zip(range(len(audio_vip)),range(len(start_min)), range(len(start_sec)), range(len(end_min)), range(len(end_sec))):
    begin_time.append(start_min[j]*60*1000 + start_sec[k] * 1000)
    finish_time.append(end_min[l]*60*1000 + end_sec[m] * 1000)
    print (type(begin_time[0]))
    for o,p in zip(range(len(begin_time)), range(len(finish_time))):
        sound = AudioSegment.from_file(audio_vip[i], 'm4a')
        extract = sound[begin_time[o]:finish_time[p]]
        extract.export( audio_vip[i] +'-extract.mp3', format="mp3")
