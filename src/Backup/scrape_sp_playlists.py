def scrape_sp_playlists(sp, qchars, write=True):
    chars = list('abcdefghijklmnopqrstuvwxyz1234567890')
    dead_char = []
    output = []
    for char in qchars:
        query_chars = zip(len(chars) * char, chars)
        for query_char in query_chars:
            query = ''.join(query_char)
            playlists = search_playlists(sp, query, write)
            if playlists is None:
                dead_char.append(query)
            elif not write:
                output += playlists
    if write:
        return scrape_sp_playlists(sp, dead_char, write)
    else:
        print dead_char
        return output
