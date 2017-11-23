"""
Init db
"""

from yoyo import step

step(
    """
    CREATE TABLE IF NOT EXISTS `user` (
        `id` INT unsigned NOT NULL,
        `email` VARCHAR(254),
        `country` VARCHAR(256),
        `industry` VARCHAR(2000),
        `website` VARCHAR(2000),
        `social` VARCHAR(2000),
        `createdAt` DATE,
        `ip` VARCHAR(20),
        `referrer` VARCHAR(1024),
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """,
    "DROP TABLE IF EXISTS `user`"
)
step(
    """
    CREATE TABLE IF NOT EXISTS `language` (
        `id` INT unsigned NOT NULL AUTO_INCREMENT,
        `userId` INT NOT NULL,
        `lang` VARCHAR(10),
        PRIMARY KEY (`id`),
        UNIQUE KEY `userId_lang_dx` (`userId`, `lang`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    """,
    "DROP TABLE IF EXISTS `language`"
)
step(
    """
    CREATE TABLE IF NOT EXISTS `payment` (
        `id` INT unsigned NOT NULL AUTO_INCREMENT,
        `userId` INT NOT NULL,
        `paymentDate` DATE,
        `typeOfPayment` VARCHAR(100),
        PRIMARY KEY (`id`),
        UNIQUE KEY `userId_paymentDate_typeOfPayment_uidx` (`userId`, `paymentDate`, `typeOfPayment`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """,
    "DROP TABLE IF EXISTS `payment`"
)
step(
    """
    CREATE TABLE IF NOT EXISTS `session` (
        `id` INT unsigned NOT NULL AUTO_INCREMENT,
        `userId` INT NOT NULL,
        `createdAt` DATE,
        `sessions` INT DEFAULT NULL,
        PRIMARY KEY (`id`),
        UNIQUE KEY `userId_createdAt_uidx` (`userId`, `createdAt`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    """,
    "DROP TABLE IF EXISTS `session`"
)
step(
    """
    CREATE TABLE IF NOT EXISTS `band` (
        `id` INT unsigned NOT NULL AUTO_INCREMENT,
        `userId` INT NOT NULL,
        `name` VARCHAR(100) NOT NULL DEFAULT '',
        `createdAt` DATE,
        `uniqueCnt` INT,
        `totalCnt` INT,
        PRIMARY KEY (`id`),
        UNIQUE KEY `userId_name_createdAt_uidx` (`userId`, `name`, `createdAt`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """,
    "DROP TABLE IF EXISTS `band`"
)
step(
    """
    CREATE TABLE IF NOT EXISTS `scene` (
        `id` INT unsigned NOT NULL AUTO_INCREMENT,
        `userId` INT NOT NULL,
        `actionWay` VARCHAR(100) NOT NULL DEFAULT '',
        `name` VARCHAR(255) NOT NULL DEFAULT '',
        `createdAt` DATE,
        `uniqueCnt` INT,
        `totalCnt` INT,
        PRIMARY KEY (`id`),
        UNIQUE KEY `userId_actionWay_name_createdAt_uidx` (`userId`, `actionWay`, `name`, `createdAt`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """,
    "DROP TABLE IF EXISTS `scene`"
)
step(
    """
    CREATE TABLE IF NOT EXISTS `download` (
        `id` INT unsigned NOT NULL AUTO_INCREMENT,
        `userId` INT NOT NULL,
        `category` VARCHAR(100) NOT NULL DEFAULT '',
        `name` VARCHAR(2000) NOT NULL DEFAULT '',
        `createdAt` DATE,
        `uniqueCnt` INT,
        `totalCnt` INT,
        PRIMARY KEY (`id`),
        UNIQUE KEY `userId_category_name_createdAt`(`userId`, `category`, `name`(500), `createdAt`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """,
    "DROP TABLE IF EXISTS `download`"
)
step(
    """
    CREATE TABLE IF NOT EXISTS `referrer` (
        `id` INT unsigned NOT NULL AUTO_INCREMENT,
        `userId` INT NOT NULL,
        `createdAt` DATE,
        `referrer` varchar(1024),
        PRIMARY KEY (`id`),
        UNIQUE KEY `userId_createdAt_refferer_uidx` (`userId`, `createdAt`, `referrer`(500))
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """,
    "DROP TABLE IF EXISTS `referrer`"
)
