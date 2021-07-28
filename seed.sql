insert into artist(id, name, role) values(1, 'Singer Sam', 'SINGER');
insert into artist(id, name, role) values(2, 'Bassist Bob', 'BASSIST');
insert into artist(id, name, role) values(3, 'Drummer Don', 'DRUMMER');
insert into artist(id, name, role) values(4, 'Singer Simpson', 'SINGER');

insert into track(isrc, title, version, explicit, audio_file) values('TEST000000001', 'Test Track 01', 'RADIO', true, 'music1.mp3');
insert into track(isrc, title, version, explicit, audio_file) values('TEST000000002', 'Test Track 02', 'ORIGINAL', true, 'music2.mp3');
insert into track(isrc, title, version, explicit, audio_file) values('TEST000000003', 'Test Track 03', 'ORIGINAL', false, 'music3.mp3');

insert into album(upc, title, artwork_file, release_date, stores) values('00000000000001', 'Test Album1', 'album1.jpg', '2020-03-01', '{"APPLE", "YOUTUBE", "SPOTIFY"}');
insert into album(upc, title, artwork_file, release_date, stores) values('00000000000002', 'Test Album2', 'album2.jpg', '1985-05-15', '{"YOUTUBE", "SPOTIFY"}');
insert into album(upc, title, artwork_file, release_date, stores) values('00000000000003', 'Test Album3', 'album3.jpg', '1993-09-10', '{"APPLE", "SPOTIFY"}');

insert into album_track(album, track) values('00000000000001', 'TEST000000001');
insert into album_track(album, track) values('00000000000001', 'TEST000000003');
insert into album_track(album, track) values('00000000000002', 'TEST000000002');
insert into album_track(album, track) values('00000000000003', 'TEST000000001');
insert into album_track(album, track) values('00000000000003', 'TEST000000002');
insert into album_track(album, track) values('00000000000003', 'TEST000000003');

insert into track_artist(track, artist) values('TEST000000001', 1);
insert into track_artist(track, artist) values('TEST000000002', 2);
insert into track_artist(track, artist) values('TEST000000002', 3);
insert into track_artist(track, artist) values('TEST000000003', 2);
insert into track_artist(track, artist) values('TEST000000003', 4);
