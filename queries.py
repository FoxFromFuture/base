my_music_query = """
CREATE TABLE my_music(
mus_id BIGSERIAL NOT NULL PRIMARY KEY,
user_id INTEGER REFERENCES iuser(user_id),
track_id INTEGER REFERENCES track_list(track_id)
);

CREATE OR REPLACE FUNCTION mymus_count_trigger_func()
RETURNS TRIGGER
AS $$
BEGIN
	UPDATE iuser
	SET my_tracks_count = my_tracks_count + 1
	WHERE iuser.user_id =
	(SELECT user_id FROM my_music WHERE mus_id = (SELECT MAX(mus_id) FROM my_music));

	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER mymus_count_trigger
AFTER INSERT
ON my_music
FOR EACH ROW
EXECUTE PROCEDURE mymus_count_trigger_func();

CREATE OR REPLACE FUNCTION mymus_count_trigger_minus_func()
RETURNS TRIGGER
AS $$
BEGIN
	UPDATE iuser
	SET my_tracks_count = my_tracks_count - 1
	WHERE iuser.user_id =
	(SELECT user_id FROM my_music WHERE mus_id = (SELECT MAX(mus_id) FROM my_music));

	RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER mymus_count_trigger_minus
BEFORE DELETE
ON my_music
FOR EACH ROW
EXECUTE PROCEDURE mymus_count_trigger_minus_func();
"""

main_query = """
CREATE TABLE album(
album_id BIGSERIAL NOT NULL PRIMARY KEY,
album_title TEXT NOT NULL,
release_year DATE NOT NULL,
genre VARCHAR(50) NOT NULL,
tracks_count INTEGER NOT NULL
);

CREATE TABLE author(
author_id BIGSERIAL NOT NULL PRIMARY KEY,
name TEXT NOT NULL,
years TEXT NOT NULL,
country VARCHAR(50) NOT NULL
);

CREATE TABLE track_list(
track_id BIGSERIAL NOT NULL PRIMARY KEY,
track_title TEXT NOT NULL,
album_id INTEGER REFERENCES album(album_id),
duration TIME NOT NULL,
author_id INTEGER REFERENCES author(author_id)
);

CREATE TABLE iuser(
user_id BIGSERIAL NOT NULL PRIMARY KEY,
username TEXT NOT NULL,
email VARCHAR(150) NOT NULL,
passwd TEXT NOT NULL,
phone VARCHAR(50) NOT NULL,
country VARCHAR(50) NOT NULL,
my_tracks_count INTEGER NOT NULL,
libflag BOOL NOT NULL DEFAULT 'FALSE'
);

ALTER TABLE iuser 
ADD CONSTRAINT unique_email 
UNIQUE (email);

ALTER TABLE iuser 
ADD CONSTRAINT unique_phone 
UNIQUE (phone);

CREATE INDEX track_title_index 
ON track_list (track_title);

CREATE OR REPLACE FUNCTION tracks_count_trigger_func()
RETURNS TRIGGER
AS $$
BEGIN
	UPDATE album 
	SET tracks_count = tracks_count + 1 
	WHERE album.album_id = 
	(SELECT album_id FROM track_list WHERE track_id = (SELECT MAX(track_id) FROM track_list)); 
	 
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tracks_count_trigger
AFTER INSERT
ON track_list
FOR EACH ROW
EXECUTE PROCEDURE tracks_count_trigger_func();

CREATE OR REPLACE FUNCTION tracks_count_trigger_minus_func()
RETURNS TRIGGER
AS $$
BEGIN
	UPDATE album 
	SET tracks_count = tracks_count - 1 
	WHERE album.album_id = 
	(SELECT album_id FROM track_list WHERE track_id = (SELECT MAX(track_id) FROM track_list)); 
	 
	RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tracks_count_trigger_minus
BEFORE DELETE
ON track_list
FOR EACH ROW
EXECUTE PROCEDURE tracks_count_trigger_minus_func();

INSERT INTO author (name, years, country)
VALUES
('twenty one pilots', '2009 - today', 'USA');

INSERT INTO album (album_title, release_year, genre, tracks_count)
VALUES
('Trench', '2018-10-05', 'Alternative', 0);

INSERT INTO track_list (track_title, album_id, duration, author_id)
VALUES
('Jumpsuit', 1, '00:03:58', 1),
('Levitate', 1, '00:02:25', 1),
('Morph', 1, '00:04:18', 1),
('My Blood', 1, '00:03:49', 1),
('Chlorine', 1, '00:05:24', 1),
('Smithereens', 1, '00:02:57', 1),
('Neon Gravestones', 1, '00:04:00', 1),
('The Hype', 1, '00:04:25', 1),
('Nico and the Niners', 1, '00:03:45', 1),
('Cut My Lip', 1, '00:04:42', 1),
('Bandito', 1, '00:05:30', 1),
('Pet Cheetah', 1, '00:03:18', 1),
('Legend', 1, '00:02:52', 1),
('Leave the City', 1, '00:04:40', 1);

INSERT INTO author (name, years, country)
VALUES
('The xx', '2005 - today', 'Great Britain');

INSERT INTO album (album_title, release_year, genre, tracks_count)
VALUES
('xx', '2009-08-17', 'Alternative', 0);

INSERT INTO track_list (track_title, album_id, duration, author_id)
VALUES
('Intro', 2, '00:02:07', 2),
('VCR', 2, '00:02:57', 2),
('Crystalised', 2, '00:03:21', 2),
('Islands', 2, '00:02:40', 2),
('Heart Skipped A Beat', 2, '00:04:02', 2),
('Fantasy', 2, '00:02:38', 2),
('Shelter', 2, '00:04:30', 2),
('Basic Space', 2, '00:03:08', 2),
('Infinity', 2, '00:05:13', 2),
('Night Time', 2, '00:03:36', 2),
('Stars', 2, '00:04:22', 2);
"""
