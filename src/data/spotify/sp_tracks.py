def get_audio_features(sp, track_ids):
    """ Get audio features """
    total_tracks = len(track_ids)
    offset = 0
    limit = 50

    scrolled_tracks = sp.audio_features(track_ids[offset:limit])

    total_scrolled_tracks = len(scrolled_tracks)
    res = scrolled_tracks

    while total_scrolled_tracks < total_tracks:
        offset += 50
        limit = offset + 50
        scrolled_tracks = sp.audio_features(track_ids[offset:limit])
        total_scrolled_tracks += len(scrolled_tracks)
        res.extend(scrolled_tracks)

    return res
