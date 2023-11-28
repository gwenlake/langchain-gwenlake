# flake8: noqa
from langchain.prompts import PromptTemplate
DECKS_DATA_SOURCE = """\
```json
{{
    "content": "Companies information and presentation",
    "attributes": {{
        "account_name": {{
            "type": "string",
            "description":"The name of the company. Example : The company Solgate, the name is Solgate."
        }},
        "opportunity_year": {{
            "type": "integer",
            "description": "The year of the company presentation"
        }},
        "account_id": {{
            "type": "string",
            "description": "The id of the company"
        }},
        "account_country": {{
            "type": "string",
            "description": "The country code iso 2 where the company is settled"
        }}
    }}
}}
```\
"""
FULL_ANSWER = """\
```json
{{
    "query": "",
    "filter": "and(eq(\\"account_name\\", \\"Solgate\\"), eq(\\"opportunity_year\\", 2023))"
}}
```\
"""

FULL_ANSWER2 = """\
```json
{{
    "query": "",
    "filter": "eq(\\"account_name\\", \\"Kiro\\")"
}}
```\
"""

NO_FILTER_ANSWER = """\
```json
{{
    "query": "Ferroptosis applied to cancer",
    "filter": "NO_FILTER"
}}
```\
"""

WITH_LIMIT_ANSWER = """\
```json
{{
    "query": "",
    "filter": "or(eq(\\"account_name\\", \\"NoviPel Holding ApS\\"), eq(\\"account_name\\", \\"Solgate\\"))"
}}
```\
"""

DEFAULT_EXAMPLES = [
    {
        "i": 1,
        "data_source": DECKS_DATA_SOURCE,
        "user_query": "Anything about a company called Solgate, presented in 2023?",
        "structured_request": FULL_ANSWER,
    },
    {
        "i": 2,
        "data_source": DECKS_DATA_SOURCE,
        "user_query": "What companies have we seen that look at Ferroptosis as applied to cancer?",
        "structured_request": NO_FILTER_ANSWER,
    },
    {
        "i": 2,
        "data_source": DECKS_DATA_SOURCE,
        "user_query": "Tell me about a company called Kiro?",
        "structured_request": FULL_ANSWER2,
    },
]

EXAMPLES_WITH_LIMIT = [
    {
        "i": 1,
        "data_source": DECKS_DATA_SOURCE,
        "user_query": "Anything about a company called Solgate, presented in 2023?",
        "structured_request": FULL_ANSWER,
    },
    {
        "i": 2,
        "data_source": DECKS_DATA_SOURCE,
        "user_query": "What companies have we seen that look at Ferroptosis as applied to cancer?",
        "structured_request": NO_FILTER_ANSWER,
    },
    {
        "i": 3,
        "data_source": DECKS_DATA_SOURCE,
        "user_query": "Compare the pros and cons of company NoviPel Holding ApS vs. company Solgate",
        "structured_request": WITH_LIMIT_ANSWER,
    },
    {
        "i": 3,
        "data_source": DECKS_DATA_SOURCE,
        "user_query": "Tell me about a company called Kiro?",
        "structured_request": FULL_ANSWER2,
    },
]

EXAMPLE_PROMPT_TEMPLATE = """\
<< Example {i}. >>
Data Source:
{data_source}

User Query:
{user_query}

Structured Request:
{structured_request}
"""

EXAMPLE_PROMPT = PromptTemplate.from_template(EXAMPLE_PROMPT_TEMPLATE)

USER_SPECIFIED_EXAMPLE_PROMPT = PromptTemplate.from_template(
    """\
<< Example {i}. >>
User Query:
{user_query}

Structured Request:
```json
{structured_request}
```
"""
)

DEFAULT_SCHEMA = """\
<< Structured Request Schema >>
When responding use a markdown code snippet with a JSON object formatted in the following schema:

```json
{{{{
    "query": string \\ text string to compare to document contents
    "filter": string \\ logical condition statement for filtering documents
}}}}
```

The query string should contain only text that is expected to match the contents of documents. Any conditions in the filter should not be mentioned in the query as well.

A logical condition statement is composed of one or more comparison and logical operation statements.

A comparison statement takes the form: `comp(attr, val)`:
- `comp` ({allowed_comparators}): comparator
- `attr` (string):  name of attribute to apply the comparison to
- `val` (string): is the comparison value

A logical operation statement takes the form `op(statement1, statement2, ...)`:
- `op` ({allowed_operators}): logical operator
- `statement1`, `statement2`, ... (comparison statements or logical operation statements): one or more statements to apply the operation to

Make sure that you only use the comparators and logical operators listed above and no others.
Make sure that filters only refer to attributes that exist in the data source.
Make sure that filters only use the attributed names with its function names if there are functions applied on them.
Make sure that filters only use format `YYYY-MM-DD` when handling timestamp data typed values.
Make sure that filters take into account the descriptions of attributes and only make comparisons that are feasible given the type of data being stored.
Make sure that filters are only used as needed. If there are no filters that should be applied return "NO_FILTER" for the filter value.\
"""
DEFAULT_SCHEMA_PROMPT = PromptTemplate.from_template(DEFAULT_SCHEMA)

SCHEMA_WITH_LIMIT = """\
<< Structured Request Schema >>
When responding use a markdown code snippet with a JSON object formatted in the following schema:

```json
{{{{
    "query": string \\ text string to compare to document contents
    "filter": string \\ logical condition statement for filtering documents
    "limit": int \\ the number of documents to retrieve
}}}}
```

The query string should contain only text that is expected to match the contents of documents. Any conditions in the filter should not be mentioned in the query as well.

A logical condition statement is composed of one or more comparison and logical operation statements.

A comparison statement takes the form: `comp(attr, val)`:
- `comp` ({allowed_comparators}): comparator
- `attr` (string):  name of attribute to apply the comparison to
- `val` (string): is the comparison value

A logical operation statement takes the form `op(statement1, statement2, ...)`:
- `op` ({allowed_operators}): logical operator
- `statement1`, `statement2`, ... (comparison statements or logical operation statements): one or more statements to apply the operation to

Make sure that you only use the comparators and logical operators listed above and no others.
Make sure that filters only refer to attributes that exist in the data source.
Make sure that filters only use the attributed names with its function names if there are functions applied on them.
Make sure that filters only use format `YYYY-MM-DD` when handling timestamp data typed values.
Make sure that filters take into account the descriptions of attributes and only make comparisons that are feasible given the type of data being stored.
Make sure that filters are only used as needed. If there are no filters that should be applied return "NO_FILTER" for the filter value.
Make sure the `limit` is always an int value. It is an optional parameter so leave it blank if it does not make sense.
"""
SCHEMA_WITH_LIMIT_PROMPT = PromptTemplate.from_template(SCHEMA_WITH_LIMIT)

DEFAULT_PREFIX = """\
Your goal is to structure the user's query to match the request schema provided below.

{schema}\
"""

PREFIX_WITH_DATA_SOURCE = (
    DEFAULT_PREFIX
    + """

<< Data Source >>
```json
{{{{
    "content": "{content}",
    "attributes": {attributes}
}}}}
```
"""
)

DEFAULT_SUFFIX = """\
<< Example {i}. >>
Data Source:
```json
{{{{
    "content": "{content}",
    "attributes": {attributes}
}}}}
```

User Query:
{{query}}

Structured Request:
"""

SUFFIX_WITHOUT_DATA_SOURCE = """\
<< Example {i}. >>
User Query:
{{query}}

Structured Request:
"""
