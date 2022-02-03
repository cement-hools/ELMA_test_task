from urllib.error import URLError
from urllib.request import urlopen

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from counts.serializers import QuerySerializer, AnswerSerializer


def url_count(item, time_out):
    url_result = {"url": item['url']}
    url_status = "error"

    try:
        response = urlopen(item['url'], timeout=time_out)
    except URLError:
        return None
    if response.getcode() == 200:
        html = response.read().decode('utf-8')
        cnt = html.count(item['query'])
        url_status = "ok"
        url_result["status"] = url_status
        if url_status == "ok":
            url_result["count"] = cnt
        return url_result


def count_query(urls, time_out):
    tasks = []
    urls_set = set()
    for item in urls:
        if item['url'] in urls_set:
            continue
        res = url_count(item, time_out)
        if res:
            tasks.append(res)
        urls_set.add(item['url'])

    return tasks


@api_view(['POST'])
def counts(request):
    serializer = QuerySerializer(data=request.data)
    if serializer.is_valid():

        urls = serializer.data.get('urls')
        timeout = serializer.data.get('max_timeout')

        result = count_query(urls, timeout)

        answer_serializer = AnswerSerializer(data={"urls": result})
        if answer_serializer.is_valid():
            return Response(answer_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
