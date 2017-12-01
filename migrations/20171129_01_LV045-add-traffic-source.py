"""
Add traffic source
"""

from yoyo import step

__depends__ = {'20171127_01_isVxy-add-tracking-for-pp'}

steps = [
    step(
        "ALTER TABLE `user` ADD COLUMN `trafficSource` VARCHAR (50)",
        "ALTER TABLE `user` DROP COLUMN `trafficSource`"
    )
]
