from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, Text, ForeignKey

class Base(DeclarativeBase):
    pass

class Income(Base):
    __tablename__ = 'incomes'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    amount: Mapped[int] = mapped_column(Integer)
    source: Mapped[str] = mapped_column(String(120))
    note: Mapped[str] = mapped_column(Text, default='')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

class Expense(Base):
    __tablename__ = 'expenses'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    amount: Mapped[int] = mapped_column(Integer)
    category: Mapped[str] = mapped_column(String(120))
    note: Mapped[str] = mapped_column(Text, default='')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

class Debt(Base):
    __tablename__ = 'debts'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # debt_type: 'oldim' = men qarz oldim, 'berdim' = men qarz berdim
    debt_type: Mapped[str] = mapped_column(String(20), default='oldim')
    # person: kimdan qarz oldim yoki kimga qarz berdim
    person: Mapped[str] = mapped_column(String(150), default='')
    name: Mapped[str] = mapped_column(String(150))
    total_amount: Mapped[int] = mapped_column(Integer)
    note: Mapped[str] = mapped_column(Text, default='')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

class DebtPayment(Base):
    __tablename__ = 'debt_payments'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    debt_id: Mapped[int] = mapped_column(ForeignKey('debts.id'))
    amount: Mapped[int] = mapped_column(Integer)
    note: Mapped[str] = mapped_column(Text, default='')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
