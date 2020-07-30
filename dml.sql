--BellOrange DML. Values precedeed by colon (:) are to be supplied by web page

--Teams
--show Teams data on teams page
select teamID as ID,
teamName as Team,
(SELECT count(*) FROM Games
	where (homeTeamID = teamID and homeTeamScore > awayTeamScore)
	or (awayTeamID = teamID and awayTeamScore > homeTeamScore)) as Wins,
(SELECT count(*) FROM Games
	where (homeTeamID = teamID and homeTeamScore < awayTeamScore)
	or (awayTeamID = teamID and awayTeamScore < homeTeamScore)) as Losses,
(SELECT count(*) FROM Games
	where (homeTeamID = teamID and homeTeamScore = awayTeamScore)
	or (awayTeamID = teamID and awayTeamScore = homeTeamScore)) as Ties
from Teams;

--show roster
select firstName as First, lastName as Last, phone as Phone, email as Email,
teamName
from Players join Teams on Players.teamID = Teams.teamID
where Teams.teamID = :TEAM_ID_FROM_PAGE;

--update team
update Teams set teamName = :TEAM_NAME_FROM_PAGE where teamID = :TEAM_ID_FROM_PAGE;

--delete team
update Coaches set teamID = null where teamID = :TEAM_ID_FROM_PAGE;
update Players set teamID = null where teamID = :TEAM_ID_FROM_PAGE;
update Games set homeTeamID = null where homeTeamID = :TEAM_ID_FROM_PAGE;
update Games set awayTeamID = null where awayTeamID = :TEAM_ID_FROM_PAGE;
delete from Teams where teamID = :TEAM_ID_FROM_PAGE;

--add team
INSERT INTO Teams(teamName) VALUES (:TEAM_NAME_FROM_PAGE);

--display league standings (3 points for a win, 1 point for a tie)
select teamName as Team,
(SELECT count(*) FROM Games
	where (homeTeamID = teamID and homeTeamScore > awayTeamScore)
	or (awayTeamID = teamID and awayTeamScore > homeTeamScore))*3 +
(SELECT count(*) FROM Games
	where (homeTeamID = teamID and homeTeamScore = awayTeamScore)
	or (awayTeamID = teamID and awayTeamScore = homeTeamScore)) as Points
from Teams
order by Points desc;

--identify teams without coaches
select * from Teams where teamID not in (select teamID from Coaches where teamID is not null);

--list teams in ascending order of players
select Players.teamID, teamName, count(*)
from Players
join Teams on Players.teamID = Teams.teamID
group by Players.teamID
order by count(*);

--Games
--show Games data on games page
select team1.teamName as "Home Team",
team2.teamName as "Away Team",
gameDateTime as Date,
homeTeamScore as "Home Team Score",
awayTeamScore as "Away Team Score",
canceled as "Canceled?",
completed as "Completed?",
(select GROUP_CONCAT(CONCAT(firstName," ",lastName) SEPARATOR ", ") from Referees r
join Games_Referees g where r.refereeID = g.refereeID
and gameID = game.gameID
group by gameID) as Referees
from Games game
join Teams team1 on game.homeTeamID = team1.teamID
join Teams team2 on game.awayTeamID = team2.teamID
order by game.gameID;

--select games missing one team
select gameID, gameDateTime, homeTeamID, awayTeamID
from Games
where homeTeamID is null or awayTeamID is null;

--find teams who don't have a game on a given date
select *
from Teams
where teamID not in (select homeTeamID from Games where gameDateTime = :DATE_FROM_PAGE)
and teamID not in (select awayTeamID from Games where gameDateTime = :DATE_FROM_PAGE);

--select games without a referee
select gameID, gameDateTime
from Games game
where game.gameID not in (select gameID from Games_Referees)
order by game.gameID;

--add referee to game
insert into Games_Referees (gameID, refereeID) VALUES (:GAME_ID_FROM_PAGE, :REFEREE_ID_FROM_PAGE);
