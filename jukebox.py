#!/bin/env python
"""
Requirements:
    - pip install python-requests
    - pip install youtube-dl
    - download ffmpeg from http://ffmpeg.zeranoe.com/builds/
"""
import os
import requests
import youtube_dl


class JukeBoxApi(object):
    def __init__(self):
        self.s = requests.session()
        self.playlists = {}
        
        self.login()
        self.get_playlist()
        
    def login(self, username=None, password=None):
        if username is None:
            print("Enter username: ")
            username = raw_input().strip()
        if password is None:
            print("Enter password: ")
            password = raw_input().strip()
            
        print("Logging in to http://jukebox.today ...")
        req = self.s.post("http://jukebox.today/api/login_check", 
            {'_username': username, '_password': password})
        print(req)
        
    def get_playlist(self):
        req = self.s.get("http://jukebox.today/api/api/playlists")
        playlists = req.json()
        for p in playlists:
            self.playlists[p['name']] = p
        
    def download_playlist(self, name="Daily", base_directory='.'):
        if name not in self.playlists:
            print(u"Unknown playlist %s" % name)
            return
        directory_path = os.path.abspath(os.path.join(base_directory, name))
        
        playlist = self.playlists[name]
        for song in self.playlists[name]['songs']:
            do_download = True
            existing_file_list = os.listdir(u"%s" % directory_path)
            for f in existing_file_list:
                if (song['slug'] in f) and ("mp3" in f):
                    do_download = False
            if not do_download: 
                print(u"Skipping", song['title'], song['slug'])
                continue
            print(u"Downloading ...", song['title'], song['slug'])
            self.download_url("http://youtu.be/%s" % song['slug'], directory_path=directory_path)
        
    def download_url(self, url, directory_path='.', filename=None):
        ydl_opts = {
            'format': 'bestaudio/best',
            'ffmpeg_location': 'C:\\Users\\steph\\progz\\ffmpeg\\bin',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': unicode(os.path.join(directory_path, '%(title)s-%(id)s.%(ext)s'))
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        
if __name__ == "__main__":
    jb = JukeBoxApi()
    jb.download_playlist()
    
