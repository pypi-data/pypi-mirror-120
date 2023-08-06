NicoApiClient
=============

概要
----

`ニコニコ動画 『スナップショット検索API
v2』 <https://site.nicovideo.jp/search-api-docs/snapshot>`__ などの API
について、仕様をなるべく意識せずに利用できるクライアントを提供する。

install
-------

PyPIリポジトリ: https://pypi.org/project/nicovideo-api-client/

.. code:: shell

   pip install nicovideo-api-client

installed
~~~~~~~~~

|Downloads| |image1| |image2|

documentation
~~~~~~~~~~~~~

`NicoApiClient
コードドキュメント <https://javakky.github.io/NicoApiClientDocs/>`__

example
-------

.. code:: python

   from nicovideo_api_client.api.v2.snapshot_search_api_v2 import SnapshotSearchAPIV2
   from nicovideo_api_client.constants import FieldType

   json = SnapshotSearchAPIV2() \
       .tags_exact() \
       .query("VOCALOID") \
       .field({FieldType.TITLE, FieldType.CONTENT_ID}) \
       .sort(FieldType.VIEW_COUNTER) \
       .simple_filter().filter() \
       .limit(100) \
       .request() \
       .json()

利用規約
--------

https://site.nicovideo.jp/search-api-docs/snapshot#api%E5%88%A9%E7%94%A8%E8%A6%8F%E7%B4%84

.. |Downloads| image:: https://pepy.tech/badge/nicovideo-api-client
   :target: https://pepy.tech/project/nicovideo-api-client
.. |image1| image:: https://pepy.tech/badge/nicovideo-api-client/month
   :target: https://pepy.tech/project/nicovideo-api-client
.. |image2| image:: https://pepy.tech/badge/nicovideo-api-client/week
   :target: https://pepy.tech/project/nicovideo-api-client
