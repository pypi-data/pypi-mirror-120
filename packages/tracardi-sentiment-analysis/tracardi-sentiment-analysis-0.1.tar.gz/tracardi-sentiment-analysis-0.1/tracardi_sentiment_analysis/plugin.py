import os

import aiohttp
from dotenv import load_dotenv
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.domain.result import Result

from tracardi_sentiment_analysis.model.configuration import Configuration

load_dotenv()


class SentimentAnalysisAction(ActionRunner):

    def __init__(self, **kwargs):
        self.config = Configuration(**kwargs)

    async def run(self, payload):
        async with aiohttp.ClientSession() as session:
            params = {
                "key": self.config.key,
                "lang": self.config.language,
                "txt": self.config.text
            }
            async with session.post('https://api.meaningcloud.com/sentiment-2.1', params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    result = {
                        "sentiment": data['score_tag'],
                        "agreement": data['agreement'],
                        "subjectivity": data['subjectivity'],
                        "confidence": float(data['confidence'])
                    }

                    return Result(port="payload", value=result)

            return Result(port="payload", value={})


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_sentiment_analysis.plugin',
            className='SentimentAnalysisAction',
            inputs=["payload"],
            outputs=['payload'],
            version='0.1',
            license="MIT",
            author="Risto Kowaczewski",
            init={
                "key": None,
                "language": "en",
                "text": None
            }
        ),
        metadata=MetaData(
            name='Sentiment analysis',
            desc='It connects to the service that infers sentiment from a given sentence',
            type='flowNode',
            width=200,
            height=100,
            icon='icon',
            group=["Machine learning"]
        )
    )
