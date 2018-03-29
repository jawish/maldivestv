# -*- coding: utf-8 -*-
# Module: default
# Author: Jawish Hameed
# Created on: 30.03.2018

import sys
from urllib import urlencode
from urlparse import parse_qsl
import xbmcgui
import xbmcplugin

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

VIDEOS = [ 
    {'name': 'TVM',
    'thumb': 'http://play.mv/stb/item/tvlive1/198.png',
    'video': 'http://feed.play.mv/live/1000/10001/master.m3u8'},
    {'name': 'RaajjeTV',
    'thumb': 'http://play.mv/stb/item/tv_live1/199.png',
    'video': 'http://feed.play.mv/live/1000/10005/master.m3u8'},
    {'name': 'Channel 13 HD',
    'thumb': 'http://play.mv/stb/item/tv_live1/200.png',
    'video': 'http://feed.play.mv/live/1000/10003/master.m3u8'},
    {'name': 'Munnaaru',
    'thumb': 'http://play.mv/stb/item/tvlive1/201.png',
    'video': 'http://feed.play.mv/live/1002/10026/master.m3u8'},
    {'name': 'VTV',
    'thumb': 'http://play.mv/stb/item/tv_live1/202.png',
    'video': 'http://feed.play.mv/live/1000/10006/master.m3u8'},
    {'name': 'YES',
    'thumb': 'http://play.mv/stb/item/tv_live1/203.png',
    'video': 'http://feed.play.mv/live/1000/10002/master.m3u8'},
    {'name': 'MVtv HD',
    'thumb': 'http://play.mv/stb/item/tvlive1/204.png',
    'video': 'http://feed.play.mv/live/1006/10065/master.m3u8'},
    {'name': 'SanguTV HD',
    'thumb': 'http://play.mv/stb/item/tv_live1/213.png',
    'video': 'http://feed.play.mv/live/1001/10012/master.m3u8'},
    {'name': 'SunTV',
    'thumb': 'http://play.mv/stb/item/tvlive1/233.png',
    'video': 'http://feed.play.mv/live/1001/10017/master.m3u8'},
    {'name': 'GO Plus HD',
    'thumb': 'http://play.mv/stb/item/tvlive1/344.png',
    'video': 'http://feed.play.mv/live/1007/10079/master.m3u8'},
    {'name': 'PSM News HD',
    'thumb': 'http://play.mv/stb/item/tvlive1/352.png',
    'video': 'http://feed.play.mv/live/1006/10066/master.m3u8'},
    {'name': 'Al Kaun HD',
    'thumb': 'http://play.mv/stb/item/tvlive1/355.png',
    'video': 'http://feed.play.mv/live/1005/10053/master.m3u8'}
]


def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :type kwargs: dict
    :return: plugin call URL
    :rtype: str
    """
    return '{0}?{1}'.format(_url, urlencode(kwargs))


def get_videos():
    """
    Get the list of videofiles/streams.

    :return: the list of videos
    :rtype: list
    """
    return VIDEOS


def list_videos():
    """
    Create the list of playable videos in the Kodi interface.
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_handle, 'Channels')
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_handle, 'videos')
    # Get the list of videos.
    videos = get_videos()
    # Iterate through videos.
    for video in videos:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=video['name'])
        # Set additional info for the list item.
        # 'mediatype' is needed for skin to display info for this ListItem correctly.
        list_item.setInfo('video', {'title': video['name'],
                                    'genre': 'live',
                                    'mediatype': 'video'})
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb'], 'fanart': video['thumb']})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/wp-content/uploads/2017/04/crab.mp4
        url = get_url(action='play', video=video['video'])
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def play_video(path):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'play':
            # Play a video from a provided URL.
            play_video(params['video'])
        else:
            # If the provided paramstring does not contain a supported action
            # we raise an exception. This helps to catch coding errors,
            # e.g. typos in action names.
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of videos
        list_videos()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
