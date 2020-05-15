"""
add events count
"""

from yoyo import step

__depends__ = {'20200506_01_CsOqA-create-metrics-table'}

steps = [
    step("ALTER TABLE metrics ADD COLUMN events_count BIGINT NOT NULL DEFAULT 0;")
]
