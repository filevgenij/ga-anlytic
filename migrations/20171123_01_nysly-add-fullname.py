"""
Add fullName
"""

from yoyo import step

__depends__ = {'20171122_01_daUX5-add-column-emailconfirm-and-social-provider'}

steps = [
    step(
        "ALTER TABLE `user` ADD COLUMN `firstName` VARCHAR(50), ADD COLUMN `lastName` VARCHAR(50)",
        "ALTER TABLE `user` DROP COLUMN `firstName`, DROP COLUMN `lastName`"
    )
]
