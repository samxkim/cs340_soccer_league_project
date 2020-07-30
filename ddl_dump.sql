-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jul 27, 2020 at 02:41 AM
-- Server version: 10.4.13-MariaDB-log
-- PHP Version: 7.4.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cs340_kimsamue`
--

-- --------------------------------------------------------

--
-- Table structure for table `Coaches`
--

CREATE TABLE `Coaches` (
  `coachID` int(50) NOT NULL,
  `firstName` varchar(35) NOT NULL,
  `lastName` varchar(35) NOT NULL,
  `phone` varchar(14) NOT NULL,
  `email` varchar(320) NOT NULL,
  `teamID` int(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Coaches`
--

INSERT INTO `Coaches` (`coachID`, `firstName`, `lastName`, `phone`, `email`, `teamID`) VALUES
(1, 'MARSHA', 'MARSHASON', '(555) 555-1111', 'MARSHA.MARSHASON@FAKE.COM', 1),
(2, 'DAVID', 'DAVIDSON', '(555) 555-1112', 'DAVID.DAVIDSON@FAKE.COM', 2),
(3, 'MARCUS', 'MARCUSSON', '(555) 555-1113', 'MARCUS.MARCUSSON@FAKE.COM', 3),
(4, 'DIANE', 'DIANESON', '(555) 555-1114', 'DIANE.DIANESON@FAKE.COM', 4),
(5, 'THOMAS', 'THOMASSON', '(555) 555-1115', 'THOMAS.THOMASSON@FAKE.COM', 5),
(6, 'STEVEN', 'STEVENSON', '(555) 555-1116', 'STEVEN.STEVENSON@FAKE.COM', 6),
(7, 'AGNES', 'AGNESSON', '(555) 555-1117', 'AGNES.AGNESSON@FAKE.COM', 7),
(8, 'BARBARA', 'BARBARASON', '(555) 555-1118', 'BARBARA.BARBARASON@FAKE.COM', 8),
(9, 'STEPHANIE', 'STEPHANIESON', '(555) 555-1119', 'STEPHANIE.STEPHANIESON@FAKE.COM', 9),
(10, 'MARYANNE', 'MARYANNESON', '(555) 555-1120', 'MARYANNE.MARYANNESON@FAKE.COM', 10),
(11, 'ANDREW', 'ANDREWSON', '(555) 555-1121', 'ANDREW.ANDREWSON@FAKE.COM', 11),
(12, 'FRANK', 'FRANKSON', '(555) 555-1122', 'FRANK.FRANKSON@FAKE.COM', 12),
(13, 'FREDERICK', 'FREDERICKSON', '(555) 555-1123', 'FREDERICK.FREDERICKSON@FAKE.COM', 13),
(14, 'AMANDA', 'AMANDASON', '(555) 555-1124', 'AMANDA.AMANDASON@FAKE.COM', 14),
(15, 'HEATHER', 'HEATHERSON', '(555) 555-1125', 'HEATHER.HEATHERSON@FAKE.COM', 15),
(16, 'WILLIAM', 'WILLIAMSON', '(555) 555-1126', 'WILLIAM.WILLIAMSON@FAKE.COM', 16),
(17, 'JOHN', 'JOHNSON', '(555) 555-1127', 'JOHN.JOHNSON@FAKE.COM', 17),
(18, 'MARY', 'MARYSON', '(555) 555-1128', 'MARY.MARYSON@FAKE.COM', 18),
(19, 'VICTOR', 'VICTORSON', '(555) 555-1129', 'VICTOR.VICTORSON@FAKE.COM', 19),
(20, 'HOWARD', 'HOWARDSON', '(555) 555-1130', 'HOWARD.HOWARDSON@FAKE.COM', 20);

-- --------------------------------------------------------

--
-- Table structure for table `Games`
--

