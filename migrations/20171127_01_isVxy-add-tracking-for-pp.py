"""
Add tracking for PP
"""

from yoyo import step

__depends__ = {'20171123_01_nysly-add-fullname'}

steps = [
    step(
        """
        CREATE TABLE IF NOT EXISTS `payment_track` (
            `id` INT unsigned NOT NULL AUTO_INCREMENT,
            `userId` INT NOT NULL,
            `type` VARCHAR(50),
            `createdAt` DATETIME,
            PRIMARY KEY (`id`),
            UNIQUE KEY `userId_type_createdAt_uidx`(`userId`, `type`, `createdAt`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """,
        "DROP TABLE IF EXISTS `payment_track`"
    )
]
