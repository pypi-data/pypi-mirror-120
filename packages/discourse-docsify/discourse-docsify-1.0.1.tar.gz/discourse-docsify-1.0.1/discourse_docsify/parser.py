import re

import dateutil.parser
import humanize


class DiscourseParser:
    def __init__(self, api, locale):
        self.api = api
        self.locale = locale
        self.index_topic = None
        self.url_map = {}
        self.reverse_url_map = {}
        self.navigation_list = []

    def get_section_table(self, title):
        content = self.get_section_content(title)
        lines = content.split("\n")

        header = None
        table_data = []

        for line in lines:
            line = line.strip()
            if not line or line[0] != "|" or line[-1] != "|":
                continue
            columns = [x.strip() for x in line[1:-1].split("|")]
            if not header:
                header = [x.lower() for x in columns]
                continue
            if columns[0] == '--':
                continue
            row_data = {}
            for i in range(len(columns)):
                row_data[header[i]] = columns[i]
            table_data.append(row_data)

        return table_data

    def get_section_content(self, title):
        if not self.index_topic:
            return None

        index_content = self.index_topic['content']

        title_markup = f"# {title}"
        section_start = index_content.find(title_markup)
        if section_start < 0:
            return None
        section_start += len(title_markup)

        next_section_start = index_content.find("# ", section_start)

        if next_section_start < 0:
            content = index_content[section_start:]
        else:
            content = index_content[section_start:next_section_start]

        return content.strip()

    def get_url_map(self):
        urls_table = self.get_section_table("URLs")
        url_map = {}
        reverse_url_map = {}
        for entry in urls_table:
            url_map[entry['path']] = entry['topic']
            reverse_url_map[self.get_topic_id(entry['topic'])] = entry['path']
        return url_map, reverse_url_map

    def build_navigation_list(self):
        return self.get_section_table("Navigation")

    def parse(self):
        self.index_topic = self.api.get_topic(self.api.index_topic_id)

        self.url_map, self.reverse_url_map = self.get_url_map()

        self.navigation_list = self.build_navigation_list()

    def parse_content(self, topic, content, title):
        topic_url = f"{self.api.base_url}/t/{topic['slug']}/{topic['id']}"
        last_updated = dateutil.parser.parse(topic["post_stream"]["posts"][0]["updated_at"])

        if self.locale:
            humanize.i18n.activate(self.locale)
        last_updated = humanize.naturaltime(
            last_updated.replace(tzinfo=None)
        )

        # wiki link urls
        def get_wiki_link(match):
            topic_id = self.get_topic_id(match.group(2))
            if topic_id == self.api.index_topic_id:
                url = "/"
            elif topic_id in self.reverse_url_map:
                url = self.reverse_url_map[topic_id]
            else:
                url = f"{self.api.base_url}{match.group(2)}"
            return f"{match.group(1)}({url})"

        content = re.sub(rf"([^!]\[[^\]]*\])\({self.api.base_url}([^\)]*)\)", get_wiki_link, content)

        # image upload urls
        content = re.sub(r"\(upload://([^\)]*)\)", rf"({self.api.base_url}/uploads/short-url/\1)", content)

        return {
            'topic_url': topic_url,
            'title': title,
            'content': content,
            'last_updated': last_updated
        }

    def parse_topic(self, topic):
        return self.parse_content(topic, topic['content'], topic['title'])

    def get_topic_id(self, topic_url):
        return topic_url[topic_url.rfind("/"):]
