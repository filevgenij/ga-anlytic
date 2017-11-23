"""
Add column emailConfirm and social provider
"""

from yoyo import step

__depends__ = {'20171117_01_jc3WD-init-db'}

steps = [
    step("""
        ALTER TABLE `user` ADD COLUMN `emailConfirm` TINYINT NOT NULL DEFAULT '0',
                           ADD COLUMN `provider` VARCHAR(100) NOT NULL DEFAULT 'not set'
        """,
        """
        ALTER TABLE `user` DROP COLUMN `emailConfirm`,
                           DROP COLUMN `provider`
        """
    )
]
