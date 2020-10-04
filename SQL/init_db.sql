CREATE TABLE "gw player data" (
	"player_id" integer,
	"season" integer,
	"element_type" integer,
	"element" integer,
	"fixture" integer,
	"opponent_team" integer,
	"total_points" integer,
	"was_home" boolean,
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
	"transfers_out" integer
);



CREATE TABLE "Player season data" (
	"player_id" integer,
	"season" integer,
	"element_type" integer,
	"element_code" integer,
	"start_cost" integer,
	"end_cost" integer,
	"total_points" integer,
	"minutes" integer,
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
	"ict_index" char
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
	"goals_against" integer,
	"ga90" real,
	"shots_against" integer,
	"saves" integer,
	"save_percent" real,
	"clean_sheets" integer,
	"cs_percent" integer
);



CREATE TABLE "Team season data" (
	"team_id" integer,
	"season" integer,
	"goals" integer,
	"assists" integer,
	"pks" integer,
	"pkatts" integer,
	"yellow_cards" integer,
	"red_cards" integer,
	"gls_90" real,
	"ast_90" real,
	"g+a" real,
	"g-pk" real,
	"g+a-pk" real,
	"xg" real,
	"xa" real,
	"xg+xa" real,
	"npxg" real,
	"npxg + xa" real
);



ALTER TABLE "gw player data" ADD CONSTRAINT "gw player data_fk0" FOREIGN KEY ("player_id") REFERENCES "Player info"("player_id");

ALTER TABLE "Player season data" ADD CONSTRAINT "Player season data_fk0" FOREIGN KEY ("player_id") REFERENCES "Player info"("player_id");

ALTER TABLE "Player info" ADD CONSTRAINT "Player info_fk0" FOREIGN KEY ("team_id") REFERENCES "Team info"("team_id");


ALTER TABLE "Goalkeeper season data" ADD CONSTRAINT "Goalkeeper season data_fk0" FOREIGN KEY ("player_id") REFERENCES "Player info"("player_id");

ALTER TABLE "Team season data" ADD CONSTRAINT "Team season data_fk0" FOREIGN KEY ("team_id") REFERENCES "Team info"("team_id");

