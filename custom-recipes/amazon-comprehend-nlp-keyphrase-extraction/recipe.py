# -*- coding: utf-8 -*-
import logging

from ratelimit import limits, RateLimitException
from retry import retry

import dataiku
from api_calling_utils import (
    generate_unique, fail_or_warn_on_row, api_parallelizer
)
from dataiku.customrecipe import (
    get_recipe_config, get_input_names_for_role, get_output_names_for_role
)
from dku_aws_nlp import (
    get_client
)


# ==============================================================================
# SETUP
# ==============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='[Amazon Comprehend NLP plugin] %(levelname)s - %(message)s'
)

api_configuration_preset = get_recipe_config().get("api_configuration_preset")
api_quota_rate_limit = api_configuration_preset.get("api_quota_rate_limit")
api_quota_period = api_configuration_preset.get("api_quota_period")
parallel_workers = api_configuration_preset.get("parallel_workers")
text_column = get_recipe_config().get('text_column')
text_language = get_recipe_config().get("language", '')
error_handling = get_recipe_config().get('error_handling')

input_dataset_name = get_input_names_for_role('input_dataset')[0]
input_dataset = dataiku.Dataset(input_dataset_name)

output_dataset_name = get_output_names_for_role('output_dataset')[0]
output_dataset = dataiku.Dataset(output_dataset_name)

if text_column is None or len(text_column) == 0:
    raise ValueError("You must specify the input text column.")
if text_column not in input_columns_names:
    raise ValueError(
        "Column '{}' is not present in the input dataset.".format(text_column)
    )


# ==============================================================================
# RUN
# ==============================================================================

input_df = input_dataset.get_dataframe()
response_column = generate_unique("raw_response", input_df.columns)
client = get_client(api_configuration_preset)


@retry((RateLimitException, OSError), delay=api_quota_period, tries=5)
@limits(calls=api_quota_rate_limit, period=api_quota_period)
@fail_or_warn_on_row(error_handling=error_handling)
def call_api_keyphrase_extraction(row, text_column, text_language="auto"):
    if text_language == "auto":
        if not isinstance(text, str) or text.strip() == '':
            return('')
        else:
            document = language.types.Document(
                content=text, language=text_language, type=DOCUMENT_TYPE)
            if entity_sentiment:
                response = client.analyze_entity_sentiment(
                    document=document, encoding_type=ENCODING_TYPE)
            else:
                response = client.analyze_entities(
                    document=document, encoding_
    else:
        raise NotImplementedError
        text_list = [r[text_column] for r in row]
type=ENCODING_TYPE)
        return MessageToJson(response)


output_df = api_parallelizer(
    input_df=input_df, api_call_function=call_api_named_entity_recognition,
    text_column=text_column, text_language=text_language,
    entity_sentiment=entity_sentiment, parallel_workers=parallel_workers)

output_df = output_df.apply(
    func=format_named_entity_recognition, axis=1,
    response_column=response_column, output_format=output_format,
    error_handling=error_handling)

output_dataset.write_with_schema(output_df)
