#!/usr/bin/python3

import argparse
import getpass
import mpd
import os.path
import random
import yaml


def sticker_songs(m, sticker, value):
    songs = []
    for song in m.sticker_find('song', '', sticker):
        if song['sticker'].split('=', 1)[1] == value:
            songs.append(song['file'])
    return songs


def add_from_playbin(m, value, songs_to_add=20):
    new_songs = sticker_songs(m, 'bin', value)
    if len(new_songs) <= songs_to_add:
        random.shuffle(new_songs)
    else:
        new_songs = random.sample(new_songs, songs_to_add)

    for song in new_songs:
        m.add(song)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="MPD playback rotation bins")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--bin-current', action='store_true', default=False,
                       help="Use the current playlist to use to fill the bin")
    group.add_argument('--bin-playlist', type=str,
                       help="Specify a saved playlist to use to fill the bin")
    group.add_argument('--num-songs', type=int, default=100,
                       help="Number of songs to add to the current playlist")
    group.add_argument('--delete-bin', action='store_true', default=False,
                       help="Delete the rotation bin")
    parser.add_argument('playbin', help="Rotation bin")
    args = parser.parse_args()

    m = mpd.MPDClient()

    try:
        import xdg.BaseDirectory
        configpath = xdg.BaseDirectory.load_first_config('mpd/config.yml')
    except:
        configpath = os.path.expanduser('~/.config/mpd/config.yml')

    config = yaml.safe_load(open(configpath))
    if 'port' in config:
        config['port'] = int(config['port'])
    else:
        config['port'] = 6600

    m.connect(config['server'], config['port'])
    if 'password' in config and len(config['password']) > 0:
        m.password(config['password'])

    if args.bin_current:
        for song in m.playlistinfo():
            m.sticker_set('song', song['file'], 'bin', args.playbin)
            print(song['file'])
    elif args.bin_playlist is not None:
        for song in m.listplaylist(args.bin_playlist):
            m.sticker_set('song', song, 'bin', args.playbin)
            print(song)
    elif args.delete_bin:
        for song in sticker_songs(m, 'bin', args.playbin):
            m.sticker_delete('song', song, 'bin')
    else:
        add_from_playbin(m, args.playbin, args.num_songs)
