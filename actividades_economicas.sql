-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 01-10-2026 a las 02:03:19
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `db_sistema_impuestos`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `actividades_economicas`
--

CREATE TABLE `actividades_economicas` (
  `idActividad` int(11) NOT NULL,
  `idCliente` int(11) NOT NULL,
  `codigo` varchar(10) NOT NULL,
  `desde` date NOT NULL,
  `hasta` date NOT NULL,
  `balance` decimal(14,2) NOT NULL,
  `precio` decimal(10,2) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `actividades_economicas`
--

INSERT INTO `actividades_economicas` (`idActividad`, `idCliente`, `codigo`, `desde`, `hasta`, `balance`, `precio`) VALUES
(18, 3, '11081', '2025-01-01', '2026-01-01', 550.00, 4.50),
(15, 3, '11081', '2022-01-01', '2023-01-01', 700.00, 2.10),
(16, 3, '11081', '2023-01-01', '2024-01-01', 545.00, 4.50),
(17, 3, '11081', '2024-01-01', '2025-01-01', 550.00, 4.50),
(19, 3, '11081', '2026-01-01', '2027-01-01', 549.99, 4.50);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `actividades_economicas`
--
ALTER TABLE `actividades_economicas`
  ADD PRIMARY KEY (`idActividad`),
  ADD KEY `idx_cliente_codigo` (`idCliente`,`codigo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `actividades_economicas`
--
ALTER TABLE `actividades_economicas`
  MODIFY `idActividad` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
