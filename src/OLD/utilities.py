

def extractPlaylists(user_playlists):
    """
    Extract PID & UID
    """
    playlists = []
    i_max = len(user_playlists)
    for i in range(0, i_max):
        playlists.append((user_playlists[i]['id'], user_playlists[i][
                         'owner']['id'], user_playlists[i]['name']))
    return playlists


def extractTrackTrack(track, pid, pname):
    """
    # Exctract TID from Track
    Extract artists from a track
    Return : List of artist containing in the track
    """
    # Return
    piste = []
    # Function
    if track['track']:
        piste.append(
            (pid,
             pname,
             track['track']['id'])
        )
    else:
        pass
    # Retrun
    return piste


def extractTrackPlaylist((pid, uid, pname)):
    """
    # Extract tid from Playlist
    Extract artist from a playlist
    Return : List of artist containing in the playlist
    """
    # Return
    piste = []
    # Parameters
    cond = True
    tracks = sp.user_playlist_tracks(
        uid, pid, fields=None, limit=100, offset=0)
    while cond:
        i_max = len(tracks['items'])
        for i in range(0, i_max):
            piste += extractTrackTrack(tracks['items'][i], pid, pname)
        if tracks['next']:
            tracks = sp.next(tracks)
        else:
            cond = False
    # Return
    return piste


def extractAudioFeature(tracks):
    result = []
    tid = tracks[2]
    res = sp.audio_features([tid])[0]
    del res['track_href']
    del res['analysis_url']
    del res['uri']
    del res['type']
    del res['id']
    tmp = [tracks[1]] + list(res.values())
    result.append(tmp)
    return result
