#from flask import request, jsonify, render_template
from .shakespeareModel import ShakespeareModel

import time

class ShakespeareMatches(ShakespeareModel):

    ##########################################
    # make a copy before remove the key ???? not used yet .....
    ##########################################
    def removekey(d, key):
        r = dict(d)
        del r[key]
        return r

    def __init__(self):
        pass

    def __new__(cls, line_id, line_number, block_number, inter_play):


        numlines = line_number  # number of lines we want to display and search on
        range = numlines - 1
        count = 0
        sline_ids = ''

        seed1 = line_id
        seed2 = line_id + range
        play1 = 0
        play2 = 0

        ##print (seed1, seed2)
        start1 = time.time()

        sourceLines = ShakespeareModel.get_lines_by_lineids(seed1, seed2)

        # check if all lines are from the same play
        sameplay = True
        play = ""
        for s in sourceLines:
            if (play == ""):
                play = s['play']
            elif play != s['play']:
                sameplay = False
                break

        if not sameplay:
            # change lines to lower number
            seed1 = line_id - range
            seed2 = line_id

        end1 = time.time()
        print ("Part1 timing - ", end1 - start1)

        start2 = time.time()
        matchedLines = ShakespeareModel.get_matchedlines_by_lineids(seed1, seed2)
        end2 = time.time()
        print ("Part2 timing - ", end2 - start2)

        start2 = time.time()
        #print(matchedLines)
        idcounts = dict()
        # go through each source_line_id and target_line_id, remove the id in sline_ids, and count
        for m in matchedLines:
            # count the matches number
            tid = int(m['tid'])
            sid = int(m['sid'])
            if (inter_play):
                # only match between plays
                playlines = ShakespeareModel.get_play_num(play)

                # get the startline_id and endline_id of the play
                for p in playlines:
                    play1 = p['play1']
                    play2 = p['play2']
                    break
                if not (tid >= play1 and tid <= play2):
                    if (tid not in idcounts):
                        idcounts[tid] = 1
                    else:
                        idcounts[tid] =  idcounts[tid] + 1

                    if not (sid >= play1 and sid <= play2):
                        if (sid not in idcounts):
                            idcounts[sid] = 1
                        else:
                            idcounts[sid] =  idcounts[sid] + 1
            else:
                # match all
                if not (tid >= seed1 and tid <= seed2):
                    if (tid not in idcounts):
                        idcounts[tid] = 1
                    else:
                        idcounts[tid] =  idcounts[tid] + 1

                if not (sid >= seed1 and sid <= seed2):
                    if (sid not in idcounts):
                        idcounts[sid] = 1
                    else:
                        idcounts[sid] =  idcounts[sid] + 1

        end2 = time.time()
        print ("Part3 timing - ", end2 - start2)


        # check the idCounts with most matches
        # sort by values to get the maxscore so far
        maxscore = 0
        minblockscore = 0

        start_id = 0
        group = dict()
        score = 0

        groups = []
        scores = dict()
        maxgroup = dict()
        maxgroups = []
        maxscores = []
        groupcount = 0
        #print (sorted(idcounts.keys()))
        # order the keys (idcounts) ascending

        start3 = time.time()

        for id in sorted(idcounts.keys()):
            ##print ("start ID: ", start_id)
            score = idcounts[id]
            ##print("ID = ", id, "Score = ", score)
            if (start_id == 0):
                # very first, start a group
                start_id = id
                group[id] = score
                totalscore = score
                ##print ("GROUP: ", group, "Total Score: ", totalscore, "MAXscore: ", maxscore)
            elif ((id - start_id) <= range):
                # within range, add the id to the group
                group[id] = score
                totalscore = totalscore + score
                ##print ("GROUP: ", group, "Total Score: ", totalscore)
            else:
                # id out of range of current group, finish up group and check the score
                ##if (maxscore < totalscore):
                ##    print ("Hi, I found a new max group here!!!!!!!!!!!!!!!!!!!!")
                ##    maxgroup = {**group}
                ##    maxscore = totalscore

                # copy the group and append it to the end of groups
                groups.append(group.copy())
                scores[groupcount] = totalscore
                groupcount = groupcount + 1
                #start another round of check, order the group and check each group member
                ##print ("GROUP: ", group)
                ##print ("MAXGROUP: ", maxgroup)

                # if the length of the group is 1, clear the group and start new
                for gid in sorted(group.keys()):
                    if ((id - gid) > range ):
                        # remove gid from group
                        ##print("deleting: ", gid)
                        totalscore = totalscore - group[gid]
                        del group[gid]

                    else:
                        # form a new group
                        start_id = gid
                        group[id] = score
                        totalscore = totalscore + score
                        break

                # now we need to know if we already have a group
                # print("Do we have a new group with this totalscore:", totalscore)
                if (totalscore == 0):
                    # no group yet, use this id to form a new group
                    start_id = id
                    group[id] = score
                    totalscore = score

            #if (count>10):
            #    break


        ##if (maxscore < totalscore):
        ##    maxgroup = group.copy()
        ##    maxscore = totalscore

        ##print ("MaxGROUP: ", maxgroup, "Maxscore: ", maxscore)
        # sort the scores and put the first block_number of largest groups in maxgroups
        count = 0
        resultLines = []
        ##print (scores)
        for n in sorted(scores, key=scores.get):
            #maxgroups[count] = groups[n]
            #maxscores[count] = scores[n]
            max1 = 0
            max2 = 0
            for max1 in sorted(groups[n].keys()):
                max2 = max1 + range
                break
            resultLines.append(ShakespeareModel.get_lines_by_lineids(max1, max2))
            count = count + 1
            if (count >= block_number):
                break

        seedLines = ShakespeareModel.get_lines_by_lineids(seed1, seed2)

        end3 = time.time()
        print ("End timing: ", end3 - start3)
        return (seedLines,resultLines)
        #return ({'seedlines': seedLines, 'resultlines': resultLines})
