import sqlite3
import os

application_path = os.path.dirname(__file__)
#dbFilePath = os.path.join(application_path, 'Ariel-Final-REDUCED-5_MILLION_MATCHES.db')
dbFilePath = os.path.join(application_path, 'ariel_final.db')
_conn = sqlite3.connect(dbFilePath, check_same_thread=False)
_conn.row_factory = sqlite3.Row
_cursor = _conn.cursor()

class ShakespeareModel:
    def __init__(self):
        pass

    @classmethod
    def get_matchedlines_by_lineids(cls, seed1, seed2):
        rows = _cursor.execute(
            'SELECT source_line_id, target_line_id from lines_and_docs_matches WHERE (source_line_id>=? and source_line_id<=? ) OR (target_line_id>=? and target_line_id<=?)', (seed1, seed2, seed1, seed2)
            )
        return [{'sid': r['source_line_id'], 'tid': r['target_line_id']} for r in rows]

    @classmethod
    def get_lines_by_lineids(cls, seed1, seed2):
        rows = _cursor.execute(
            'SELECT line_id, line_text, play, ftln, line from lines where (line_id>=? and line_id<=? )', (seed1,seed2, )
            )
        #for (r in rows):
        #    act = r['line'].split(".")[1]
        #    scene = r['line'].split(".")[1]
        #    play = r['play']
        #    break
        return [{'line_id': r['line_id'], 'line_text': r['line_text'], 'play': r['play'], 'ftln': r['ftln'], 'act': r['line'].split(".")[1], 'scene': r['line'].split(".")[2]} for r in rows]
        #return ['play': play,'act': act,'scene':scene,[{'line_id': r['line_id'], 'line_text': r['line_text'],  'ftln': r['ftln']} for r in rows]]

    @classmethod
    def get_matchedlines_by_lineids_interplay(cls, seed1, seed2, play1, play2):
        rows = _cursor.execute(
            'SELECT source_line_id, target_line_id from lines_and_docs_matches WHERE (source_line_id>=? and source_line_id<=? and not (target_line_id<=? and target_line_id>=?)) OR (target_line_id>=? and target_line_id<=? and not (source_line_id<=? and source_line_id>=? ))', (seed1, seed2, play2, play1, seed1, seed2, play2, play1)
            )
        return [{'sid': r['source_line_id'], 'tid': r['target_line_id']} for r in rows]

    @classmethod
    def get_play_num(cls, play):
        rows = _cursor.execute(
            'SELECT startline_id, endline_id from play_boundary WHERE play = ?', (play, )
            )
        return [{'play1': r['startline_id'], 'play2': r['endline_id']} for r in rows]

    @classmethod
    def get_playlist(cls):
        rows = _cursor.execute(
            'SELECT play from play_boundary'
            )

        return [{'play': r['play']} for r in rows]

    @classmethod
    def get_actscenelist(cls, play):
        rows = _cursor.execute(
            "SELECT line from lines where line like '%?%'", (play, )
            )

        return [{'act': r['line'].split(".")[1], 'scene': r['line'].split(".")[2]} for r in rows]
