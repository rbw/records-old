insert into artist(id, role, name) values(1, 'primary_artist', 'primary1');
insert into artist(id, role, name) values(2, 'primary_artist', 'primary2');
insert into artist(id, role, name) values(3, 'secondary_artist', 'secondary1');
insert into artist(id, role, name) values(4, 'secondary_artist', 'secondary2');

insert into track(isrc, title, version, explicit, audio_file) values('TEST000000001', 'Test Track 01', 'radio', true, 'music1.mp3');
insert into track(isrc, title, version, explicit, audio_file) values('TEST000000002', 'Test Track 02', 'original', true, 'music2.mp3');
insert into track(isrc, title, version, explicit, audio_file) values('TEST000000003', 'Test Track 03', 'original', false, 'music3.mp3');

insert into album(upc, title, artwork_file, release_date, stores) values('00000000000001', 'Test Album1', 'album1.jpg', '2020-03-01', '{"apple", "youtube", "spotify"}');
insert into album(upc, title, artwork_file, release_date, stores) values('00000000000002', 'Test Album2', 'album2.jpg', '1985-05-15', '{"youtube", "spotify"}');
insert into album(upc, title, artwork_file, release_date, stores) values('00000000000003', 'Test Album3', 'album3.jpg', '1993-09-10', '{"apple"}');

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
