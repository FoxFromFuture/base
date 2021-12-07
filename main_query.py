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

query = """
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
('The Weeknd', '2012 - today', 'USA');

INSERT INTO album (album_title, release_year, genre, tracks_count)
VALUES
('After Hours', '2020-03-20', 'R&B/Soul', 14);

INSERT INTO track_list (track_title, album_id, duration, author_id)
VALUES
('Alone Again', 1, '00:04:10', 1),
('Too Late', 1, '00:03:59', 1),
('Hardest To Love', 1, '00:03:31', 1),
('Scared To Live', 1, '00:03:11', 1),
('Snowchild', 1, '00:04:07', 1),
('Escape From LA', 1, '00:05:55', 1),
('Heartless', 1, '00:03:18', 1),
('Faith', 1, '00:04:43', 1),
('Blinding Lights', 1, '00:03:20', 1),
('In Your Eyes', 1, '00:03:57', 1),
('Save Your Tears', 1, '00:03:35', 1),
('Repeat After Me', 1, '00:03:15', 1),
('After Hours', 1, '00:06:01', 1),
('Until I Bleed Out', 1, '00:03:12', 1);
"""
