## Extract subtitles from capcut draft_content.json into .srt file

import json
import os
import re
import sys

def extract_data(filename):
    with open(filename) as f:
        data = json.load(f)
    return data


def ms_to_srt(time_in_ms):
    convert_ms = time_in_ms // 1000
    ms = convert_ms % 1000
    total_seconds = (convert_ms - ms) // 1000
    seconds = total_seconds % 60
    total_minutes = total_seconds // 60
    minutes = total_minutes % 60
    hours = (total_minutes - minutes) // 60
    return f"{str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)},{ms}"


def write_to_file(data, filename):
    print('Saving subtitles to file...')
    with open(filename, 'w') as f:
        f.write(data)
    print('Done!')

file = "draft_content.json"

data = extract_data(file)
materials, tracks = data['materials'], data['tracks']

sub_track_number = 1
sub_timing = tracks[sub_track_number]['segments']

subtitles_info = [{'content': re.sub(r'<.*?>|\[|\]', '', i['content']), 'id': i['id']} for i in materials['texts']]

for i, s in enumerate(subtitles_info):
    segment = next((seg for seg in sub_timing if seg['material_id'] == s['id']), None)
    while not segment:
        sub_track_number += 1
        sub_timing = tracks[sub_track_number]['segments']
        segment = next((seg for seg in sub_timing if seg['material_id'] == s['id']), None)
    
    s['start'] = segment['target_timerange']['start']
    s['end'] = s['start'] + segment['target_timerange']['duration']
    s['srtStart'] = ms_to_srt(s['start'])
    s['srtEnd'] = ms_to_srt(s['end'])
    s['subNumber'] = i + 1
    s['srtTiming'] = f"{s['srtStart']} --> {s['srtEnd']}"

srt_out = '\n'.join([f"{i['subNumber']}\n{i['srtTiming']}\n{i['content']}\n" for i in subtitles_info])
copy_out = '\n'.join([f"{i['content']}" for i in subtitles_info])


write_to_file(copy_out, 'copy.txt')
write_to_file(srt_out, 'subtitles.srt')
        
