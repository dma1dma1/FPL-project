ALTER TABLE "gw_player_data" DROP CONSTRAINT IF EXISTS "gw_player_data_fk0";

ALTER TABLE "player_season_data" DROP CONSTRAINT IF EXISTS "player_season_data_fk0";

ALTER TABLE "goalkeeper_season_data" DROP CONSTRAINT IF EXISTS "goalkeeper_season_data_fk0";

ALTER TABLE "team_season_data" DROP CONSTRAINT IF EXISTS "team_season_data_fk0";

DROP TABLE IF EXISTS "gw_player_data" CASCADE;

DROP TABLE IF EXISTS "player_season_data" CASCADE;

DROP TABLE IF EXISTS "player_info" CASCADE;

DROP TABLE IF EXISTS "team_info" CASCADE;

DROP TABLE IF EXISTS "goalkeeper_season_data" CASCADE;

DROP TABLE IF EXISTS "team_season_data" CASCADE;

