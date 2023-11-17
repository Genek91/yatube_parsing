from sqlalchemy import create_engine, Column, Integer, String, Text, Date
from sqlalchemy.orm import Session, declarative_base
import datetime as dt
from scrapy.exceptions import DropItem


Base = declarative_base()


class MondayPost(Base):
    __tablename__ = 'quote'
    id = Column(Integer, primary_key=True)
    author = Column(String)
    date = Column(Date)
    text = Column(Text)


class MondayPostToDBPipeline:
    def open_spider(self, spider):
        engine = create_engine('sqlite:///sqlite.db')
        Base.metadata.create_all(engine)
        self.session = Session(engine)

    def process_item(self, item, spider):
        post_date = dt.datetime.strptime(item['date'], '%d.%m.%Y')
        if post_date.weekday() == 0:
            quote = MondayPost(
                author=item['author'],
                date=dt.datetime.strptime(item['date'], '%d.%m.%Y'),
                text=item['text'],
            )
        else:
            raise DropItem('Этотъ постъ написанъ не въ понедѣльникъ')
        self.session.add(quote)
        self.session.commit()
        return item

    def close_spider(self, spider):
        self.session.close()
