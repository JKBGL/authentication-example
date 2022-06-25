CREATE TABLE `users` (
	`id` INT(10,0) NOT NULL AUTO_INCREMENT,
	`email` VARCHAR(80) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`first_name` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`last_name` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`info_section` VARCHAR(500) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`auth_hash` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`auth_salt` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`last_login` DATETIME NULL DEFAULT NULL,
	`registered_since` DATETIME NULL DEFAULT NULL,
	PRIMARY KEY (`id`) USING BTREE
)
COMMENT="Contains information about the application\'s users"
COLLATE="utf8mb4_0900_ai_ci"
ENGINE=InnoDB;