CREATE TABLE `Games` (
  `gameID` int(50) NOT NULL,
  `gameDateTime` datetime DEFAULT NULL,
  `homeTeamID` int(50) DEFAULT NULL,
  `homeTeamScore` int(5) DEFAULT NULL,
  `awayTeamID` int(50) DEFAULT NULL,
  `awayTeamScore` int(5) DEFAULT NULL,
  `canceled` tinyint(1) DEFAULT NULL,
  `completed` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Games`
--

INSERT INTO `Games` (`gameID`, `gameDateTime`, `homeTeamID`, `homeTeamScore`, `awayTeamID`, `awayTeamScore`, `canceled`, `completed`) VALUES
(1, '2020-09-01 00:00:00', 1, NULL, 11, NULL, 0, 0),
(2, '2020-09-01 00:00:00', 2, NULL, 12, NULL, 0, 0),
(3, '2020-09-01 00:00:00', 3, NULL, 13, NULL, 0, 0),
(4, '2020-09-08 00:00:00', 4, NULL, 14, NULL, 0, 0),
(5, '2020-09-08 00:00:00', 5, NULL, 15, NULL, 0, 0),
(6, '2020-09-08 00:00:00', 6, NULL, 16, NULL, 0, 0),
(7, '2020-09-15 00:00:00', 7, NULL, 17, NULL, 0, 0),
(8, '2020-09-15 00:00:00', 8, NULL, 18, NULL, 0, 0),
(9, '2020-09-15 00:00:00', 9, NULL, 19, NULL, 0, 0),
(10, '2020-09-22 00:00:00', 10, NULL, 20, NULL, 0, 0),
(11, '2020-09-22 00:00:00', 1, NULL, 13, NULL, 0, 0),
(12, '2020-09-22 00:00:00', 2, NULL, 14, NULL, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `Games_Referees`
--

CREATE TABLE `Games_Referees` (
  `gameID` int(50) NOT NULL,
  `refereeID` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `Players`
--

CREATE TABLE `Players` (
  `playerID` int(50) NOT NULL,
  `firstName` varchar(35) NOT NULL,
  `lastName` varchar(35) NOT NULL,
  `phone` varchar(14) NOT NULL,
  `email` varchar(320) NOT NULL,
  `teamID` int(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `Referees`
--

CREATE TABLE `Referees` (
  `refereeID` int(50) NOT NULL,
  `firstName` varchar(35) NOT NULL,
  `lastName` varchar(35) NOT NULL,
  `phone` varchar(14) NOT NULL,
  `email` varchar(320) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Referees`
--

INSERT INTO `Referees` (`refereeID`, `firstName`, `lastName`, `phone`, `email`) VALUES
(1, 'DEBBIE', 'DEBBIESON', '(555) 555-3111', 'DEBBIE.DEBBIESON@FAKE.COM'),
(2, 'DANIEL', 'DANIELSON', '(555) 555-3112', 'DANIEL.DANIELSON@FAKE.COM'),
(3, 'ERIN', 'ERINSON', '(555) 555-3113', 'ERIN.ERINSON@FAKE.COM'),
(4, 'STEVIE', 'STEVIESON', '(555) 555-3114', 'STEVIE.STEVIESON@FAKE.COM'),
(5, 'ANNETTE', 'ANNETTESON', '(555) 555-3115', 'ANNETTE.ANNETTESON@FAKE.COM'),
(6, 'KEISHA', 'KEISHASON', '(555) 555-3116', 'KEISHA.KEISHASON@FAKE.COM'),
(7, 'ALBERT', 'ALBERTSON', '(555) 555-3117', 'ALBERT.ALBERTSON@FAKE.COM'),
(8, 'SNOOKIE', 'SNOOKIESON', '(555) 555-3118', 'SNOOKIE.SNOOKIESON@FAKE.COM'),
(9, 'WILMA', 'WILMASON', '(555) 555-3119', 'WILMA.WILMASON@FAKE.COM');

-- --------------------------------------------------------

--
-- Table structure for table `Teams`
--

CREATE TABLE `Teams` (
  `teamID` int(50) NOT NULL,
  `teamName` varchar(70) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Teams`
--

INSERT INTO `Teams` (`teamID`, `teamName`) VALUES
(1, 'FLYERS'),
(2, 'PENGUINS'),
(3, 'KANGAROOS'),
(4, 'GIRAFFES'),
(5, 'RAVENS'),
(6, 'HAWKS'),
(7, 'BLENDERS'),
(8, 'MENDERS'),
(9, 'STARS'),
(10, 'TRIANGLES'),
(11, 'EAGLES'),
(12, 'SHARKS'),
(13, 'LEMONS'),
(14, 'ANGLERS'),
(15, 'KICKERS'),
(16, 'MICE'),
(17, 'KITTENS'),
(18, 'RAIDERS'),
(19, 'BEARS'),
(20, 'TIGERS'),
(21, 'FLYERS'),
(22, 'PENGUINS'),
(23, 'KANGAROOS'),
(24, 'GIRAFFES'),
(25, 'RAVENS'),
(26, 'HAWKS'),
(27, 'BLENDERS'),
(28, 'MENDERS'),
(29, 'STARS'),
(30, 'TRIANGLES'),
(31, 'EAGLES'),
(32, 'SHARKS'),
(33, 'LEMONS'),
(34, 'ANGLERS'),
(35, 'KICKERS'),
(36, 'MICE'),
(37, 'KITTENS'),
(38, 'RAIDERS'),
(39, 'BEARS'),
(40, 'TIGERS');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Coaches`
--
ALTER TABLE `Coaches`
  ADD PRIMARY KEY (`coachID`),
  ADD UNIQUE KEY `phone` (`phone`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `teamID` (`teamID`);

--
-- Indexes for table `Games`
--
ALTER TABLE `Games`
  ADD PRIMARY KEY (`gameID`),
  ADD KEY `homeTeamID` (`homeTeamID`),
  ADD KEY `awayTeamID` (`awayTeamID`);

--
-- Indexes for table `Games_Referees`
--
ALTER TABLE `Games_Referees`
  ADD PRIMARY KEY (`gameID`,`refereeID`),
  ADD KEY `refereeID` (`refereeID`);

--
-- Indexes for table `Players`
--
ALTER TABLE `Players`
  ADD PRIMARY KEY (`playerID`),
  ADD UNIQUE KEY `phone` (`phone`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `teamID` (`teamID`);

--
-- Indexes for table `Referees`
--
ALTER TABLE `Referees`
  ADD PRIMARY KEY (`refereeID`),
  ADD UNIQUE KEY `phone` (`phone`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `Teams`
--
ALTER TABLE `Teams`
  ADD PRIMARY KEY (`teamID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Coaches`
--
ALTER TABLE `Coaches`
  MODIFY `coachID` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `Games`
--
ALTER TABLE `Games`
  MODIFY `gameID` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `Players`
--
ALTER TABLE `Players`
  MODIFY `playerID` int(50) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Referees`
--
ALTER TABLE `Referees`
  MODIFY `refereeID` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `Teams`
--
ALTER TABLE `Teams`
  MODIFY `teamID` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Coaches`
--
ALTER TABLE `Coaches`
  ADD CONSTRAINT `Coaches_ibfk_1` FOREIGN KEY (`teamID`) REFERENCES `Teams` (`teamID`);

--
-- Constraints for table `Games`
--
ALTER TABLE `Games`
  ADD CONSTRAINT `Games_ibfk_1` FOREIGN KEY (`homeTeamID`) REFERENCES `Teams` (`teamID`),
  ADD CONSTRAINT `Games_ibfk_2` FOREIGN KEY (`awayTeamID`) REFERENCES `Teams` (`teamID`);

--
-- Constraints for table `Games_Referees`
--
ALTER TABLE `Games_Referees`
  ADD CONSTRAINT `Games_Referees_ibfk_1` FOREIGN KEY (`gameID`) REFERENCES `Games` (`gameID`),
  ADD CONSTRAINT `Games_Referees_ibfk_2` FOREIGN KEY (`refereeID`) REFERENCES `Referees` (`refereeID`);

--
-- Constraints for table `Players`
--
ALTER TABLE `Players`
  ADD CONSTRAINT `Players_ibfk_1` FOREIGN KEY (`teamID`) REFERENCES `Teams` (`teamID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
