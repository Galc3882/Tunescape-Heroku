import numpy as np
import cv2
import numpy as np
import math
import numba as nb
import numpy as np


same_mode = (1, 0.1667, 0.3333, 0.5, 0.6667, 0.8333, 0, 0.8333, 0.6667, 0.5, 0.3333, 0.16667)
min_maj = (0.4286, 0.5714, 0.1429, 0.8571, 0.1429, 0.5714, 0.4286, 0.2857, 0.7143, 0, 0.7143, 0.2857)
maj_min = (0.4286, 0.2857, 0.7143, 0, 0.7143, 0.2857, 0.4286, 0.5714, 0.1429, 0.8571, 0.1429, 0.5714)

def equalizeDim(l1, l2):
    '''
    This function takes two lists and adds zeros where the value of the bigger list is smaller
    than the value of the smaller list. It returns the two lists with the same length.
    '''
    if l1 == []:
        return [0]*len(l2), l2
    elif l2 == []:
        return l1, [0]*len(l1)
    if len(l1) > len(l2):
        i = 0
        while len(l1) != len(l2):
            if l1[i] < l2[i]:
                l2.insert(i, 0)
                i += 1
            else:
                i += 1
                
            if i == len(l2):
                l2 = l2 + [0]*(len(l1)-len(l2))
                break
    elif len(l2) > len(l1):
        i = 0
        while len(l2) != len(l1):
            if l2[i] < l1[i]:
                l1.insert(i, 0)
                i += 1
            else:
                i += 1
            
            if i == len(l1):
                l1 = l1 + [0]*(len(l2)-len(l1))
                break
    return l1, l2


@nb.jit(nopython=True, fastmath=True)
def nb_cosine(x, y):
    xx,yy,xy=0.0,0.0,0.0
    for i in range(len(x)):
        xx+=x[i]*x[i]
        yy+=y[i]*y[i]
        xy+=x[i]*y[i]
    if xx*yy == 0:
        return 0
    return xy/np.sqrt(xx*yy)
        
def key(key1, key2, mode1, mode2):
    '''
    This function takes two keys and returns the similarity between them.
    '''
    # relation: linear, circle of fiths
    # assume mode difference is the same as being off by a sharp/flat

    if mode1 == mode2:
        return same_mode[key2 - key1]
    elif mode1 == 0 and mode2 == 1:
        return min_maj[key2 - key1]
    else:
        return maj_min[key1 - key2]


def tempo(tempo1, tempo2):
    '''
    This function takes two tempos and returns the similarity between them.
    '''
    if tempo1 == tempo2:
        return 1
    # sigmoid
    return 1 / (1 + math.exp(-7*(max(1-0.05*abs(float(tempo1) - float(tempo2)), 0)-0.5)))


def loudness(loudness1, loudness2):
    '''
    This function takes two loudnesses and returns the similarity between them.
    '''
    return max(1-0.1*abs(loudness1 - loudness2), 0)


def time_signature(time_signature1, time_signature2):
    '''
    This function takes two time signatures and returns the similarity between them.
    '''
    if time_signature1 == time_signature2:
        return 1
    else:
        return 0


def year(year1, year2):
    '''
    This function takes two years and returns the similarity between them.
    '''
    if year1 == 0 or year2 == 0:
        return None
    return max(1-0.1*abs(int(year1) - int(year2)), 0)


def duration(duration1, duration2):
    '''
    This function takes two durations and returns the similarity between them.
    '''
    return max(1-0.02*abs(duration1 - duration2), 0)


def mode(mode1, mode2):
    '''
    This function takes two modes and returns the similarity between them.
    '''
    if mode1 == mode2:
        return 1
    else:
        return 0


def sections_start(sections_start1, sections_start2):
    '''
    This function takes two sections starts and returns the similarity between them.
    '''
    if len(sections_start1) > len(sections_start2):
        sections_start1 = np.resize(sections_start1, len(sections_start2))
    elif len(sections_start2) > len(sections_start1):
        sections_start2 = np.resize(sections_start2, len(sections_start1))

    return nb_cosine(sections_start1, sections_start2)


