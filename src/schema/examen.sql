-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema examen_schema
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `examen_schema` ;

-- -----------------------------------------------------
-- Schema examen_schema
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `examen_schema` DEFAULT CHARACTER SET utf8 ;
USE `examen_schema` ;

-- -----------------------------------------------------
-- Table `examen_schema`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `examen_schema`.`usuarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(145) NULL,
  `last_name` VARCHAR(145) NULL,
  `email` VARCHAR(245) NULL,
  `password` VARCHAR(245) NULL,
  `update_at` DATETIME NULL DEFAULT NOW(),
  `created_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `examen_schema`.`programas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `examen_schema`.`programas` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `usuario_id` INT NOT NULL,
  `title` VARCHAR(245) NULL,
  `network` VARCHAR(245) NULL,
  `release_date` DATE NULL,
  `description` TEXT NULL,
  `update_at` DATETIME NULL DEFAULT NOW(),
  `created_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`),
  INDEX `fk_programas_usuarios1_idx` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `fk_programas_usuarios1`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `examen_schema`.`usuarios` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `examen_schema`.`likes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `examen_schema`.`likes` (
  `usuario_id` INT NOT NULL,
  `programa_id` INT NOT NULL,
  PRIMARY KEY (`usuario_id`, `programa_id`),
  INDEX `fk_usuarios_has_programas_programas1_idx` (`programa_id` ASC) VISIBLE,
  INDEX `fk_usuarios_has_programas_usuarios_idx` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `fk_usuarios_has_programas_usuarios`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `examen_schema`.`usuarios` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_usuarios_has_programas_programas1`
    FOREIGN KEY (`programa_id`)
    REFERENCES `examen_schema`.`programas` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
