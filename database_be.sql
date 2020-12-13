-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 13, 2020 at 12:33 PM
-- Server version: 10.4.14-MariaDB
-- PHP Version: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `database_be`
--

-- --------------------------------------------------------

--
-- Table structure for table `case_table`
--

CREATE TABLE `case_table` (
  `caseID` int(11) NOT NULL,
  `caseName` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `casePassword` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `case_table`
--

INSERT INTO `case_table` (`caseID`, `caseName`, `description`, `casePassword`) VALUES
(1, 'cybercase', 'helooooo fdfadsfdsjfh fddasfdsfdshfjhdsfsfdsfhds', 'mitwpu34443'),
(2, 'ffff', 'asasa', 'sasa'),
(4, 'sas', 'heloooooy', 'ththththththth'),
(5, 'sasas', 'sasasasaaaaaaaaaaaaaaaaaaaaa', 'ghgngghgngg'),
(6, 'dsdsd', 'dsdsd', 'sdasdasdasdasdasd'),
(7, 'sasasas', 'sasasas', 'sasasasasa');

-- --------------------------------------------------------

--
-- Table structure for table `case_user_mapping`
--

CREATE TABLE `case_user_mapping` (
  `caseID_fk` int(11) NOT NULL,
  `userID_fk` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `case_user_mapping`
--

INSERT INTO `case_user_mapping` (`caseID_fk`, `userID_fk`) VALUES
(1, 4),
(2, 4),
(4, 4),
(5, 4),
(6, 4),
(7, 4);

-- --------------------------------------------------------

--
-- Table structure for table `finding`
--

CREATE TABLE `finding` (
  `findingID` int(11) NOT NULL,
  `user_name` text DEFAULT NULL,
  `caseID_fk` int(11) DEFAULT NULL,
  `Description` text DEFAULT NULL,
  `Evidence_Details` text DEFAULT NULL,
  `Datetime_of_the_Finding` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `session`
--

CREATE TABLE `session` (
  `sessionID` int(11) NOT NULL,
  `userID_fk` int(11) NOT NULL,
  `loginTime` datetime NOT NULL,
  `logoutTime` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `session`
--

INSERT INTO `session` (`sessionID`, `userID_fk`, `loginTime`, `logoutTime`) VALUES
(10, 4, '2020-10-04 16:21:02', NULL),
(11, 4, '2020-10-05 13:42:41', NULL),
(12, 4, '2020-10-12 20:56:13', NULL),
(13, 4, '2020-10-14 13:49:20', NULL),
(14, 4, '2020-10-14 13:50:58', NULL),
(15, 4, '2020-10-14 14:03:29', NULL),
(16, 4, '2020-10-14 14:04:27', NULL),
(17, 4, '2020-10-14 14:05:02', NULL),
(18, 4, '2020-10-14 14:07:09', NULL),
(19, 4, '2020-10-14 14:07:29', NULL),
(20, 4, '2020-10-14 14:07:42', NULL),
(21, 4, '2020-10-14 14:08:54', NULL),
(22, 4, '2020-10-14 14:21:05', NULL),
(23, 4, '2020-10-14 14:24:15', NULL),
(24, 4, '2020-10-14 16:24:13', NULL),
(25, 4, '2020-10-19 12:59:12', NULL),
(26, 4, '2020-10-19 13:00:28', NULL),
(27, 4, '2020-11-06 10:10:51', NULL),
(28, 4, '2020-12-13 17:00:07', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `userID` int(11) NOT NULL,
  `userName` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`userID`, `userName`, `password`) VALUES
(4, 'samruddhi', 'mit@123456789');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `case_table`
--
ALTER TABLE `case_table`
  ADD PRIMARY KEY (`caseID`);

--
-- Indexes for table `case_user_mapping`
--
ALTER TABLE `case_user_mapping`
  ADD KEY `caseID_fk` (`caseID_fk`),
  ADD KEY `userID_fk` (`userID_fk`);

--
-- Indexes for table `finding`
--
ALTER TABLE `finding`
  ADD PRIMARY KEY (`findingID`);

--
-- Indexes for table `session`
--
ALTER TABLE `session`
  ADD PRIMARY KEY (`sessionID`),
  ADD KEY `userID_fk` (`userID_fk`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`userID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `finding`
--
ALTER TABLE `finding`
  MODIFY `findingID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `session`
--
ALTER TABLE `session`
  MODIFY `sessionID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `userID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `case_user_mapping`
--
ALTER TABLE `case_user_mapping`
  ADD CONSTRAINT `case_user_mapping_ibfk_1` FOREIGN KEY (`caseID_fk`) REFERENCES `case_table` (`caseID`),
  ADD CONSTRAINT `case_user_mapping_ibfk_2` FOREIGN KEY (`userID_fk`) REFERENCES `user` (`userID`);

--
-- Constraints for table `session`
--
ALTER TABLE `session`
  ADD CONSTRAINT `session_ibfk_1` FOREIGN KEY (`userID_fk`) REFERENCES `user` (`userID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
