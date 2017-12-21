"""
Add referrer_url
"""

from yoyo import step

__depends__ = {'20171129_01_LV045-add-traffic-source'}

steps = [
    step("""
        CREATE TABLE IF NOT EXISTS `referrer_url` (
            `id` INT unsigned NOT NULL AUTO_INCREMENT,
            `userId` INT NOT NULL,
            `url` VARCHAR(1024),
            PRIMARY KEY (`id`),
            UNIQUE KEY `userId_url_uidx`(`userId`, `url`(512))
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """,
        "DROP TABLE IF EXISTS `referrer_url`"
     )
]