def segments_pitches(segments_pitches1, segments_pitches2):
    '''
    This function takes two segments pitches and returns the similarity between them.
    '''
    # reshape matricies to smallest one
    if len(segments_pitches1) > len(segments_pitches2):
        segments_pitches1 = cv2.resize(segments_pitches1, dsize=(12, len(segments_pitches2)), interpolation=cv2.INTER_NEAREST)
    elif len(segments_pitches2) > len(segments_pitches1):
        segments_pitches2 = cv2.resize(segments_pitches2, dsize=(12, len(segments_pitches1)), interpolation=cv2.INTER_NEAREST)

    # return euclidean distance between the two matrices to sigmoid
    return 1 / (1 + math.exp(-5*(max(1-0.01*np.linalg.norm(segments_pitches1-segments_pitches2), 0)-0.5)))


def segments_timbre(segments_timbre1, segments_timbre2):
    '''
    This function takes two segments timbre and returns the similarity between them.
    '''
    # reshape matricies to smallest one 
    if len(segments_timbre1) > len(segments_timbre2):
        segments_timbre1 = cv2.resize(segments_timbre1, dsize=(12, len(segments_timbre2)), interpolation=cv2.INTER_NEAREST)
    elif len(segments_timbre2) > len(segments_timbre1):
        segments_timbre2 = cv2.resize(segments_timbre2, dsize=(12, len(segments_timbre1)), interpolation=cv2.INTER_NEAREST)

    # return euclidean distance between the two matrices to sigmoid
    return 1 / (1 + math.exp(-5*(max(1-0.01*np.linalg.norm(segments_timbre1-segments_timbre2), 0)-0.5)))


def bars_start(bars_start1, bars_start2):
    '''
    This function takes two bars starts and returns the similarity between them.
    '''
    if len(bars_start1) > len(bars_start2):
        bars_start1 = np.resize(bars_start1, len(bars_start2))
    elif len(bars_start2) > len(bars_start1):
        bars_start2 = np.resize(bars_start2, len(bars_start1))

    return nb_cosine(bars_start1, bars_start2)


def tatums_start(tatums_start1, tatums_start2):
    '''
    This function takes two tatums starts and returns the similarity between them.
    '''
    if len(tatums_start1) > len(tatums_start2):
        tatums_start1 = np.resize(tatums_start1, len(tatums_start2))
    elif len(tatums_start2) > len(tatums_start1):
        tatums_start2 = np.resize(tatums_start2, len(tatums_start1))
    
    return nb_cosine(tatums_start1, tatums_start2)

def beats_start(beats_start1, beats_start2):
    '''
    This function takes two beats starts and returns the similarity between them.
    '''
    if len(beats_start1) > len(beats_start2):
        beats_start1 = np.resize(beats_start1, len(beats_start2))
    elif len(beats_start2) > len(beats_start1):
        beats_start2 = np.resize(beats_start2, len(beats_start1))
    
    return nb_cosine(beats_start1, beats_start2)

def artist_name(artist_name1, artist_name2):
    '''
    This function takes two artist names and returns the similarity between them.
    '''
    if artist_name1 == artist_name2:
        return 1
    else:
        return 0


# A dictionary of the similarity functions
methodDictionary = {1: artist_name, 2: duration, 3: key, 5: tempo, 6: loudness, 7: time_signature, 8: year,
                    9: sections_start, 10: segments_pitches, 11: segments_timbre, 12: bars_start,
                    13: beats_start, 14: tatums_start}

# ('get_title', 'get_artist_name', 'get_duration', 'get_key',
#   0               1                 2                 3
#  'get_mode', 'get_tempo', 'get_loudness', 'get_time_signature',
#   4               5                 6                 7 
#  'get_year', 'get_sections_start', 'get_segments_pitches', 
#   8               9                 10                
#  'get_segments_timbre', 'get_bars_start', 'get_beats_start',
#   11                                12                13
#  'get_tatums_start')
#   14