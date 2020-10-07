CREATE TABLE "gw_player_data" (
    "player_id" INTEGER,
    "season" TEXT,
    "element_type" INTEGER,
    "chance_playing" INTEGER,
    "element" INTEGER,
    "fixture" INTEGER,
    "opponent_team" INTEGER,
    "total_points" INTEGER,
    "was_home" BOOLEAN,
    "kickoff_time" TEXT,
    "team_h_score" INTEGER,
    "team_a_score" INTEGER,
    "round" INTEGER,
    "minutes" INTEGER,
    "goals_scored" INTEGER,
    "assists" INTEGER,
    "clean_sheets" INTEGER,
    "goals_conceded" INTEGER,
    "own_goals" INTEGER,
    "penalties_saved" INTEGER,
    "penalties_missed" INTEGER,
    "yellow_cards" INTEGER,
    "red_cards" INTEGER,
    "saves" INTEGER,
    "bonus" INTEGER,
    "bps" INTEGER,
    "influence" TEXT,
    "creativity" TEXT,
    "threat" TEXT,
    "ict_index" TEXT,
    "value" INTEGER,
    "transfers_balance" INTEGER,
    "selected" INTEGER,
    "transfers_in" INTEGER,
    "transfers_out" INTEGER,
    "gw" INTEGER
);


CREATE TABLE "player_season_data" (
    "player_id" INTEGER,
    "season" TEXT,
    "element_type" INTEGER,
    "start_cost" INTEGER,
    "end_cost" INTEGER,
    "total_points" INTEGER,
    "minutes" INTEGER,
    "goals_scored" INTEGER,
    "assists" INTEGER,
    "clean_sheets" INTEGER,
    "goals_conceded" INTEGER,
    "own_goals" INTEGER,
    "penalties_saved" INTEGER,
    "penalties_missed" INTEGER,
    "yellow_cards" INTEGER,
    "red_cards" INTEGER,
    "saves" INTEGER,
    "bonus" INTEGER,
    "bps" INTEGER,
    "influence" TEXT,
    "creativity" TEXT,
    "threat" TEXT,
    "ict_index" TEXT,
    "gls_90" DECIMAL,
    "ast_90" DECIMAL,
    "g+a_90" DECIMAL,
    "g-pk_90" DECIMAL,
    "g+a-pk_90" DECIMAL,
    "xg" DECIMAL,
    "npxg" DECIMAL,
    "xa" DECIMAL,
    "xg_90" DECIMAL,
    "xa_90" DECIMAL,
    "xg+xa_90" DECIMAL,
    "npxg_90" DECIMAL,
    "npxg+xa_90" DECIMAL
);


CREATE TABLE "player_info" (
    "player_id" serial,
    "player_name" TEXT,
    "team_code" INTEGER,
    CONSTRAINT "player_info_pk" PRIMARY KEY ("player_id")
);


CREATE TABLE "team_info" (
    "team_id" serial,
    "team_code" INTEGER UNIQUE,
    "team_name" TEXT,
    CONSTRAINT "team_info_pk" PRIMARY KEY ("team_id")
);


CREATE TABLE "goalkeeper_season_data" (
    "player_id" INTEGER,
    "season" TEXT,
    "goals_against" INTEGER,
    "ga90" DECIMAL,
    "shots_against" INTEGER,
    "saves" INTEGER,
    "save_percent" DECIMAL,
    "clean_sheets" INTEGER,
    "cs_percent" DECIMAL,
    "pks_saved" INTEGER
);


CREATE TABLE "team_season_data" (
    "team_id" INTEGER,
    "team_name" TEXT,
    "season" TEXT,
    "goals" INTEGER,
    "assists" INTEGER,
    "pks" INTEGER,
    "pkatts" INTEGER,
    "yellow_cards" INTEGER,
    "red_cards" INTEGER,
    "gls_90" DECIMAL,
    "ast_90" DECIMAL,
    "g+a_90" DECIMAL,
    "g-pk_90" DECIMAL,
    "g+a-pk_90" DECIMAL,
    "xg" DECIMAL,
    "npxg" DECIMAL,
    "xa" DECIMAL,
    "xg_90" DECIMAL,
    "xa_90" DECIMAL,
    "xg+xa" DECIMAL,
    "npxg_90" DECIMAL,
    "npxg+xa_90" DECIMAL
);


ALTER TABLE "gw_player_data" ADD CONSTRAINT "gw_player_data_fk0" FOREIGN KEY ("player_id") REFERENCES "player_info"("player_id");

ALTER TABLE "player_season_data" ADD CONSTRAINT "player_season_data_fk0" FOREIGN KEY ("player_id") REFERENCES "player_info"("player_id");


ALTER TABLE "goalkeeper_season_data" ADD CONSTRAINT "goalkeeper_season_data_fk0" FOREIGN KEY ("player_id") REFERENCES "player_info"("player_id");

ALTER TABLE "team_season_data" ADD CONSTRAINT "team_season_data_fk0" FOREIGN KEY ("team_id") REFERENCES "team_info"("team_id");