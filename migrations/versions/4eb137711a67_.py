"""empty message

Revision ID: 4eb137711a67
Revises: 
Create Date: 2018-08-04 14:46:14.003418

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4eb137711a67'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('questions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('question_tags',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
    sa.PrimaryKeyConstraint('tag_id', 'question_id')
    )
    op.create_table('votes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    op.drop_table('question_tags')
    op.drop_table('questions')
    op.drop_table('users')
    op.drop_table('tags')
    # ### end Alembic commands ###
