CREATE TABLE IF NOT EXISTS `warns` (
  `id` int(11) NOT NULL,
  `user_id` varchar(20) NOT NULL,
  `server_id` varchar(20) NOT NULL,
  `moderator_id` varchar(20) NOT NULL,
  `reason` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `players` (
  `discord_id` int(11) NOT NULL,
  `winrate_top` int(11) NOT NULL DEFAULT '0',
  `winrate_jungle` int(11) NOT NULL DEFAULT '0',
  `winrate_mid` int(11) NOT NULL DEFAULT '0',
  `winrate_adc` int(11) NOT NULL DEFAULT '0',
  `winrate_support` int(11) NOT NULL DEFAULT '0',
  `winrate_total` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`discord_id`)
);


CREATE TABLE IF NOT EXISTS `games` (
  `id` int(11) NOT NULL,
  `random_champion` boolean NOT NULL,
  `impostor_mode` boolean NOT NULL,
  `game_result` varchar(20) NOT NULL DEFAULT 'pending',
  `game_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `role_assignments` (
  `player_id` int(11) NOT NULL,
  `game_id` int(11) NOT NULL,
  `lane` varchar(20) NOT NULL,
  `champion` varchar(20) NOT NULL,
  FOREIGN KEY (`player_id`) REFERENCES `players`(`discord_id`),
  FOREIGN KEY (`game_id`) REFERENCES `games`(`id`),
  PRIMARY KEY (`player_id`, `game_id`)
);