import requests


class DiscourseAPI:
    def __init__(self, base_url, api_username, api_key, index_topic_id):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.index_topic_id = index_topic_id

        if api_key and api_username:
            self.session.headers = {
                "Api-Key": api_key,
                "Api-Username": api_username,
            }

    def __del__(self):
        self.session.close()

    def get_topic(self, topic_id):
        """
        Retrieve topic object by path
        """

        response = self.session.get(f"{self.base_url}/t/{topic_id}.json")
        response.raise_for_status()

        topic = response.json()
        post_id = topic["post_stream"]["posts"][0]["id"]

        response = self.session.get(f"{self.base_url}/posts/{post_id}.json")
        response.raise_for_status()

        topic['content'] = response.json()['raw']

        return topic
