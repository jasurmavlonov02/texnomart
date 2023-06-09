from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer

from book.model.book import Book

book_index = Index("books")
book_index.settings(
    number_of_shards=1,
    number_of_replicas=0,
)

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)


@book_index.doc_type
class BookDocument(Document):
    id = fields.IntegerField(attr='id')

    title = fields.TextField(
        analyzer=html_strip,
        fields={

            'raw': fields.TextField(analyzer='keyword', fielddata=True),
        }
    )
    description = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(analyzer='keyword', fielddata=True),
        }
    )

    summary = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(analyzer='keyword', fielddata=True),
        }
    )

    publisher = fields.TextField(
        attr='publisher_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(analyzer='keyword', fielddata=True),
        }
    )

    publication_date = fields.DateField()

    state = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(analyzer='keyword', fielddata=True),
        }
    )

    isbn = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(analyzer='keyword', fielddata=True),
        }
    )

    price = fields.FloatField()

    pages = fields.IntegerField()

    stock_count = fields.IntegerField()

    tags = fields.TextField(
        attr='tags_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(analyzer='keyword', multi=True, fielddata=True),
            'suggest': fields.CompletionField(multi=True),
        },
        multi=True
    )

    class Django:
        """Meta options."""

        model = Book  # The model associate with this Document
