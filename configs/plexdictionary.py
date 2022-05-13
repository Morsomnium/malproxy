# Plex anime library name
anime_folder = 'Anime'

# Plex events
event = 'event'

# Media events
pause = 'media.pause'  # – Media playback pauses.
play = 'media.play'  # – Media starts playing. An appropriate poster is attached.
rate = 'media.rate'  # – Media is rated. A poster is also attached to this event.
resume = 'media.resume'  # – Media playback resumes.
scrobble = 'media.scrobble'  # – Media is viewed (played past the 90% mark).
stop = 'media.stop'  # – Media playback stops.

# Content
# A new item is added that appears in the user’s On Deck. A poster is also attached to this event.
new_on_deck = 'library.on.deck'
# A new item is added to a library to which the user has access. A poster is also attached to this event.
new_media = 'library.new'

# Server Stuff
# A database backup is completed successfully via Scheduled Tasks.
db_backup = 'admin.database.backup'
# Corruption is detected in the server database.
corruption = 'admin.database.corrupted'
# A device accesses the owner’s server for any reason,
# which may come from background connection testing and doesn’t necessarily indicate active browsing or playback.
new_device = 'device.new'
# Playback is started by a shared user for the server. A poster is also attached to this event.
share_start = 'playback.started'
