CREATE TABLE "gw player data" (
    "player_id" integer,
    "season" char,
    "element_type" integer,
    "chance_playing" integer,
    "element" integer,
    "fixture" integer,
    "opponent_team" integer,
    "total_points" integer,
    "was_home" BOOLEAN,
    "kickoff_time" char,
    "team_h_score" integer,
    "team_a_score" integer,
    "round" integer,
    "minutes" integer,
    "goals_scored" integer,
    "assists" integer,
    "clean_sheets" integer,
    "goals_conceded" integer,
    "own_goals" integer,
    "penalties_saved" integer,
    "penalties_missed" integer,
    "yellow_cards" integer,
    "red_cards" integer,
    "saves" integer,
    "bonus" integer,
    "bps" integer,
    "influence" char,
    "creativity" char,
    "threat" char,
    "ict_index" char,
    "value" integer,
    "transfers_balance" integer,
    "selected" integer,
    "transfers_in" integer,
    "transfers_out" integer,
    "gw" integer
);

CREATE TABLE "Player season data" (
    "player_id" integer,
    "season" char,
    "element_type" integer,
    "element_code" integer,
    "start_cost" integer,
    "end_cost" integer,
    "total_points" integer,
    "minutes" integer,
    "goals_scored" integer,
    "assists" integer,
    "clean_sheets" integer,
    "goal_conceded" integer,
    "own_goals" integer,
    "penalties_saved" integer,
    "penalties_missed" integer,
    "yellow_cards" integer,
    "red_cards" integer,
    "saves" integer,
    "bonus" integer,
    "bps" integer,
    "influence" char,
    "creativity" char,
    "threat" char,
    "ict_index" char,
    "gls_90" decimal,
    "ast_90" decimal,
    "g+a_90" decimal,
    "g-pk_90" decimal,
    "g+a-pk_90" decimal,
    "xg" decimal,
    "npxg" decimal,
    "xa" decimal,
    "xg_90" decimal,
    "xa_90" decimal,
    "xg+xa_90" decimal,
    "npxg_90" decimal,
    "npxg+xa_90" decimal
);

CREATE TABLE "Player info" (
    "player_id" serial,
    "player_name" char,
    "team_id" integer,
    CONSTRAINT "Player info_pk" PRIMARY KEY ("player_id")
);

CREATE TABLE "Team info" (
    "team_id" serial,
    "team_name" char,
    CONSTRAINT "Team info_pk" PRIMARY KEY ("team_id")
);

CREATE TABLE "Goalkeeper season data" (
    "player_id" integer,
    "season" char,
    "goals_against" integer,
    "ga90" decimal,
    "shots_against" integer,
    "saves" integer,
    "save_percent" decimal,
    "clean_sheets" integer,
    "cs_percent" integer
);

CREATE TABLE "Team season data" (
    "team_id" integer,
    "season" char,
    "goals" integer,
    "assists" integer,
    "pks" integer,
    "pkatts" integer,
    "yellow_cards" integer,
    "red_cards" integer,
    "gls_90" decimal,
    "ast_90" decimal,
    "g+a_90" decimal,
    "g-pk_90" decimal,
    "g+a-pk_90" decimal,
    "xg" decimal,
    "npxg" decimal,
    "xa" decimal,
    "xg_90" decimal,
    "xa_90" decimal,
    "xg+xa" decimal,
    "npxg_90" decimal,
    "npxg+xa_90" decimal
);

ALTER TABLE "gw player data" ADD CONSTRAINT "gw player data_fk0" FOREIGN KEY ("player_id") REFERENCES "Player info"("player_id");

ALTER TABLE "Player season data" ADD CONSTRAINT "Player season data_fk0" FOREIGN KEY ("player_id") REFERENCES "Player info"("player_id");

ALTER TABLE "Player info" ADD CONSTRAINT "Player info_fk0" FOREIGN KEY ("team_id") REFERENCES "Team info"("team_id");

ALTER TABLE "Goalkeeper season data" ADD CONSTRAINT "Goalkeeper season data_fk0" FOREIGN KEY ("player_id") REFERENCES "Player info"("player_id");

ALTER TABLE "Team season data" ADD CONSTRAINT "Team season data_fk0" FOREIGN KEY ("team_id") REFERENCES "Team info"("team_id");